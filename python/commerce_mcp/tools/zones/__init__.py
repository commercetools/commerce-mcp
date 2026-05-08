from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_zone, read_zone, update_zone
from .schemas import CreateZoneParams, ReadZoneParams, UpdateZoneParams

_ZONES_TOOLS = [
    ToolDefinition(
        method="read_zone",
        name="Read Zone",
        description="Read or list zones. Provide an id or key to fetch a specific zone, or omit both to list zones with optional filtering.",
        parameters=ReadZoneParams,
        handler=read_zone,
        actions={"zones": {"read": True}},
    ),
    ToolDefinition(
        method="create_zone",
        name="Create Zone",
        description="Create a new zone with a name, optional key, description, and locations.",
        parameters=CreateZoneParams,
        handler=create_zone,
        actions={"zones": {"create": True}},
    ),
    ToolDefinition(
        method="update_zone",
        name="Update Zone",
        description="Apply update actions to an existing zone identified by id or key.",
        parameters=UpdateZoneParams,
        handler=update_zone,
        actions={"zones": {"update": True}},
    ),
]

for _tool in _ZONES_TOOLS:
    register_tool(_tool)
