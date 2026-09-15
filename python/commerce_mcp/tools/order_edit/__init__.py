from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadOrderEditParams, CreateOrderEditParams, UpdateOrderEditParams, ApplyOrderEditParams
from .functions import read_order_edit, create_order_edit, update_order_edit, apply_order_edit

_ORDER_EDIT_TOOLS = [
    ToolDefinition(
        method="read_order_edit",
        name="Read Order Edit",
        description=(
            "Fetch a commercetools Order Edit by ID, key, or query predicates. "
            "Order Edits capture staged modifications to existing Orders before they are applied. "
            "Admin context only."
        ),
        parameters=ReadOrderEditParams,
        handler=read_order_edit,
        actions={"order-edit": {"read": True}},
    ),
    ToolDefinition(
        method="create_order_edit",
        name="Create Order Edit",
        description=(
            "Create a new commercetools Order Edit with staged actions for a target Order. "
            "Staged actions are not applied until apply_order_edit is called. "
            "Admin context only."
        ),
        parameters=CreateOrderEditParams,
        handler=create_order_edit,
        actions={"order-edit": {"create": True}},
    ),
    ToolDefinition(
        method="update_order_edit",
        name="Update Order Edit",
        description=(
            "Apply update actions to an existing commercetools Order Edit identified by ID or key. "
            "Supported actions: addStagedAction, setStagedActions, setComment, setKey, setCustomField, setCustomType. "
            "Admin context only."
        ),
        parameters=UpdateOrderEditParams,
        handler=update_order_edit,
        actions={"order-edit": {"update": True}},
    ),
    ToolDefinition(
        method="apply_order_edit",
        name="Apply Order Edit",
        description=(
            "Apply a commercetools Order Edit to its target Order, executing all staged actions permanently. "
            "Requires both the edit version and the current Order resource version. "
            "Admin context only."
        ),
        parameters=ApplyOrderEditParams,
        handler=apply_order_edit,
        actions={"order-edit": {"update": True}},
    ),
]

for _tool in _ORDER_EDIT_TOOLS:
    register_tool(_tool)
