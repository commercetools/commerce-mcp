from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_business_unit, read_business_unit, update_business_unit
from .schemas import CreateBusinessUnitParams, ReadBusinessUnitParams, UpdateBusinessUnitParams

_BUSINESS_UNIT_TOOLS = [
    ToolDefinition(
        method="read_business_unit",
        name="Read Business Unit",
        description=(
            "Fetch information about a commercetools business unit. "
            "Provide an id or key to fetch a specific business unit, or omit both to list "
            "business units with optional filtering. Supports store-scoped and admin access."
        ),
        parameters=ReadBusinessUnitParams,
        handler=read_business_unit,
        actions={"business_unit": {"read": True}},
    ),
    ToolDefinition(
        method="create_business_unit",
        name="Create Business Unit",
        description=(
            "Create a new Business Unit in commercetools. "
            "Requires key, name, and unitType (Company or Division). "
            "Supports store-scoped and admin access."
        ),
        parameters=CreateBusinessUnitParams,
        handler=create_business_unit,
        actions={"business_unit": {"create": True}},
    ),
    ToolDefinition(
        method="update_business_unit",
        name="Update Business Unit",
        description=(
            "Update a Business Unit in commercetools using update actions. "
            "Requires either id or key, and an array of update actions. "
            "Version is fetched automatically if not provided. "
            "Supports store-scoped and admin access."
        ),
        parameters=UpdateBusinessUnitParams,
        handler=update_business_unit,
        actions={"business_unit": {"update": True}},
    ),
]

for _tool in _BUSINESS_UNIT_TOOLS:
    register_tool(_tool)
