from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_customer_group, read_customer_group, update_customer_group
from .schemas import CreateCustomerGroupParams, ReadCustomerGroupParams, UpdateCustomerGroupParams

_CUSTOMER_GROUP_TOOLS = [
    ToolDefinition(
        method="read_customer_group",
        name="Read Customer Group",
        description="Read or list customer groups. Provide an id or key to fetch a specific group, or omit both to list groups.",
        parameters=ReadCustomerGroupParams,
        handler=read_customer_group,
        actions={"customer_group": {"read": True}},
    ),
    ToolDefinition(
        method="create_customer_group",
        name="Create Customer Group",
        description="Create a new customer group with a name and optional key.",
        parameters=CreateCustomerGroupParams,
        handler=create_customer_group,
        actions={"customer_group": {"create": True}},
    ),
    ToolDefinition(
        method="update_customer_group",
        name="Update Customer Group",
        description="Apply update actions to an existing customer group identified by id or key.",
        parameters=UpdateCustomerGroupParams,
        handler=update_customer_group,
        actions={"customer_group": {"update": True}},
    ),
]

for _tool in _CUSTOMER_GROUP_TOOLS:
    register_tool(_tool)
