"""LangChain adapter.

Wraps ToolDefinitions into LangChain StructuredTools so they can be
used with any LangChain agent (create_react_agent, AgentExecutor, etc.).

Requires: pip install commerce-mcp[langchain]
"""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...config import Configuration
    from ...api import CommercetoolsAPI


def get_langchain_tools(config: "Configuration", api: "CommercetoolsAPI") -> list[Any]:
    """Returns a list of LangChain StructuredTools built from the permitted tool set.

    Example::

        from commerce_mcp import Configuration, CTContext, Actions, ResourceActions
        from commerce_mcp.api import CommercetoolsAPI
        from commerce_mcp.integrations.langchain import get_langchain_tools
        from langchain_anthropic import ChatAnthropic
        from langgraph.prebuilt import create_react_agent

        config = Configuration(
            actions=Actions(products=ResourceActions(read=True)),
            context=CTContext(is_admin=True),
        )
        api = await CommercetoolsAPI.create(auth, config.context)
        tools = get_langchain_tools(config, api)
        agent = create_react_agent(ChatAnthropic(model="claude-opus-4-7"), tools)
    """
    try:
        from langchain_core.tools import StructuredTool
    except ImportError as exc:
        raise ImportError(
            "langchain-core is required: pip install commerce-mcp[langchain]"
        ) from exc

    from ...tools.registry import get_tools

    lc_tools: list[Any] = []
    for tool in get_tools(config):
        # Capture loop variable with default arg
        def _make_coroutine(t=tool):
            async def coroutine(**kwargs: Any) -> str:
                params = t.parameters(**kwargs)
                result = await t.handler(params, api, config.context)
                return result if isinstance(result, str) else str(result)
            return coroutine

        lc_tools.append(
            StructuredTool(
                name=tool.method,
                description=tool.description,
                args_schema=tool.parameters,
                coroutine=_make_coroutine(),
                return_direct=False,
            )
        )
    return lc_tools
