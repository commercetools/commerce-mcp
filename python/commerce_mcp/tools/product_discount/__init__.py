from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_product_discount, read_product_discount, update_product_discount
from .schemas import CreateProductDiscountParams, ReadProductDiscountParams, UpdateProductDiscountParams

_PRODUCT_DISCOUNT_TOOLS = [
    ToolDefinition(
        method="read_product_discount",
        name="Read Product Discount",
        description="Read or list product discounts. Provide an id or key to fetch a specific discount, or omit both to list discounts.",
        parameters=ReadProductDiscountParams,
        handler=read_product_discount,
        actions={"product_discount": {"read": True}},
    ),
    ToolDefinition(
        method="create_product_discount",
        name="Create Product Discount",
        description="Create a new product discount with a name, value, predicate, and sort order.",
        parameters=CreateProductDiscountParams,
        handler=create_product_discount,
        actions={"product_discount": {"create": True}},
    ),
    ToolDefinition(
        method="update_product_discount",
        name="Update Product Discount",
        description="Apply update actions to an existing product discount identified by id or key.",
        parameters=UpdateProductDiscountParams,
        handler=update_product_discount,
        actions={"product_discount": {"update": True}},
    ),
]

for _tool in _PRODUCT_DISCOUNT_TOOLS:
    register_tool(_tool)
