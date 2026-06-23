"""Anthropic SDK adapter.

Exposes ToolDefinitions in the format expected by the Anthropic Messages API
(tool_use blocks). Compatible with claude-opus-4-7, claude-sonnet-4-6, etc.

Requires: pip install commerce-mcp[anthropic]
"""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...config import Configuration
    from ...api import CommercetoolsAPI


def get_anthropic_tools(config: "Configuration") -> list[dict[str, Any]]:
    """Returns Anthropic tool definitions for use with client.messages.create(tools=...).

    Example::

        import anthropic
        from commerce_mcp.integrations.anthropic_sdk import get_anthropic_tools, dispatch_tool_call

        client = anthropic.Anthropic()
        tools = get_anthropic_tools(config)

        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=4096,
            tools=tools,
            messages=[{"role": "user", "content": "List 5 products"}],
        )
        for block in response.content:
            if block.type == "tool_use":
                result = await dispatch_tool_call(block.name, block.input, api, config)
    """
    from ...tools.registry import get_tools

    return [
        {
            "name": tool.method,
            "description": tool.description,
            "input_schema": tool.parameters.model_json_schema(),
        }
        for tool in get_tools(config)
    ]


async def dispatch_tool_call(
    tool_name: str,
    tool_input: dict[str, Any],
    api: "CommercetoolsAPI",
    config: "Configuration",
) -> str:
    """Dispatches a tool_use block from an Anthropic response to the correct handler."""
    from ...tools.registry import get_tools

    registry = {t.method: t for t in get_tools(config)}
    tool = registry.get(tool_name)
    if tool is None:
        return f"Error: tool '{tool_name}' not found"

    params = tool.parameters(**tool_input)
    result = await tool.handler(params, api, config.context)
    return result if isinstance(result, str) else str(result)
