from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import CreateStoreParams, ReadStoreParams, UpdateStoreParams
from .functions import create_store, read_store, update_store

_STORE_TOOLS = [
    ToolDefinition(
        method="read_store",
        name="Read Store",
        description=(
            "Fetch a commercetools store by ID, key, or list with optional filtering. "
            "In store context only reads the store's own record. "
            "Requires isAdmin or storeKey context."
        ),
        parameters=ReadStoreParams,
        handler=read_store,
        actions={"store": {"read": True}},
    ),
    ToolDefinition(
        method="create_store",
        name="Create Store",
        description=(
            "Create a new commercetools store with a key, localized name, languages, countries, "
            "distribution channels, supply channels, product selections, and custom fields. "
            "Requires isAdmin context."
        ),
        parameters=CreateStoreParams,
        handler=create_store,
        actions={"store": {"create": True}},
    ),
    ToolDefinition(
        method="update_store",
        name="Update Store",
        description=(
            "Apply update actions to an existing commercetools store. "
            "In store context updates only the store's own record. "
            "Admin context allows updating any store by ID or key. "
            "Requires isAdmin or storeKey context."
        ),
        parameters=UpdateStoreParams,
        handler=update_store,
        actions={"store": {"update": True}},
    ),
]

for _tool in _STORE_TOOLS:
    register_tool(_tool)
