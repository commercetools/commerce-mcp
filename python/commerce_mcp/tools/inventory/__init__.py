from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_inventory, read_inventory, update_inventory
from .schemas import CreateInventoryParams, ReadInventoryParams, UpdateInventoryParams

_INVENTORY_TOOLS = [
    ToolDefinition(
        method="read_inventory",
        name="Read Inventory",
        description="Read or list inventory entries. Provide an id or key to fetch a specific entry, or omit both to list entries with optional filtering.",
        parameters=ReadInventoryParams,
        handler=read_inventory,
        actions={"inventory": {"read": True}},
    ),
    ToolDefinition(
        method="create_inventory",
        name="Create Inventory",
        description="Create a new inventory entry for a product variant SKU with an initial stock quantity.",
        parameters=CreateInventoryParams,
        handler=create_inventory,
        actions={"inventory": {"create": True}},
    ),
    ToolDefinition(
        method="update_inventory",
        name="Update Inventory",
        description="Apply update actions to an existing inventory entry identified by id or key.",
        parameters=UpdateInventoryParams,
        handler=update_inventory,
        actions={"inventory": {"update": True}},
    ),
]

for _tool in _INVENTORY_TOOLS:
    register_tool(_tool)
