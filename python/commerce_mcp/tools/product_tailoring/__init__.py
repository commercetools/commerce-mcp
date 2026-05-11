from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import (
    ReadProductTailoringParams,
    CreateProductTailoringParams,
    UpdateProductTailoringParams,
)
from .functions import read_product_tailoring, create_product_tailoring, update_product_tailoring
from .prompts import CREATE_PRODUCT_TAILORING_PROMPT, READ_PRODUCT_TAILORING_PROMPT, UPDATE_PRODUCT_TAILORING_PROMPT

_PRODUCT_TAILORING_TOOLS = [
    ToolDefinition(
        method="read_product_tailoring",
        name="Read product tailoring",
        description=READ_PRODUCT_TAILORING_PROMPT,
        parameters=ReadProductTailoringParams,
        handler=read_product_tailoring,
        actions={"product_tailoring": {"read": True}},
    ),
    ToolDefinition(
        method="create_product_tailoring",
        name="Create product tailoring",
        description=CREATE_PRODUCT_TAILORING_PROMPT,
        parameters=CreateProductTailoringParams,
        handler=create_product_tailoring,
        actions={"product_tailoring": {"create": True}},
    ),
    ToolDefinition(
        method="update_product_tailoring",
        name="Update product tailoring",
        description=UPDATE_PRODUCT_TAILORING_PROMPT,
        parameters=UpdateProductTailoringParams,
        handler=update_product_tailoring,
        actions={"product_tailoring": {"update": True}},
    ),
]

for _tool in _PRODUCT_TAILORING_TOOLS:
    register_tool(_tool)
