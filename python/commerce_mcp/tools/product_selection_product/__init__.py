from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadProductSelectionProductParams
from .functions import read_product_selection_product

_PRODUCT_SELECTION_PRODUCT_TOOLS = [
    ToolDefinition(
        method="read_product_selection_product",
        name="Read Product Selection Product",
        description=(
            "Fetch products assigned to a commercetools Product Selection by selection ID or key. "
            "Returns AssignedProductPagedQueryResponse with product references and optional variant selection/exclusion. "
            "Available for admin and store contexts."
        ),
        parameters=ReadProductSelectionProductParams,
        handler=read_product_selection_product,
        actions={"product-selection-product": {"read": True}},
    ),
]

for _tool in _PRODUCT_SELECTION_PRODUCT_TOOLS:
    register_tool(_tool)
