from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_extension, read_extension, update_extension
from .schemas import CreateExtensionParams, ReadExtensionParams, UpdateExtensionParams

_EXTENSIONS_TOOLS = [
    ToolDefinition(
        method="read_extension",
        name="Read Extension",
        description="Read or list API extensions. Provide an id or key to fetch a specific extension, or omit both to list extensions.",
        parameters=ReadExtensionParams,
        handler=read_extension,
        actions={"extensions": {"read": True}},
    ),
    ToolDefinition(
        method="create_extension",
        name="Create Extension",
        description="Create a new API extension with triggers and a destination (HTTP, AWS Lambda, or Google Cloud Function).",
        parameters=CreateExtensionParams,
        handler=create_extension,
        actions={"extensions": {"create": True}},
    ),
    ToolDefinition(
        method="update_extension",
        name="Update Extension",
        description="Apply update actions to an existing API extension identified by id or key.",
        parameters=UpdateExtensionParams,
        handler=update_extension,
        actions={"extensions": {"update": True}},
    ),
]

for _tool in _EXTENSIONS_TOOLS:
    register_tool(_tool)
