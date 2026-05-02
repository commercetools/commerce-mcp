from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadOrderParams, CreateOrderParams, UpdateOrderParams
from .functions import read_order, create_order, update_order

_ORDER_TOOLS = [
    ToolDefinition(
        method="read_order",
        name="Read Order",
        description=(
            "Fetch a commercetools order by ID, order number, or query predicates. "
            "Routes to admin, customer, store, or associate scope based on context."
        ),
        parameters=ReadOrderParams,
        handler=read_order,
        actions={"order": {"read": True}},
    ),
    ToolDefinition(
        method="create_order",
        name="Create Order",
        description=(
            "Create a commercetools order from a cart, from a quote, or by import. "
            "Routes to admin, store, or associate scope based on context."
        ),
        parameters=CreateOrderParams,
        handler=create_order,
        actions={"order": {"create": True}},
    ),
    ToolDefinition(
        method="update_order",
        name="Update Order",
        description=(
            "Apply update actions to an existing commercetools order identified by ID or order number. "
            "Routes to admin, store, or associate scope based on context."
        ),
        parameters=UpdateOrderParams,
        handler=update_order,
        actions={"order": {"update": True}},
    ),
]

for _tool in _ORDER_TOOLS:
    register_tool(_tool)
