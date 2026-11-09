from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadProductSelectionProductParams
from .functions import read_product_selection_product
from .prompts import READ_PRODUCT_SELECTION_PRODUCT_PROMPT

_PRODUCT_SELECTION_PRODUCT_TOOLS = [
    ToolDefinition(
        method="read_product_selection_product",
        name="Read Product Selection Product",
        description=READ_PRODUCT_SELECTION_PRODUCT_PROMPT,
        parameters=ReadProductSelectionProductParams,
        handler=read_product_selection_product,
        actions={"product-selection-product": {"read": True}},
    ),
]

for _tool in _PRODUCT_SELECTION_PRODUCT_TOOLS:
    register_tool(_tool)
