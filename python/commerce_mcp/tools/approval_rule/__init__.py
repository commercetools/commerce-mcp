from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadApprovalRuleParams, CreateApprovalRuleParams, UpdateApprovalRuleParams
from .functions import read_approval_rule, create_approval_rule, update_approval_rule

_APPROVAL_RULE_TOOLS = [
    ToolDefinition(
        method="read_approval_rule",
        name="Read Approval Rule",
        description=(
            "Fetch a commercetools Approval Rule by ID, key, or query predicates. "
            "Approval Rules define when Orders in a Business Unit require approval and who must approve them. "
            "Available for admin context (requires associateId + businessUnitKey params) "
            "and associate context (customerId + businessUnitKey taken from session)."
        ),
        parameters=ReadApprovalRuleParams,
        handler=read_approval_rule,
        actions={"approval-rule": {"read": True}},
    ),
    ToolDefinition(
        method="create_approval_rule",
        name="Create Approval Rule",
        description=(
            "Create a new commercetools Approval Rule with a name, predicate, approver hierarchy, and requesters. "
            "Available for admin context (requires associateId + businessUnitKey params) "
            "and associate context (customerId + businessUnitKey taken from session)."
        ),
        parameters=CreateApprovalRuleParams,
        handler=create_approval_rule,
        actions={"approval-rule": {"create": True}},
    ),
    ToolDefinition(
        method="update_approval_rule",
        name="Update Approval Rule",
        description=(
            "Apply update actions to a commercetools Approval Rule identified by ID or key. "
            "Supported actions: setApprovers, setRequesters, setName, setDescription, setPredicate, setStatus, setKey, setCustomField, setCustomType. "
            "Available for admin context (requires associateId + businessUnitKey params) "
            "and associate context (customerId + businessUnitKey taken from session)."
        ),
        parameters=UpdateApprovalRuleParams,
        handler=update_approval_rule,
        actions={"approval-rule": {"update": True}},
    ),
]

for _tool in _APPROVAL_RULE_TOOLS:
    register_tool(_tool)
