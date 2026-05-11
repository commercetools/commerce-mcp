from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .prompts import CREATE_CATEGORY_PROMPT, READ_CATEGORY_PROMPT, UPDATE_CATEGORY_PROMPT
from .schemas import CreateCategoryParams, ReadCategoryParams, UpdateCategoryParams
from .functions import create_category, read_category, update_category

_CATEGORY_TOOLS = [
    ToolDefinition(
        method="read_category",
        name="Read Category",
        description=READ_CATEGORY_PROMPT,
        parameters=ReadCategoryParams,
        handler=read_category,
        actions={"category": {"read": True}},
    ),
    ToolDefinition(
        method="create_category",
        name="Create Category",
        description=CREATE_CATEGORY_PROMPT,
        parameters=CreateCategoryParams,
        handler=create_category,
        actions={"category": {"create": True}},
    ),
    ToolDefinition(
        method="update_category",
        name="Update Category",
        description=UPDATE_CATEGORY_PROMPT,
        parameters=UpdateCategoryParams,
        handler=update_category,
        actions={"category": {"update": True}},
    ),
]

for _tool in _CATEGORY_TOOLS:
    register_tool(_tool)
