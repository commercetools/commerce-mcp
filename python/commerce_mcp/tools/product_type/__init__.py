from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import read_product_type, create_product_type, update_product_type
from .schemas import ReadProductTypeParams, CreateProductTypeParams, UpdateProductTypeParams
from .prompts import CREATE_PRODUCT_TYPE_PROMPT, READ_PRODUCT_TYPE_PROMPT, UPDATE_PRODUCT_TYPE_PROMPT

_PRODUCT_TYPE_TOOLS = [
    ToolDefinition(
        method="read_product_type",
        name="Read Product Type",
        description=READ_PRODUCT_TYPE_PROMPT,
        parameters=ReadProductTypeParams,
        handler=read_product_type,
        actions={"product_type": {"read": True}},
    ),
    ToolDefinition(
        method="create_product_type",
        name="Create Product Type",
        description=CREATE_PRODUCT_TYPE_PROMPT,
        parameters=CreateProductTypeParams,
        handler=create_product_type,
        actions={"product_type": {"create": True}},
    ),
    ToolDefinition(
        method="update_product_type",
        name="Update Product Type",
        description=UPDATE_PRODUCT_TYPE_PROMPT,
        parameters=UpdateProductTypeParams,
        handler=update_product_type,
        actions={"product_type": {"update": True}},
    ),
]

for _tool in _PRODUCT_TYPE_TOOLS:
    register_tool(_tool)
