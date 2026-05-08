from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import bulk_create, bulk_update
from .schemas import BulkCreateParams, BulkUpdateParams

_BULK_TOOLS = [
    ToolDefinition(
        method="bulk_create",
        name="Bulk Create",
        description="Create multiple entities in parallel. Provide a list of items each with an entityType and data.",
        parameters=BulkCreateParams,
        handler=bulk_create,
        actions={"bulk": {"create": True}},
    ),
    ToolDefinition(
        method="bulk_update",
        name="Bulk Update",
        description="Update multiple entities in parallel. Provide a list of items each with an entityType and data (must include version and actions).",
        parameters=BulkUpdateParams,
        handler=bulk_update,
        actions={"bulk": {"update": True}},
    ),
]

for _tool in _BULK_TOOLS:
    register_tool(_tool)
