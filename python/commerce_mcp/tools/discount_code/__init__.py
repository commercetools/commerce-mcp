from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_discount_code, read_discount_code, update_discount_code
from .prompts import CREATE_DISCOUNT_CODE_PROMPT, READ_DISCOUNT_CODE_PROMPT, UPDATE_DISCOUNT_CODE_PROMPT
from .schemas import CreateDiscountCodeParams, ReadDiscountCodeParams, UpdateDiscountCodeParams

_DISCOUNT_CODE_TOOLS = [
    ToolDefinition(
        method="read_discount_code",
        name="Read Discount Code",
        description=READ_DISCOUNT_CODE_PROMPT,
        parameters=ReadDiscountCodeParams,
        handler=read_discount_code,
        actions={"discount_code": {"read": True}},
    ),
    ToolDefinition(
        method="create_discount_code",
        name="Create Discount Code",
        description=CREATE_DISCOUNT_CODE_PROMPT,
        parameters=CreateDiscountCodeParams,
        handler=create_discount_code,
        actions={"discount_code": {"create": True}},
    ),
    ToolDefinition(
        method="update_discount_code",
        name="Update Discount Code",
        description=UPDATE_DISCOUNT_CODE_PROMPT,
        parameters=UpdateDiscountCodeParams,
        handler=update_discount_code,
        actions={"discount_code": {"update": True}},
    ),
]

for _tool in _DISCOUNT_CODE_TOOLS:
    register_tool(_tool)
