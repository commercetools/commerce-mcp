from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import CreateCategoryParams, ReadCategoryParams, UpdateCategoryParams
from .functions import create_category, read_category, update_category

_CATEGORY_TOOLS = [
    ToolDefinition(
        method="read_category",
        name="Read Category",
        description=(
            "Fetch a commercetools category by ID, key, or list with optional filtering and sorting. "
            "Available in all contexts (no authentication context required for reading)."
        ),
        parameters=ReadCategoryParams,
        handler=read_category,
        actions={"category": {"read": True}},
    ),
    ToolDefinition(
        method="create_category",
        name="Create Category",
        description=(
            "Create a new commercetools category with a localized name, slug, and optional parent, "
            "order hint, assets, and custom fields. Requires isAdmin context."
        ),
        parameters=CreateCategoryParams,
        handler=create_category,
        actions={"category": {"create": True}},
    ),
    ToolDefinition(
        method="update_category",
        name="Update Category",
        description=(
            "Apply update actions to an existing commercetools category identified by ID or key. "
            "Requires isAdmin context."
        ),
        parameters=UpdateCategoryParams,
        handler=update_category,
        actions={"category": {"update": True}},
    ),
]

for _tool in _CATEGORY_TOOLS:
    register_tool(_tool)
