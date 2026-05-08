from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_product_selection, read_product_selection, update_product_selection
from .schemas import CreateProductSelectionParams, ReadProductSelectionParams, UpdateProductSelectionParams

_PRODUCT_SELECTION_TOOLS = [
    ToolDefinition(
        method="read_product_selection",
        name="Read Product Selection",
        description="Read or list product selections. Provide an id or key to fetch a specific selection, or omit both to list selections.",
        parameters=ReadProductSelectionParams,
        handler=read_product_selection,
        actions={"product_selection": {"read": True}},
    ),
    ToolDefinition(
        method="create_product_selection",
        name="Create Product Selection",
        description="Create a new product selection with a localized name and optional mode (Individual or IndividualExclusion).",
        parameters=CreateProductSelectionParams,
        handler=create_product_selection,
        actions={"product_selection": {"create": True}},
    ),
    ToolDefinition(
        method="update_product_selection",
        name="Update Product Selection",
        description="Apply update actions to an existing product selection identified by id or key.",
        parameters=UpdateProductSelectionParams,
        handler=update_product_selection,
        actions={"product_selection": {"update": True}},
    ),
]

for _tool in _PRODUCT_SELECTION_TOOLS:
    register_tool(_tool)
