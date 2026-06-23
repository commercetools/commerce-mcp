from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import read_tax_category, create_tax_category, update_tax_category
from .schemas import ReadTaxCategoryParams, CreateTaxCategoryParams, UpdateTaxCategoryParams
from .prompts import CREATE_TAX_CATEGORY_PROMPT, READ_TAX_CATEGORY_PROMPT, UPDATE_TAX_CATEGORY_PROMPT

_TAX_CATEGORY_TOOLS = [
    ToolDefinition(
        method="read_tax_category",
        name="Read Tax Category",
        description=READ_TAX_CATEGORY_PROMPT,
        parameters=ReadTaxCategoryParams,
        handler=read_tax_category,
        actions={"tax_category": {"read": True}},
    ),
    ToolDefinition(
        method="create_tax_category",
        name="Create Tax Category",
        description=CREATE_TAX_CATEGORY_PROMPT,
        parameters=CreateTaxCategoryParams,
        handler=create_tax_category,
        actions={"tax_category": {"create": True}},
    ),
    ToolDefinition(
        method="update_tax_category",
        name="Update Tax Category",
        description=UPDATE_TAX_CATEGORY_PROMPT,
        parameters=UpdateTaxCategoryParams,
        handler=update_tax_category,
        actions={"tax_category": {"update": True}},
    ),
]

for _tool in _TAX_CATEGORY_TOOLS:
    register_tool(_tool)
