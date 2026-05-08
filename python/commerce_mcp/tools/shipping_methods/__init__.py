from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import read_shipping_methods, create_shipping_methods, update_shipping_methods
from .schemas import (
    ReadShippingMethodsParams,
    CreateShippingMethodsParams,
    UpdateShippingMethodsParams,
)

_SHIPPING_METHODS_TOOLS = [
    ToolDefinition(
        method="read_shipping_methods",
        name="Read Shipping Methods",
        description=(
            "Read or list shipping methods. Provide an id or key to fetch a specific shipping method, "
            "or omit both to list shipping methods with optional filtering, sorting, and pagination. "
            "Admin-only operation."
        ),
        parameters=ReadShippingMethodsParams,
        handler=read_shipping_methods,
        actions={"shipping_methods": {"read": True}},
    ),
    ToolDefinition(
        method="create_shipping_methods",
        name="Create Shipping Methods",
        description=(
            "Create a new shipping method with a name, zone rates, optional tax category, and other "
            "settings. Zone rates define the shipping price per geographic zone. Admin-only operation."
        ),
        parameters=CreateShippingMethodsParams,
        handler=create_shipping_methods,
        actions={"shipping_methods": {"create": True}},
    ),
    ToolDefinition(
        method="update_shipping_methods",
        name="Update Shipping Methods",
        description=(
            "Apply update actions to an existing shipping method identified by id or key. "
            "Supported actions include: changeName, setDescription, addZoneRate, removeZoneRate, "
            "setDefault, setTaxCategory, setCustomType, setCustomField. Admin-only operation."
        ),
        parameters=UpdateShippingMethodsParams,
        handler=update_shipping_methods,
        actions={"shipping_methods": {"update": True}},
    ),
]

for _tool in _SHIPPING_METHODS_TOOLS:
    register_tool(_tool)
