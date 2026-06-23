from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_product_discount, read_product_discount, update_product_discount
from .prompts import CREATE_PRODUCT_DISCOUNT_PROMPT, READ_PRODUCT_DISCOUNT_PROMPT, UPDATE_PRODUCT_DISCOUNT_PROMPT
from .schemas import CreateProductDiscountParams, ReadProductDiscountParams, UpdateProductDiscountParams

_PRODUCT_DISCOUNT_TOOLS = [
    ToolDefinition(
        method="read_product_discount",
        name="Read Product Discount",
        description=READ_PRODUCT_DISCOUNT_PROMPT,
        parameters=ReadProductDiscountParams,
        handler=read_product_discount,
        actions={"product_discount": {"read": True}},
    ),
    ToolDefinition(
        method="create_product_discount",
        name="Create Product Discount",
        description=CREATE_PRODUCT_DISCOUNT_PROMPT,
        parameters=CreateProductDiscountParams,
        handler=create_product_discount,
        actions={"product_discount": {"create": True}},
    ),
    ToolDefinition(
        method="update_product_discount",
        name="Update Product Discount",
        description=UPDATE_PRODUCT_DISCOUNT_PROMPT,
        parameters=UpdateProductDiscountParams,
        handler=update_product_discount,
        actions={"product_discount": {"update": True}},
    ),
]

for _tool in _PRODUCT_DISCOUNT_TOOLS:
    register_tool(_tool)
