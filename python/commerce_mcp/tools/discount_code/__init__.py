from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_discount_code, read_discount_code, update_discount_code
from .schemas import CreateDiscountCodeParams, ReadDiscountCodeParams, UpdateDiscountCodeParams

_DISCOUNT_CODE_TOOLS = [
    ToolDefinition(
        method="read_discount_code",
        name="Read Discount Code",
        description="Read or list discount codes. Provide an id or key to fetch a specific code, or omit both to list codes with optional filtering.",
        parameters=ReadDiscountCodeParams,
        handler=read_discount_code,
        actions={"discount_code": {"read": True}},
    ),
    ToolDefinition(
        method="create_discount_code",
        name="Create Discount Code",
        description="Create a new discount code linked to one or more cart discounts.",
        parameters=CreateDiscountCodeParams,
        handler=create_discount_code,
        actions={"discount_code": {"create": True}},
    ),
    ToolDefinition(
        method="update_discount_code",
        name="Update Discount Code",
        description="Apply update actions to an existing discount code identified by id or key.",
        parameters=UpdateDiscountCodeParams,
        handler=update_discount_code,
        actions={"discount_code": {"update": True}},
    ),
]

for _tool in _DISCOUNT_CODE_TOOLS:
    register_tool(_tool)
