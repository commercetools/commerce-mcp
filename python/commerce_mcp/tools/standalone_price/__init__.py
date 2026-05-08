from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_standalone_price, read_standalone_price, update_standalone_price
from .schemas import CreateStandalonePriceParams, ReadStandalonePriceParams, UpdateStandalonePriceParams

_STANDALONE_PRICE_TOOLS = [
    ToolDefinition(
        method="read_standalone_price",
        name="Read Standalone Price",
        description="Read or list standalone prices. Provide an id or key to fetch a specific price, or omit both to list prices with optional filtering.",
        parameters=ReadStandalonePriceParams,
        handler=read_standalone_price,
        actions={"standalone_price": {"read": True}},
    ),
    ToolDefinition(
        method="create_standalone_price",
        name="Create Standalone Price",
        description="Create a new standalone price for a product variant SKU.",
        parameters=CreateStandalonePriceParams,
        handler=create_standalone_price,
        actions={"standalone_price": {"create": True}},
    ),
    ToolDefinition(
        method="update_standalone_price",
        name="Update Standalone Price",
        description="Apply update actions to an existing standalone price identified by id or key.",
        parameters=UpdateStandalonePriceParams,
        handler=update_standalone_price,
        actions={"standalone_price": {"update": True}},
    ),
]

for _tool in _STANDALONE_PRICE_TOOLS:
    register_tool(_tool)
