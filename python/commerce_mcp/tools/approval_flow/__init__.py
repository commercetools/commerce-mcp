from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadApprovalFlowParams, UpdateApprovalFlowParams
from .functions import read_approval_flow, update_approval_flow

_APPROVAL_FLOW_TOOLS = [
    ToolDefinition(
        method="read_approval_flow",
        name="Read Approval Flow",
        description=(
            "Fetch a commercetools Approval Flow by ID or query predicates. "
            "Approval Flows represent the approval process for Orders, linking them to the Approval Rules that triggered the requirement. "
            "Available for admin context (requires associateId + businessUnitKey params) "
            "and associate context (customerId + businessUnitKey taken from session)."
        ),
        parameters=ReadApprovalFlowParams,
        handler=read_approval_flow,
        actions={"approval-flow": {"read": True}},
    ),
    ToolDefinition(
        method="update_approval_flow",
        name="Update Approval Flow",
        description=(
            "Apply update actions to a commercetools Approval Flow. "
            "Supported actions: approve, reject, setCustomField, setCustomType. "
            "Available for admin context (requires associateId + businessUnitKey params) "
            "and associate context (customerId + businessUnitKey taken from session)."
        ),
        parameters=UpdateApprovalFlowParams,
        handler=update_approval_flow,
        actions={"approval-flow": {"update": True}},
    ),
]

for _tool in _APPROVAL_FLOW_TOOLS:
    register_tool(_tool)
