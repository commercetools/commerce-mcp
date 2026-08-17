"""Vercel AI SDK adapter.

Emits tool definitions in the OpenAI function-call JSON format that the
Vercel AI SDK (and openai Python SDK) understands. Use this when a
TypeScript AI SDK frontend calls into a Python backend for tool execution.

No extra dependencies required.
"""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...config import Configuration
    from ...api import CommercetoolsAPI


def get_ai_sdk_tools(config: "Configuration") -> list[dict[str, Any]]:
    """Returns Vercel AI SDK / OpenAI-compatible tool definitions.

    Example (TypeScript AI SDK calling a Python HTTP endpoint)::

        # Python side — return these from GET /tools
        from commerce_mcp.integrations.ai_sdk import get_ai_sdk_tools
        tools = get_ai_sdk_tools(config)

        # TypeScript AI SDK side:
        # const tools = await fetch('/tools').then(r => r.json());
        # const result = await generateText({ model, tools, prompt });

    Example (OpenAI Python SDK)::

        from openai import OpenAI
        from commerce_mcp.integrations.ai_sdk import get_ai_sdk_tools, dispatch_tool_call

        client = OpenAI()
        tools = get_ai_sdk_tools(config)
        response = client.chat.completions.create(
            model="gpt-4o",
            tools=tools,
            messages=[...],
        )
        for call in response.choices[0].message.tool_calls or []:
            result = await dispatch_tool_call(call.function.name, call.function.arguments, api, config)
    """
    from ...tools.registry import get_tools

    return [
        {
            "type": "function",
            "function": {
                "name": tool.method,
                "description": tool.description,
                "parameters": tool.parameters.model_json_schema(),
            },
        }
        for tool in get_tools(config)
    ]


async def dispatch_tool_call(
    tool_name: str,
    tool_input: "dict[str, Any] | str",
    api: "CommercetoolsAPI",
    config: "Configuration",
) -> str:
    """Dispatches a function_call from an OpenAI / Vercel AI SDK response."""
    import json as _json
    from ...tools.registry import get_tools

    if isinstance(tool_input, str):
        tool_input = _json.loads(tool_input)

    registry = {t.method: t for t in get_tools(config)}
    tool = registry.get(tool_name)
    if tool is None:
        return f"Error: tool '{tool_name}' not found"

    params = tool.parameters(**tool_input)
    result = await tool.handler(params, api, config.context)
    return result if isinstance(result, str) else str(result)
