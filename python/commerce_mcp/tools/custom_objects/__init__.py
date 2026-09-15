from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_custom_object, read_custom_object, update_custom_object
from .prompts import CREATE_CUSTOM_OBJECT_PROMPT, READ_CUSTOM_OBJECT_PROMPT, UPDATE_CUSTOM_OBJECT_PROMPT
from .schemas import CreateCustomObjectParams, ReadCustomObjectParams, UpdateCustomObjectParams

_CUSTOM_OBJECTS_TOOLS = [
    ToolDefinition(
        method="read_custom_object",
        name="Read Custom Object",
        description=READ_CUSTOM_OBJECT_PROMPT,
        parameters=ReadCustomObjectParams,
        handler=read_custom_object,
        actions={"custom_objects": {"read": True}},
    ),
    ToolDefinition(
        method="create_custom_object",
        name="Create Custom Object",
        description=CREATE_CUSTOM_OBJECT_PROMPT,
        parameters=CreateCustomObjectParams,
        handler=create_custom_object,
        actions={"custom_objects": {"create": True}},
    ),
    ToolDefinition(
        method="update_custom_object",
        name="Update Custom Object",
        description=UPDATE_CUSTOM_OBJECT_PROMPT,
        parameters=UpdateCustomObjectParams,
        handler=update_custom_object,
        actions={"custom_objects": {"update": True}},
    ),
]

for _tool in _CUSTOM_OBJECTS_TOOLS:
    register_tool(_tool)
