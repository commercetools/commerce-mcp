"""Products namespace — reference implementation.

Every namespace follows the same pattern:
  schemas.py  — Pydantic input models
  functions.py — async handler functions (no framework dependency)
  __init__.py  — ToolDefinition declarations + register_tool() calls

build_server() in server.py reads the registry and wires everything
into FastMCP automatically — no @mcp.tool() decorators here.
"""
from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ListProductsParams, CreateProductParams, UpdateProductParams
from .functions import list_products, create_product, update_product
from .prompts import CREATE_PRODUCT_PROMPT, LIST_PRODUCTS_PROMPT, UPDATE_PRODUCT_PROMPT

_PRODUCTS_TOOLS = [
    ToolDefinition(
        method="list_products",
        name="List Products",
        description=LIST_PRODUCTS_PROMPT,
        parameters=ListProductsParams,
        handler=list_products,
        actions={"products": {"read": True}},
    ),
    ToolDefinition(
        method="create_product",
        name="Create Product",
        description=CREATE_PRODUCT_PROMPT,
        parameters=CreateProductParams,
        handler=create_product,
        actions={"products": {"create": True}},
    ),
    ToolDefinition(
        method="update_product",
        name="Update Product",
        description=UPDATE_PRODUCT_PROMPT,
        parameters=UpdateProductParams,
        handler=update_product,
        actions={"products": {"update": True}},
    ),
]

for _tool in _PRODUCTS_TOOLS:
    register_tool(_tool)
