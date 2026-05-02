from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from fastmcp import FastMCP, Context
from fastmcp.tools import Tool

from .config import AuthConfig, Configuration, CTContext
from .api import CommercetoolsAPI

if TYPE_CHECKING:
    from .tools.registry import Registry


@dataclass
class AppState:
    """Shared state injected into every tool via fastMCP lifespan context."""
    api: CommercetoolsAPI
    ct_context: CTContext
    config: Configuration


def make_lifespan(auth: AuthConfig, config: Configuration):
    @asynccontextmanager
    async def lifespan(server: FastMCP):
        api = await CommercetoolsAPI.create(auth, config.context)
        try:
            yield AppState(api=api, ct_context=config.context, config=config)
        finally:
            await api.close()
    return lifespan


def build_server(auth: AuthConfig, config: Configuration, registry: "Registry | None" = None) -> FastMCP:
    """Constructs the FastMCP server from the tool registry.

    Tools are defined once in their namespace files (schemas + handler functions +
    register_tool() calls). This function reads the registry and wires each
    ToolDefinition into FastMCP — no duplicate @mcp.tool() decorators anywhere.

    If the number of permitted tools exceeds the dynamic loading threshold,
    three meta-tools (list / inject / execute) are registered instead.

    Pass an isolated Registry instance to use a different tool set — useful for
    testing or running multiple servers in the same process.
    """
    from .tools.registry import _default_registry

    reg = registry or _default_registry
    mcp = FastMCP("commerce-mcp", lifespan=make_lifespan(auth, config))
    permitted = reg.get_tools(config)
    threshold = config.context.dynamic_tool_loading_threshold

    if len(permitted) > threshold:
        _register_dynamic_tools(mcp)
    else:
        _register_tools_from_registry(mcp, permitted)

    return mcp


def _register_tools_from_registry(mcp: FastMCP, tools) -> None:
    """Programmatically register each ToolDefinition as a FastMCP tool.

    Each wrapper captures the ToolDefinition via closure and fetches AppState
    from the fastMCP lifespan context at call time.
    """
    from .tools.registry import ToolDefinition

    for tool in tools:
        _add_tool(mcp, tool)


def _add_tool(mcp: FastMCP, tool) -> None:
    params_model = tool.parameters

    async def handler(params, ctx: Context) -> str:
        state: AppState = ctx.request_context.lifespan_context  # type: ignore[attr-defined]
        return await tool.handler(params, state.api, state.ct_context)

    handler.__name__ = tool.method
    # Set annotations explicitly so Pydantic resolves them as real types, not strings.
    # (from __future__ import annotations at module level would otherwise stringify them.)
    handler.__annotations__ = {"params": params_model, "ctx": Context, "return": str}
    mcp.add_tool(Tool.from_function(handler, name=tool.method, description=tool.description))


def _register_dynamic_tools(mcp: FastMCP) -> None:
    from .tools.dynamic import list_available_tools, inject_tools, execute_tool
    from .tools.dynamic import (
        ListAvailableToolsParams,
        InjectToolsParams,
        ExecuteToolParams,
    )

    for fn, params_model, name, description in [
        (list_available_tools, ListAvailableToolsParams,
         "list_available_tools",
         "List all available Commercetools tools grouped by resource namespace."),
        (inject_tools, InjectToolsParams,
         "inject_tools",
         "Dynamically inject specific tools into this MCP session by method name."),
        (execute_tool, ExecuteToolParams,
         "execute_tool",
         "Execute any available Commercetools tool by method name without pre-injecting it."),
    ]:
        _fn, _pm, _name, _desc = fn, params_model, name, description

        async def _handler(params, ctx: Context, __fn=_fn) -> str:
            return await __fn(params, ctx)

        _handler.__name__ = _name
        _handler.__annotations__ = {"params": _pm, "ctx": Context, "return": str}
        mcp.add_tool(Tool.from_function(_handler, name=_name, description=_desc))
