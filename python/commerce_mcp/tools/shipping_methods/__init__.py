from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import read_shipping_methods, create_shipping_methods, update_shipping_methods
from .schemas import (
    ReadShippingMethodsParams,
    CreateShippingMethodsParams,
    UpdateShippingMethodsParams,
)
from .prompts import CREATE_SHIPPING_METHOD_PROMPT, READ_SHIPPING_METHOD_PROMPT, UPDATE_SHIPPING_METHOD_PROMPT

_SHIPPING_METHODS_TOOLS = [
    ToolDefinition(
        method="read_shipping_methods",
        name="Read Shipping Methods",
        description=READ_SHIPPING_METHOD_PROMPT,
        parameters=ReadShippingMethodsParams,
        handler=read_shipping_methods,
        actions={"shipping_methods": {"read": True}},
    ),
    ToolDefinition(
        method="create_shipping_methods",
        name="Create Shipping Methods",
        description=CREATE_SHIPPING_METHOD_PROMPT,
        parameters=CreateShippingMethodsParams,
        handler=create_shipping_methods,
        actions={"shipping_methods": {"create": True}},
    ),
    ToolDefinition(
        method="update_shipping_methods",
        name="Update Shipping Methods",
        description=UPDATE_SHIPPING_METHOD_PROMPT,
        parameters=UpdateShippingMethodsParams,
        handler=update_shipping_methods,
        actions={"shipping_methods": {"update": True}},
    ),
]

for _tool in _SHIPPING_METHODS_TOOLS:
    register_tool(_tool)
