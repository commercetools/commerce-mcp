from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadQuoteParams, CreateQuoteParams, UpdateQuoteParams
from .functions import read_quote, create_quote, update_quote
from .prompts import CREATE_QUOTE_PROMPT, READ_QUOTE_PROMPT, UPDATE_QUOTE_PROMPT

_TOOLS = [
    ToolDefinition(
        method="read_quote",
        name="Read Quote",
        description=READ_QUOTE_PROMPT,
        parameters=ReadQuoteParams,
        handler=read_quote,
        actions={"quote": {"read": True}},
    ),
    ToolDefinition(
        method="create_quote",
        name="Create Quote",
        description=CREATE_QUOTE_PROMPT,
        parameters=CreateQuoteParams,
        handler=create_quote,
        actions={"quote": {"create": True}},
    ),
    ToolDefinition(
        method="update_quote",
        name="Update Quote",
        description=UPDATE_QUOTE_PROMPT,
        parameters=UpdateQuoteParams,
        handler=update_quote,
        actions={"quote": {"update": True}},
    ),
]

for _tool in _TOOLS:
    register_tool(_tool)
