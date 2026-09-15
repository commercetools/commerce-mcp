from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_product_selection, read_product_selection, update_product_selection
from .schemas import CreateProductSelectionParams, ReadProductSelectionParams, UpdateProductSelectionParams
from .prompts import CREATE_PRODUCT_SELECTION_PROMPT, READ_PRODUCT_SELECTION_PROMPT, UPDATE_PRODUCT_SELECTION_PROMPT

_PRODUCT_SELECTION_TOOLS = [
    ToolDefinition(
        method="read_product_selection",
        name="Read Product Selection",
        description=READ_PRODUCT_SELECTION_PROMPT,
        parameters=ReadProductSelectionParams,
        handler=read_product_selection,
        actions={"product_selection": {"read": True}},
    ),
    ToolDefinition(
        method="create_product_selection",
        name="Create Product Selection",
        description=CREATE_PRODUCT_SELECTION_PROMPT,
        parameters=CreateProductSelectionParams,
        handler=create_product_selection,
        actions={"product_selection": {"create": True}},
    ),
    ToolDefinition(
        method="update_product_selection",
        name="Update Product Selection",
        description=UPDATE_PRODUCT_SELECTION_PROMPT,
        parameters=UpdateProductSelectionParams,
        handler=update_product_selection,
        actions={"product_selection": {"update": True}},
    ),
]

for _tool in _PRODUCT_SELECTION_TOOLS:
    register_tool(_tool)
