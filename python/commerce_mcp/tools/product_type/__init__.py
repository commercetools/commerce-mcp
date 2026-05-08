from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import read_product_type, create_product_type, update_product_type
from .schemas import ReadProductTypeParams, CreateProductTypeParams, UpdateProductTypeParams

_PRODUCT_TYPE_TOOLS = [
    ToolDefinition(
        method="read_product_type",
        name="Read Product Type",
        description=(
            "Read a single product type by its ID, or list product types with optional filtering, "
            "sorting, and pagination. Provide an id to fetch a specific product type, or omit it "
            "to list all product types. Available to all contexts."
        ),
        parameters=ReadProductTypeParams,
        handler=read_product_type,
        actions={"product_type": {"read": True}},
    ),
    ToolDefinition(
        method="create_product_type",
        name="Create Product Type",
        description=(
            "Create a new product type with a key, name, description, and optional attribute "
            "definitions. Each attribute requires a name, label, and type definition. "
            "Admin-only operation."
        ),
        parameters=CreateProductTypeParams,
        handler=create_product_type,
        actions={"product_type": {"create": True}},
    ),
    ToolDefinition(
        method="update_product_type",
        name="Update Product Type",
        description=(
            "Apply update actions to an existing product type identified by its ID. "
            "Supported actions include: addAttributeDefinition, removeAttributeDefinition, "
            "changeName, changeDescription, changeAttributeOrder, setKey, and more. "
            "Admin-only operation."
        ),
        parameters=UpdateProductTypeParams,
        handler=update_product_type,
        actions={"product_type": {"update": True}},
    ),
]

for _tool in _PRODUCT_TYPE_TOOLS:
    register_tool(_tool)
