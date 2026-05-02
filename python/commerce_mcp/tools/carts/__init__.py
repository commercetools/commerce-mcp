from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadCartParams, CreateCartParams, UpdateCartParams
from .functions import read_cart, create_cart, update_cart

_CART_TOOLS = [
    ToolDefinition(
        method="read_cart",
        name="Read Cart",
        description="Read carts. Scoped to associate, customer, store, or admin context.",
        parameters=ReadCartParams,
        handler=read_cart,
        actions={"cart": {"read": True}},
    ),
    ToolDefinition(
        method="create_cart",
        name="Create Cart",
        description="Create a new cart. Scoped to associate, customer, store, or admin context.",
        parameters=CreateCartParams,
        handler=create_cart,
        actions={"cart": {"create": True}},
    ),
    ToolDefinition(
        method="update_cart",
        name="Update Cart",
        description="Apply update actions to an existing cart.",
        parameters=UpdateCartParams,
        handler=update_cart,
        actions={"cart": {"update": True}},
    ),
]

for _tool in _CART_TOOLS:
    register_tool(_tool)
