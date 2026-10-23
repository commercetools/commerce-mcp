from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadRecurrencePolicyParams, CreateRecurrencePolicyParams, UpdateRecurrencePolicyParams
from .functions import read_recurrence_policy, create_recurrence_policy, update_recurrence_policy

_RECURRENCE_POLICY_TOOLS = [
    ToolDefinition(
        method="read_recurrence_policy",
        name="Read Recurrence Policy",
        description=(
            "Fetch a commercetools Recurrence Policy by ID, key, or query predicates. "
            "Recurrence Policies define the schedule for recurring orders. "
            "Admin context only."
        ),
        parameters=ReadRecurrencePolicyParams,
        handler=read_recurrence_policy,
        actions={"recurrence-policy": {"read": True}},
    ),
    ToolDefinition(
        method="create_recurrence_policy",
        name="Create Recurrence Policy",
        description=(
            "Create a new commercetools Recurrence Policy. "
            "Specify a schedule (standard interval or day-of-month) and an optional localized name and description. "
            "Admin context only."
        ),
        parameters=CreateRecurrencePolicyParams,
        handler=create_recurrence_policy,
        actions={"recurrence-policy": {"create": True}},
    ),
    ToolDefinition(
        method="update_recurrence_policy",
        name="Update Recurrence Policy",
        description=(
            "Apply update actions to a commercetools Recurrence Policy identified by ID or key. "
            "Supported actions: setKey, setName, setDescription, setSchedule. "
            "Admin context only."
        ),
        parameters=UpdateRecurrencePolicyParams,
        handler=update_recurrence_policy,
        actions={"recurrence-policy": {"update": True}},
    ),
]

for _tool in _RECURRENCE_POLICY_TOOLS:
    register_tool(_tool)
