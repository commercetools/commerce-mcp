from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import bulk_create, bulk_update
from .prompts import CREATE_BULK_DESCRIPTION, UPDATE_BULK_DESCRIPTION
from .schemas import BulkCreateParams, BulkUpdateParams

_BULK_TOOLS = [
    ToolDefinition(
        method="bulk_create",
        name="Bulk Create",
        description=CREATE_BULK_DESCRIPTION,
        parameters=BulkCreateParams,
        handler=bulk_create,
        actions={"bulk": {"create": True}},
    ),
    ToolDefinition(
        method="bulk_update",
        name="Bulk Update",
        description=UPDATE_BULK_DESCRIPTION,
        parameters=BulkUpdateParams,
        handler=bulk_update,
        actions={"bulk": {"update": True}},
    ),
]

for _tool in _BULK_TOOLS:
    register_tool(_tool)
