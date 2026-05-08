from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadQuoteRequestParams, CreateQuoteRequestParams, UpdateQuoteRequestParams
from .functions import read_quote_request, create_quote_request, update_quote_request

_TOOLS = [
    ToolDefinition(
        method="read_quote_request",
        name="Read Quote Request",
        description=(
            "Fetch a commercetools quote request by ID, key, or query predicates. "
            "Routes to associate (/as-associate/{id}/in-business-unit/key={key}/quote-requests), "
            "customer (/me/quote-requests), "
            "store (/in-store/key={storeKey}/quote-requests), "
            "or admin (/quote-requests) scope based on context."
        ),
        parameters=ReadQuoteRequestParams,
        handler=read_quote_request,
        actions={"quote_request": {"read": True}},
    ),
    ToolDefinition(
        method="create_quote_request",
        name="Create Quote Request",
        description=(
            "Create a new commercetools quote request from a cart. "
            "Routes to associate (/as-associate/{id}/in-business-unit/key={key}/quote-requests), "
            "store (/in-store/key={storeKey}/quote-requests), "
            "or admin (/quote-requests) scope based on context. "
            "Not available for customer-only context."
        ),
        parameters=CreateQuoteRequestParams,
        handler=create_quote_request,
        actions={"quote_request": {"create": True}},
    ),
    ToolDefinition(
        method="update_quote_request",
        name="Update Quote Request",
        description=(
            "Apply update actions to an existing commercetools quote request identified by ID or key. "
            "Routes to associate (/as-associate/{id}/in-business-unit/key={key}/quote-requests), "
            "customer (/me/quote-requests), "
            "store (/in-store/key={storeKey}/quote-requests), "
            "or admin (/quote-requests) scope based on context."
        ),
        parameters=UpdateQuoteRequestParams,
        handler=update_quote_request,
        actions={"quote_request": {"update": True}},
    ),
]

for _tool in _TOOLS:
    register_tool(_tool)
