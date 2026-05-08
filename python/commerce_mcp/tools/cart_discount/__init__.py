from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_cart_discount, read_cart_discount, update_cart_discount
from .schemas import CreateCartDiscountParams, ReadCartDiscountParams, UpdateCartDiscountParams

_CART_DISCOUNT_TOOLS = [
    ToolDefinition(
        method="read_cart_discount",
        name="Read Cart Discount",
        description=(
            "Fetch cart discounts from commercetools. "
            "Provide an id or key to fetch a specific cart discount, or omit both to list "
            "cart discounts with optional filtering. Supports store-scoped and admin access."
        ),
        parameters=ReadCartDiscountParams,
        handler=read_cart_discount,
        actions={"cart_discount": {"read": True}},
    ),
    ToolDefinition(
        method="create_cart_discount",
        name="Create Cart Discount",
        description=(
            "Create a new Cart Discount in commercetools. "
            "Requires name, cartPredicate, value, and sortOrder. "
            "Supports store-scoped and admin access."
        ),
        parameters=CreateCartDiscountParams,
        handler=create_cart_discount,
        actions={"cart_discount": {"create": True}},
    ),
    ToolDefinition(
        method="update_cart_discount",
        name="Update Cart Discount",
        description=(
            "Update a Cart Discount in commercetools using update actions. "
            "Requires either id or key, the current version, and an array of update actions. "
            "Supports store-scoped and admin access."
        ),
        parameters=UpdateCartDiscountParams,
        handler=update_cart_discount,
        actions={"cart_discount": {"update": True}},
    ),
]

for _tool in _CART_DISCOUNT_TOOLS:
    register_tool(_tool)
