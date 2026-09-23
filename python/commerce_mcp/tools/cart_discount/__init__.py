from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_cart_discount, read_cart_discount, update_cart_discount
from .prompts import CREATE_CART_DISCOUNT_PROMPT, READ_CART_DISCOUNT_PROMPT, UPDATE_CART_DISCOUNT_PROMPT
from .schemas import CreateCartDiscountParams, ReadCartDiscountParams, UpdateCartDiscountParams

_CART_DISCOUNT_TOOLS = [
    ToolDefinition(
        method="read_cart_discount",
        name="Read Cart Discount",
        description=READ_CART_DISCOUNT_PROMPT,
        parameters=ReadCartDiscountParams,
        handler=read_cart_discount,
        actions={"cart_discount": {"read": True}},
    ),
    ToolDefinition(
        method="create_cart_discount",
        name="Create Cart Discount",
        description=CREATE_CART_DISCOUNT_PROMPT,
        parameters=CreateCartDiscountParams,
        handler=create_cart_discount,
        actions={"cart_discount": {"create": True}},
    ),
    ToolDefinition(
        method="update_cart_discount",
        name="Update Cart Discount",
        description=UPDATE_CART_DISCOUNT_PROMPT,
        parameters=UpdateCartDiscountParams,
        handler=update_cart_discount,
        actions={"cart_discount": {"update": True}},
    ),
]

for _tool in _CART_DISCOUNT_TOOLS:
    register_tool(_tool)
