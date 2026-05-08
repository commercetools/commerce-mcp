from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadShoppingListParams, CreateShoppingListParams, UpdateShoppingListParams
from .functions import read_shopping_list, create_shopping_list, update_shopping_list

_TOOLS = [
    ToolDefinition(
        method="read_shopping_list",
        name="Read Shopping List",
        description=(
            "Fetch a commercetools shopping list by ID, key, or query predicates. "
            "Routes to customer (/me/shopping-lists), store (/in-store/key={storeKey}/shopping-lists), "
            "or admin (/shopping-lists) scope based on context."
        ),
        parameters=ReadShoppingListParams,
        handler=read_shopping_list,
        actions={"shopping_lists": {"read": True}},
    ),
    ToolDefinition(
        method="create_shopping_list",
        name="Create Shopping List",
        description=(
            "Create a new commercetools shopping list. "
            "Routes to customer (/me/shopping-lists), store (/in-store/key={storeKey}/shopping-lists), "
            "or admin (/shopping-lists) scope based on context."
        ),
        parameters=CreateShoppingListParams,
        handler=create_shopping_list,
        actions={"shopping_lists": {"create": True}},
    ),
    ToolDefinition(
        method="update_shopping_list",
        name="Update Shopping List",
        description=(
            "Apply update actions to an existing commercetools shopping list identified by ID or key. "
            "Routes to customer (/me/shopping-lists), store (/in-store/key={storeKey}/shopping-lists), "
            "or admin (/shopping-lists) scope based on context."
        ),
        parameters=UpdateShoppingListParams,
        handler=update_shopping_list,
        actions={"shopping_lists": {"update": True}},
    ),
]

for _tool in _TOOLS:
    register_tool(_tool)
