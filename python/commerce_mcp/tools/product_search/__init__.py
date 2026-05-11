from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import search_products
from .schemas import SearchProductsParams
from .prompts import SEARCH_PRODUCTS_PROMPT

_PRODUCT_SEARCH_TOOLS = [
    ToolDefinition(
        method="search_products",
        name="Search Products",
        description=SEARCH_PRODUCTS_PROMPT,
        parameters=SearchProductsParams,
        handler=search_products,
        actions={"product_search": {"read": True}},
    ),
]

for _tool in _PRODUCT_SEARCH_TOOLS:
    register_tool(_tool)
