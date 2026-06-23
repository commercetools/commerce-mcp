"""Dynamic tool loading system.

When the number of active tools exceeds the threshold in CTContext,
server.py registers these three handler functions as FastMCP tools instead
of registering every namespace tool individually.
This keeps the LLM's context window manageable for large tool sets.

Usage pattern (mirrors TypeScript resource-based-tools-system):
  1. list_available_tools — discover what's available by resource
  2. inject_tools          — load specific tools into the active set
  3. execute_tool          — run any tool by method name
"""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any
from fastmcp import Context
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from ...server import AppState


class ListAvailableToolsParams(BaseModel):
    resource: str | None = Field(
        None,
        description="Filter by resource namespace, e.g. 'products', 'orders'. Omit to list all.",
    )


class InjectToolsParams(BaseModel):
    tool_names: list[str] = Field(
        description="Method names of the tools to inject, e.g. ['list_products', 'create_order']"
    )


class ExecuteToolParams(BaseModel):
    tool_method: str = Field(description="Method name of the tool to execute, e.g. 'list_products'")
    arguments: dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments matching the tool's parameter schema",
    )


async def list_available_tools(params: ListAvailableToolsParams, ctx: Context) -> str:
    from ...tools.registry import get_tools
    state: "AppState" = ctx.request_context.lifespan_context  # type: ignore[attr-defined]
    tools = get_tools(state.config)

    groups: dict[str, list[str]] = {}
    for tool in tools:
        for ns in tool.actions:
            groups.setdefault(ns, []).append(f"{tool.method}: {tool.description[:80]}")

    if params.resource:
        filtered = {k: v for k, v in groups.items() if params.resource in k}
        return json.dumps(filtered, indent=2)

    return json.dumps(groups, indent=2)


async def inject_tools(params: InjectToolsParams, ctx: Context) -> str:
    from ...tools.registry import get_tools
    state: "AppState" = ctx.request_context.lifespan_context  # type: ignore[attr-defined]
    all_tools = {t.method: t for t in get_tools(state.config)}

    injected: list[str] = []
    missing: list[str] = []

    for name in params.tool_names:
        if name not in all_tools:
            missing.append(name)
            continue
        tool = all_tools[name]
        server = ctx.request_context.server  # type: ignore[attr-defined]
        if hasattr(server, "_tool_manager"):
            server._tool_manager.add_tool(  # type: ignore[attr-defined]
                tool.handler,
                name=tool.method,
                description=tool.description,
            )
        injected.append(name)

    result: dict[str, Any] = {"injected": injected}
    if missing:
        result["not_found"] = missing
    return json.dumps(result, indent=2)


async def execute_tool(params: ExecuteToolParams, ctx: Context) -> str:
    from ...tools.registry import get_tools
    state: "AppState" = ctx.request_context.lifespan_context  # type: ignore[attr-defined]
    all_tools = {t.method: t for t in get_tools(state.config)}

    tool = all_tools.get(params.tool_method)
    if tool is None:
        return json.dumps({"error": f"Tool '{params.tool_method}' not found"})

    parsed_params = tool.parameters(**params.arguments)
    result = await tool.handler(parsed_params, state.api, state.ct_context)
    return result if isinstance(result, str) else json.dumps(result, default=str)
