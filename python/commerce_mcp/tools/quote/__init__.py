from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadQuoteParams, CreateQuoteParams, UpdateQuoteParams
from .functions import read_quote, create_quote, update_quote

_TOOLS = [
    ToolDefinition(
        method="read_quote",
        name="Read Quote",
        description=(
            "Fetch a commercetools quote by ID, key, or query predicates. "
            "Routes to associate (/as-associate/{id}/in-business-unit/key={key}/quotes), "
            "customer (/quotes with customer filter), "
            "store (/in-store/key={storeKey}/quotes), "
            "or admin (/quotes) scope based on context."
        ),
        parameters=ReadQuoteParams,
        handler=read_quote,
        actions={"quote": {"read": True}},
    ),
    ToolDefinition(
        method="create_quote",
        name="Create Quote",
        description=(
            "Create a new commercetools quote from a staged quote. "
            "Routes to store (/in-store/key={storeKey}/quotes) "
            "or admin (/quotes) scope based on context. "
            "Not available for customer-only or associate context."
        ),
        parameters=CreateQuoteParams,
        handler=create_quote,
        actions={"quote": {"create": True}},
    ),
    ToolDefinition(
        method="update_quote",
        name="Update Quote",
        description=(
            "Apply update actions to an existing commercetools quote identified by ID or key. "
            "Routes to associate (/as-associate/{id}/in-business-unit/key={key}/quotes), "
            "customer (/quotes with ownership check), "
            "store (/in-store/key={storeKey}/quotes), "
            "or admin (/quotes) scope based on context."
        ),
        parameters=UpdateQuoteParams,
        handler=update_quote,
        actions={"quote": {"update": True}},
    ),
]

for _tool in _TOOLS:
    register_tool(_tool)
