from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadShoppingListParams, CreateShoppingListParams, UpdateShoppingListParams
from .functions import read_shopping_list, create_shopping_list, update_shopping_list
from .prompts import CREATE_SHOPPING_LIST_PROMPT, READ_SHOPPING_LIST_PROMPT, UPDATE_SHOPPING_LIST_PROMPT

_TOOLS = [
    ToolDefinition(
        method="read_shopping_list",
        name="Read Shopping List",
        description=READ_SHOPPING_LIST_PROMPT,
        parameters=ReadShoppingListParams,
        handler=read_shopping_list,
        actions={"shopping_lists": {"read": True}},
    ),
    ToolDefinition(
        method="create_shopping_list",
        name="Create Shopping List",
        description=CREATE_SHOPPING_LIST_PROMPT,
        parameters=CreateShoppingListParams,
        handler=create_shopping_list,
        actions={"shopping_lists": {"create": True}},
    ),
    ToolDefinition(
        method="update_shopping_list",
        name="Update Shopping List",
        description=UPDATE_SHOPPING_LIST_PROMPT,
        parameters=UpdateShoppingListParams,
        handler=update_shopping_list,
        actions={"shopping_lists": {"update": True}},
    ),
]

for _tool in _TOOLS:
    register_tool(_tool)
