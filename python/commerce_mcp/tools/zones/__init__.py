from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_zone, read_zone, update_zone
from .schemas import CreateZoneParams, ReadZoneParams, UpdateZoneParams
from .prompts import CREATE_ZONE_PROMPT, READ_ZONE_PROMPT, UPDATE_ZONE_PROMPT

_ZONES_TOOLS = [
    ToolDefinition(
        method="read_zone",
        name="Read Zone",
        description=READ_ZONE_PROMPT,
        parameters=ReadZoneParams,
        handler=read_zone,
        actions={"zones": {"read": True}},
    ),
    ToolDefinition(
        method="create_zone",
        name="Create Zone",
        description=CREATE_ZONE_PROMPT,
        parameters=CreateZoneParams,
        handler=create_zone,
        actions={"zones": {"create": True}},
    ),
    ToolDefinition(
        method="update_zone",
        name="Update Zone",
        description=UPDATE_ZONE_PROMPT,
        parameters=UpdateZoneParams,
        handler=update_zone,
        actions={"zones": {"update": True}},
    ),
]

for _tool in _ZONES_TOOLS:
    register_tool(_tool)
