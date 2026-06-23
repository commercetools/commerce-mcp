from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .prompts import CREATE_ORDER_PROMPT, READ_ORDER_PROMPT, UPDATE_ORDER_PROMPT
from .schemas import ReadOrderParams, CreateOrderParams, UpdateOrderParams
from .functions import read_order, create_order, update_order

_ORDER_TOOLS = [
    ToolDefinition(
        method="read_order",
        name="Read Order",
        description=READ_ORDER_PROMPT,
        parameters=ReadOrderParams,
        handler=read_order,
        actions={"order": {"read": True}},
    ),
    ToolDefinition(
        method="create_order",
        name="Create Order",
        description=CREATE_ORDER_PROMPT,
        parameters=CreateOrderParams,
        handler=create_order,
        actions={"order": {"create": True}},
    ),
    ToolDefinition(
        method="update_order",
        name="Update Order",
        description=UPDATE_ORDER_PROMPT,
        parameters=UpdateOrderParams,
        handler=update_order,
        actions={"order": {"update": True}},
    ),
]

for _tool in _ORDER_TOOLS:
    register_tool(_tool)
