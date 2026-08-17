from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .prompts import CREATE_CUSTOMER_PROMPT, READ_CUSTOMER_PROMPT, UPDATE_CUSTOMER_PROMPT
from .schemas import ReadCustomerParams, CreateCustomerParams, UpdateCustomerParams
from .functions import read_customer, create_customer, update_customer

_CUSTOMER_TOOLS = [
    ToolDefinition(
        method="read_customer",
        name="Read Customer",
        description=READ_CUSTOMER_PROMPT,
        parameters=ReadCustomerParams,
        handler=read_customer,
        actions={"customer": {"read": True}},
    ),
    ToolDefinition(
        method="create_customer",
        name="Create Customer",
        description=CREATE_CUSTOMER_PROMPT,
        parameters=CreateCustomerParams,
        handler=create_customer,
        actions={"customer": {"create": True}},
    ),
    ToolDefinition(
        method="update_customer",
        name="Update Customer",
        description=UPDATE_CUSTOMER_PROMPT,
        parameters=UpdateCustomerParams,
        handler=update_customer,
        actions={"customer": {"update": True}},
    ),
]

for _tool in _CUSTOMER_TOOLS:
    register_tool(_tool)
