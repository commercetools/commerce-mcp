from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_standalone_price, read_standalone_price, update_standalone_price
from .schemas import CreateStandalonePriceParams, ReadStandalonePriceParams, UpdateStandalonePriceParams
from .prompts import CREATE_STANDALONE_PRICE_PROMPT, READ_STANDALONE_PRICE_PROMPT, UPDATE_STANDALONE_PRICE_PROMPT

_STANDALONE_PRICE_TOOLS = [
    ToolDefinition(
        method="read_standalone_price",
        name="Read Standalone Price",
        description=READ_STANDALONE_PRICE_PROMPT,
        parameters=ReadStandalonePriceParams,
        handler=read_standalone_price,
        actions={"standalone_price": {"read": True}},
    ),
    ToolDefinition(
        method="create_standalone_price",
        name="Create Standalone Price",
        description=CREATE_STANDALONE_PRICE_PROMPT,
        parameters=CreateStandalonePriceParams,
        handler=create_standalone_price,
        actions={"standalone_price": {"create": True}},
    ),
    ToolDefinition(
        method="update_standalone_price",
        name="Update Standalone Price",
        description=UPDATE_STANDALONE_PRICE_PROMPT,
        parameters=UpdateStandalonePriceParams,
        handler=update_standalone_price,
        actions={"standalone_price": {"update": True}},
    ),
]

for _tool in _STANDALONE_PRICE_TOOLS:
    register_tool(_tool)
