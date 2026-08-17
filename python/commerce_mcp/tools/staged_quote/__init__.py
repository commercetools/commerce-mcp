from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_staged_quote, read_staged_quote, update_staged_quote
from .schemas import CreateStagedQuoteParams, ReadStagedQuoteParams, UpdateStagedQuoteParams
from .prompts import CREATE_STAGED_QUOTE_PROMPT, READ_STAGED_QUOTE_PROMPT, UPDATE_STAGED_QUOTE_PROMPT

_STAGED_QUOTE_TOOLS = [
    ToolDefinition(
        method="read_staged_quote",
        name="Read Staged Quote",
        description=READ_STAGED_QUOTE_PROMPT,
        parameters=ReadStagedQuoteParams,
        handler=read_staged_quote,
        actions={"staged_quote": {"read": True}},
    ),
    ToolDefinition(
        method="create_staged_quote",
        name="Create Staged Quote",
        description=CREATE_STAGED_QUOTE_PROMPT,
        parameters=CreateStagedQuoteParams,
        handler=create_staged_quote,
        actions={"staged_quote": {"create": True}},
    ),
    ToolDefinition(
        method="update_staged_quote",
        name="Update Staged Quote",
        description=UPDATE_STAGED_QUOTE_PROMPT,
        parameters=UpdateStagedQuoteParams,
        handler=update_staged_quote,
        actions={"staged_quote": {"update": True}},
    ),
]

for _tool in _STAGED_QUOTE_TOOLS:
    register_tool(_tool)
