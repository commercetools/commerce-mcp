from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import CreateRecurringOrdersParams, ReadRecurringOrdersParams, UpdateRecurringOrdersParams
from .functions import create_recurring_orders, read_recurring_orders, update_recurring_orders
from .prompts import CREATE_RECURRING_ORDER_PROMPT, READ_RECURRING_ORDER_PROMPT, UPDATE_RECURRING_ORDER_PROMPT

_RECURRING_ORDER_TOOLS = [
    ToolDefinition(
        method="read_recurring_orders",
        name="Read Recurring Orders",
        description=READ_RECURRING_ORDER_PROMPT,
        parameters=ReadRecurringOrdersParams,
        handler=read_recurring_orders,
        actions={"recurring_orders": {"read": True}},
    ),
    ToolDefinition(
        method="create_recurring_orders",
        name="Create Recurring Orders",
        description=CREATE_RECURRING_ORDER_PROMPT,
        parameters=CreateRecurringOrdersParams,
        handler=create_recurring_orders,
        actions={"recurring_orders": {"create": True}},
    ),
    ToolDefinition(
        method="update_recurring_orders",
        name="Update Recurring Orders",
        description=UPDATE_RECURRING_ORDER_PROMPT,
        parameters=UpdateRecurringOrdersParams,
        handler=update_recurring_orders,
        actions={"recurring_orders": {"update": True}},
    ),
]

for _tool in _RECURRING_ORDER_TOOLS:
    register_tool(_tool)
