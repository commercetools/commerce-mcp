from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadOrderParams, CreateOrderParams, UpdateOrderParams
from .functions import read_order, create_order, update_order

_ORDER_TOOLS = [
    ToolDefinition(
        method="read_order",
        name="Read Order",
        description="Read orders. Routes automatically to admin, customer, store, or associate scope.",
        parameters=ReadOrderParams,
        handler=read_order,
        actions={"order": {"read": True}},
    ),
    ToolDefinition(
        method="create_order",
        name="Create Order",
        description="Convert a cart into an order.",
        parameters=CreateOrderParams,
        handler=create_order,
        actions={"order": {"create": True}},
    ),
    ToolDefinition(
        method="update_order",
        name="Update Order",
        description="Apply update actions to an existing order.",
        parameters=UpdateOrderParams,
        handler=update_order,
        actions={"order": {"update": True}},
    ),
]

for _tool in _ORDER_TOOLS:
    register_tool(_tool)
