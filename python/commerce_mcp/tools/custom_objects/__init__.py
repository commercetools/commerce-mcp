from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_custom_object, read_custom_object, update_custom_object
from .schemas import CreateCustomObjectParams, ReadCustomObjectParams, UpdateCustomObjectParams

_CUSTOM_OBJECTS_TOOLS = [
    ToolDefinition(
        method="read_custom_object",
        name="Read Custom Object",
        description="Read custom objects. Provide container+key for a single object, container only to list all in that container, or omit both to list all custom objects.",
        parameters=ReadCustomObjectParams,
        handler=read_custom_object,
        actions={"custom_objects": {"read": True}},
    ),
    ToolDefinition(
        method="create_custom_object",
        name="Create Custom Object",
        description="Create or overwrite a custom object identified by container and key. If the object exists, pass a version to use optimistic locking.",
        parameters=CreateCustomObjectParams,
        handler=create_custom_object,
        actions={"custom_objects": {"create": True}},
    ),
    ToolDefinition(
        method="update_custom_object",
        name="Update Custom Object",
        description="Update an existing custom object's value identified by container and key.",
        parameters=UpdateCustomObjectParams,
        handler=update_custom_object,
        actions={"custom_objects": {"update": True}},
    ),
]

for _tool in _CUSTOM_OBJECTS_TOOLS:
    register_tool(_tool)
