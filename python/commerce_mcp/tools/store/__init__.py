from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import CreateStoreParams, ReadStoreParams, UpdateStoreParams
from .functions import create_store, read_store, update_store
from .prompts import CREATE_STORE_PROMPT, READ_STORE_PROMPT, UPDATE_STORE_PROMPT

_STORE_TOOLS = [
    ToolDefinition(
        method="read_store",
        name="Read Store",
        description=READ_STORE_PROMPT,
        parameters=ReadStoreParams,
        handler=read_store,
        actions={"store": {"read": True}},
    ),
    ToolDefinition(
        method="create_store",
        name="Create Store",
        description=CREATE_STORE_PROMPT,
        parameters=CreateStoreParams,
        handler=create_store,
        actions={"store": {"create": True}},
    ),
    ToolDefinition(
        method="update_store",
        name="Update Store",
        description=UPDATE_STORE_PROMPT,
        parameters=UpdateStoreParams,
        handler=update_store,
        actions={"store": {"update": True}},
    ),
]

for _tool in _STORE_TOOLS:
    register_tool(_tool)
