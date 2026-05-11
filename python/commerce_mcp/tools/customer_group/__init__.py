from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_customer_group, read_customer_group, update_customer_group
from .prompts import CREATE_CUSTOMER_GROUP_PROMPT, READ_CUSTOMER_GROUP_PROMPT, UPDATE_CUSTOMER_GROUP_PROMPT
from .schemas import CreateCustomerGroupParams, ReadCustomerGroupParams, UpdateCustomerGroupParams

_CUSTOMER_GROUP_TOOLS = [
    ToolDefinition(
        method="read_customer_group",
        name="Read Customer Group",
        description=READ_CUSTOMER_GROUP_PROMPT,
        parameters=ReadCustomerGroupParams,
        handler=read_customer_group,
        actions={"customer_group": {"read": True}},
    ),
    ToolDefinition(
        method="create_customer_group",
        name="Create Customer Group",
        description=CREATE_CUSTOMER_GROUP_PROMPT,
        parameters=CreateCustomerGroupParams,
        handler=create_customer_group,
        actions={"customer_group": {"create": True}},
    ),
    ToolDefinition(
        method="update_customer_group",
        name="Update Customer Group",
        description=UPDATE_CUSTOMER_GROUP_PROMPT,
        parameters=UpdateCustomerGroupParams,
        handler=update_customer_group,
        actions={"customer_group": {"update": True}},
    ),
]

for _tool in _CUSTOMER_GROUP_TOOLS:
    register_tool(_tool)
