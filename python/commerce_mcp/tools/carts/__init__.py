from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .prompts import CREATE_CART_PROMPT, READ_CART_PROMPT, REPLICATE_CART_PROMPT, UPDATE_CART_PROMPT
from .schemas import ReadCartParams, CreateCartParams, ReplicateCartParams, UpdateCartParams
from .functions import read_cart, create_cart, replicate_cart, update_cart

_CART_TOOLS = [
    ToolDefinition(
        method="read_cart",
        name="Read Cart",
        description=READ_CART_PROMPT,
        parameters=ReadCartParams,
        handler=read_cart,
        actions={"cart": {"read": True}},
    ),
    ToolDefinition(
        method="create_cart",
        name="Create Cart",
        description=CREATE_CART_PROMPT,
        parameters=CreateCartParams,
        handler=create_cart,
        actions={"cart": {"create": True}},
    ),
    ToolDefinition(
        method="replicate_cart",
        name="Replicate Cart",
        description=REPLICATE_CART_PROMPT,
        parameters=ReplicateCartParams,
        handler=replicate_cart,
        actions={"cart": {"create": True}},
    ),
    ToolDefinition(
        method="update_cart",
        name="Update Cart",
        description=UPDATE_CART_PROMPT,
        parameters=UpdateCartParams,
        handler=update_cart,
        actions={"cart": {"update": True}},
    ),
]

for _tool in _CART_TOOLS:
    register_tool(_tool)
