from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import read_tax_category, create_tax_category, update_tax_category
from .schemas import ReadTaxCategoryParams, CreateTaxCategoryParams, UpdateTaxCategoryParams

_TAX_CATEGORY_TOOLS = [
    ToolDefinition(
        method="read_tax_category",
        name="Read Tax Category",
        description=(
            "Read or list tax categories. Provide an id or key to fetch a specific tax category, "
            "or omit both to list tax categories with optional filtering, sorting, and pagination. "
            "Admin-only operation."
        ),
        parameters=ReadTaxCategoryParams,
        handler=read_tax_category,
        actions={"tax_category": {"read": True}},
    ),
    ToolDefinition(
        method="create_tax_category",
        name="Create Tax Category",
        description=(
            "Create a new tax category with a name, optional key, description, and tax rates. "
            "Each rate requires a name, amount (decimal, e.g. 0.19 for 19%), and country code. "
            "Admin-only operation."
        ),
        parameters=CreateTaxCategoryParams,
        handler=create_tax_category,
        actions={"tax_category": {"create": True}},
    ),
    ToolDefinition(
        method="update_tax_category",
        name="Update Tax Category",
        description=(
            "Apply update actions to an existing tax category identified by id or key. "
            "Supported actions include: changeName, setDescription, addTaxRate, removeTaxRate, "
            "replaceTaxRate, setKey, setCustomType, setCustomField. Admin-only operation."
        ),
        parameters=UpdateTaxCategoryParams,
        handler=update_tax_category,
        actions={"tax_category": {"update": True}},
    ),
]

for _tool in _TAX_CATEGORY_TOOLS:
    register_tool(_tool)
