from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadQuoteRequestParams, CreateQuoteRequestParams, UpdateQuoteRequestParams
from .functions import read_quote_request, create_quote_request, update_quote_request
from .prompts import CREATE_QUOTE_REQUEST_PROMPT, READ_QUOTE_REQUEST_PROMPT, UPDATE_QUOTE_REQUEST_PROMPT

_TOOLS = [
    ToolDefinition(
        method="read_quote_request",
        name="Read Quote Request",
        description=READ_QUOTE_REQUEST_PROMPT,
        parameters=ReadQuoteRequestParams,
        handler=read_quote_request,
        actions={"quote_request": {"read": True}},
    ),
    ToolDefinition(
        method="create_quote_request",
        name="Create Quote Request",
        description=CREATE_QUOTE_REQUEST_PROMPT,
        parameters=CreateQuoteRequestParams,
        handler=create_quote_request,
        actions={"quote_request": {"create": True}},
    ),
    ToolDefinition(
        method="update_quote_request",
        name="Update Quote Request",
        description=UPDATE_QUOTE_REQUEST_PROMPT,
        parameters=UpdateQuoteRequestParams,
        handler=update_quote_request,
        actions={"quote_request": {"update": True}},
    ),
]

for _tool in _TOOLS:
    register_tool(_tool)
