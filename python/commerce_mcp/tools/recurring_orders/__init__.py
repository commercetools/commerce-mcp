from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import CreateRecurringOrdersParams, ReadRecurringOrdersParams, UpdateRecurringOrdersParams
from .functions import create_recurring_orders, read_recurring_orders, update_recurring_orders

_RECURRING_ORDER_TOOLS = [
    ToolDefinition(
        method="read_recurring_orders",
        name="Read Recurring Orders",
        description=(
            "Fetch a commercetools recurring order by ID, key, or list with optional filtering. "
            "In customer context only reads the customer's own recurring orders. "
            "Requires isAdmin or customerId context."
        ),
        parameters=ReadRecurringOrdersParams,
        handler=read_recurring_orders,
        actions={"recurring_orders": {"read": True}},
    ),
    ToolDefinition(
        method="create_recurring_orders",
        name="Create Recurring Orders",
        description=(
            "Create a new recurring order from a cart reference. "
            "Requires isAdmin context."
        ),
        parameters=CreateRecurringOrdersParams,
        handler=create_recurring_orders,
        actions={"recurring_orders": {"create": True}},
    ),
    ToolDefinition(
        method="update_recurring_orders",
        name="Update Recurring Orders",
        description=(
            "Apply update actions to an existing recurring order identified by ID or key. "
            "Requires isAdmin context."
        ),
        parameters=UpdateRecurringOrdersParams,
        handler=update_recurring_orders,
        actions={"recurring_orders": {"update": True}},
    ),
]

for _tool in _RECURRING_ORDER_TOOLS:
    register_tool(_tool)
