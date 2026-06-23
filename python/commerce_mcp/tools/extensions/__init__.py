from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_extension, read_extension, update_extension
from .prompts import CREATE_EXTENSION_PROMPT, READ_EXTENSION_PROMPT, UPDATE_EXTENSION_PROMPT
from .schemas import CreateExtensionParams, ReadExtensionParams, UpdateExtensionParams

_EXTENSIONS_TOOLS = [
    ToolDefinition(
        method="read_extension",
        name="Read Extension",
        description=READ_EXTENSION_PROMPT,
        parameters=ReadExtensionParams,
        handler=read_extension,
        actions={"extensions": {"read": True}},
    ),
    ToolDefinition(
        method="create_extension",
        name="Create Extension",
        description=CREATE_EXTENSION_PROMPT,
        parameters=CreateExtensionParams,
        handler=create_extension,
        actions={"extensions": {"create": True}},
    ),
    ToolDefinition(
        method="update_extension",
        name="Update Extension",
        description=UPDATE_EXTENSION_PROMPT,
        parameters=UpdateExtensionParams,
        handler=update_extension,
        actions={"extensions": {"update": True}},
    ),
]

for _tool in _EXTENSIONS_TOOLS:
    register_tool(_tool)
