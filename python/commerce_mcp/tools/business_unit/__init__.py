from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_business_unit, read_business_unit, update_business_unit
from .prompts import CREATE_BUSINESS_UNIT_PROMPT, READ_BUSINESS_UNIT_PROMPT, UPDATE_BUSINESS_UNIT_PROMPT
from .schemas import CreateBusinessUnitParams, ReadBusinessUnitParams, UpdateBusinessUnitParams

_BUSINESS_UNIT_TOOLS = [
    ToolDefinition(
        method="read_business_unit",
        name="Read Business Unit",
        description=READ_BUSINESS_UNIT_PROMPT,
        parameters=ReadBusinessUnitParams,
        handler=read_business_unit,
        actions={"business_unit": {"read": True}},
    ),
    ToolDefinition(
        method="create_business_unit",
        name="Create Business Unit",
        description=CREATE_BUSINESS_UNIT_PROMPT,
        parameters=CreateBusinessUnitParams,
        handler=create_business_unit,
        actions={"business_unit": {"create": True}},
    ),
    ToolDefinition(
        method="update_business_unit",
        name="Update Business Unit",
        description=UPDATE_BUSINESS_UNIT_PROMPT,
        parameters=UpdateBusinessUnitParams,
        handler=update_business_unit,
        actions={"business_unit": {"update": True}},
    ),
]

for _tool in _BUSINESS_UNIT_TOOLS:
    register_tool(_tool)
