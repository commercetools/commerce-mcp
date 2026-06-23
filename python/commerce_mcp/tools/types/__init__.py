from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_type, read_type, update_type
from .schemas import CreateTypeParams, ReadTypeParams, UpdateTypeParams
from .prompts import CREATE_TYPE_PROMPT, READ_TYPE_PROMPT, UPDATE_TYPE_PROMPT

_TYPES_TOOLS = [
    ToolDefinition(
        method="read_type",
        name="Read Type",
        description=READ_TYPE_PROMPT,
        parameters=ReadTypeParams,
        handler=read_type,
        actions={"types": {"read": True}},
    ),
    ToolDefinition(
        method="create_type",
        name="Create Type",
        description=CREATE_TYPE_PROMPT,
        parameters=CreateTypeParams,
        handler=create_type,
        actions={"types": {"create": True}},
    ),
    ToolDefinition(
        method="update_type",
        name="Update Type",
        description=UPDATE_TYPE_PROMPT,
        parameters=UpdateTypeParams,
        handler=update_type,
        actions={"types": {"update": True}},
    ),
]

for _tool in _TYPES_TOOLS:
    register_tool(_tool)
