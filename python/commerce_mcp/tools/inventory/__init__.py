from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_inventory, read_inventory, update_inventory
from .prompts import CREATE_INVENTORY_PROMPT, READ_INVENTORY_PROMPT, UPDATE_INVENTORY_PROMPT
from .schemas import CreateInventoryParams, ReadInventoryParams, UpdateInventoryParams

_INVENTORY_TOOLS = [
    ToolDefinition(
        method="read_inventory",
        name="Read Inventory",
        description=READ_INVENTORY_PROMPT,
        parameters=ReadInventoryParams,
        handler=read_inventory,
        actions={"inventory": {"read": True}},
    ),
    ToolDefinition(
        method="create_inventory",
        name="Create Inventory",
        description=CREATE_INVENTORY_PROMPT,
        parameters=CreateInventoryParams,
        handler=create_inventory,
        actions={"inventory": {"create": True}},
    ),
    ToolDefinition(
        method="update_inventory",
        name="Update Inventory",
        description=UPDATE_INVENTORY_PROMPT,
        parameters=UpdateInventoryParams,
        handler=update_inventory,
        actions={"inventory": {"update": True}},
    ),
]

for _tool in _INVENTORY_TOOLS:
    register_tool(_tool)
