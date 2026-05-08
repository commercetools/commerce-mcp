from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_staged_quote, read_staged_quote, update_staged_quote
from .schemas import CreateStagedQuoteParams, ReadStagedQuoteParams, UpdateStagedQuoteParams

_STAGED_QUOTE_TOOLS = [
    ToolDefinition(
        method="read_staged_quote",
        name="Read Staged Quote",
        description=(
            "Read a staged quote or query staged quotes in commercetools. "
            "Provide an id or key to fetch a specific staged quote, or omit both to list "
            "staged quotes with optional filtering. Supports store-scoped and admin access."
        ),
        parameters=ReadStagedQuoteParams,
        handler=read_staged_quote,
        actions={"staged_quote": {"read": True}},
    ),
    ToolDefinition(
        method="create_staged_quote",
        name="Create Staged Quote",
        description=(
            "Create a new staged quote in commercetools from an existing quote request. "
            "Requires a quoteRequest reference and quoteRequestVersion. "
            "Supports store-scoped and admin access."
        ),
        parameters=CreateStagedQuoteParams,
        handler=create_staged_quote,
        actions={"staged_quote": {"create": True}},
    ),
    ToolDefinition(
        method="update_staged_quote",
        name="Update Staged Quote",
        description=(
            "Update an existing staged quote in commercetools using update actions. "
            "Requires either id or key, the current version, and an array of update actions. "
            "Supports store-scoped and admin access."
        ),
        parameters=UpdateStagedQuoteParams,
        handler=update_staged_quote,
        actions={"staged_quote": {"update": True}},
    ),
]

for _tool in _STAGED_QUOTE_TOOLS:
    register_tool(_tool)
