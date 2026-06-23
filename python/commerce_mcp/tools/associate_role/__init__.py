from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadAssociateRoleParams, CreateAssociateRoleParams, UpdateAssociateRoleParams
from .functions import read_associate_role, create_associate_role, update_associate_role

_ASSOCIATE_ROLE_TOOLS = [
    ToolDefinition(
        method="read_associate_role",
        name="Read Associate Role",
        description=(
            "Fetch a commercetools Associate Role by ID, key, or query predicates. "
            "Associate Roles define permission sets assignable to Associates within a Business Unit. "
            "Available for admin and associate (read-only) contexts."
        ),
        parameters=ReadAssociateRoleParams,
        handler=read_associate_role,
        actions={"associate-role": {"read": True}},
    ),
    ToolDefinition(
        method="create_associate_role",
        name="Create Associate Role",
        description=(
            "Create a new commercetools Associate Role with a key, buyerAssignable flag, and optional permissions. "
            "Admin context only."
        ),
        parameters=CreateAssociateRoleParams,
        handler=create_associate_role,
        actions={"associate-role": {"create": True}},
    ),
    ToolDefinition(
        method="update_associate_role",
        name="Update Associate Role",
        description=(
            "Apply update actions to a commercetools Associate Role identified by ID or key. "
            "Supported actions: addPermission, removePermission, setPermissions, changeBuyerAssignable, setName, setCustomField, setCustomType. "
            "Admin context only."
        ),
        parameters=UpdateAssociateRoleParams,
        handler=update_associate_role,
        actions={"associate-role": {"update": True}},
    ),
]

for _tool in _ASSOCIATE_ROLE_TOOLS:
    register_tool(_tool)
