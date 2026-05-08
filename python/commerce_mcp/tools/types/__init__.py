from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_type, read_type, update_type
from .schemas import CreateTypeParams, ReadTypeParams, UpdateTypeParams

_TYPES_TOOLS = [
    ToolDefinition(
        method="read_type",
        name="Read Type",
        description="Read or list custom types. Provide an id or key to fetch a specific type, or omit both to list types with optional filtering.",
        parameters=ReadTypeParams,
        handler=read_type,
        actions={"types": {"read": True}},
    ),
    ToolDefinition(
        method="create_type",
        name="Create Type",
        description="Create a new custom type with field definitions for extending Commercetools resources.",
        parameters=CreateTypeParams,
        handler=create_type,
        actions={"types": {"create": True}},
    ),
    ToolDefinition(
        method="update_type",
        name="Update Type",
        description="Apply update actions to an existing custom type identified by id or key.",
        parameters=UpdateTypeParams,
        handler=update_type,
        actions={"types": {"update": True}},
    ),
]

for _tool in _TYPES_TOOLS:
    register_tool(_tool)
