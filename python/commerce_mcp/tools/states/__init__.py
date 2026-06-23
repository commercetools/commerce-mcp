from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadStateParams, CreateStateParams, UpdateStateParams
from .functions import read_state, create_state, update_state

_STATES_TOOLS = [
    ToolDefinition(
        method="read_state",
        name="Read State",
        description=(
            "Fetch a commercetools State by ID, key, or query predicates. "
            "States represent custom workflow steps for Orders, Line Items, Products, Reviews, Payments, Quotes, and Recurring Orders. "
            "Admin context only."
        ),
        parameters=ReadStateParams,
        handler=read_state,
        actions={"states": {"read": True}},
    ),
    ToolDefinition(
        method="create_state",
        name="Create State",
        description=(
            "Create a new commercetools State. "
            "Each State has a type (OrderState, LineItemState, ProductState, etc.) that determines which resource it applies to. "
            "Admin context only."
        ),
        parameters=CreateStateParams,
        handler=create_state,
        actions={"states": {"create": True}},
    ),
    ToolDefinition(
        method="update_state",
        name="Update State",
        description=(
            "Apply update actions to an existing commercetools State identified by ID or key. "
            "Supported actions: addRoles, removeRoles, setRoles, changeKey, changeType, changeInitial, setName, setDescription, setTransitions. "
            "Admin context only."
        ),
        parameters=UpdateStateParams,
        handler=update_state,
        actions={"states": {"update": True}},
    ),
]

for _tool in _STATES_TOOLS:
    register_tool(_tool)
