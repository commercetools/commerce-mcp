from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import ReadCustomerParams, CreateCustomerParams, UpdateCustomerParams
from .functions import read_customer, create_customer, update_customer

_CUSTOMER_TOOLS = [
    ToolDefinition(
        method="read_customer",
        name="Read Customer",
        description=(
            "Fetch a Customer by ID from commercetools or a specific store, "
            "or query customers with optional filtering, sorting, and pagination. "
            "Customers can only read their own profile; store context reads within "
            "the store; admin context reads any customer."
        ),
        parameters=ReadCustomerParams,
        handler=read_customer,
        actions={"customer": {"read": True}},
    ),
    ToolDefinition(
        method="create_customer",
        name="Create Customer",
        description=(
            "Create a new Customer in commercetools or in a specific store. "
            "Requires store or admin context."
        ),
        parameters=CreateCustomerParams,
        handler=create_customer,
        actions={"customer": {"create": True}},
    ),
    ToolDefinition(
        method="update_customer",
        name="Update Customer",
        description=(
            "Apply update actions to an existing Customer using the commercetools API. "
            "Requires store or admin context."
        ),
        parameters=UpdateCustomerParams,
        handler=update_customer,
        actions={"customer": {"update": True}},
    ),
]

for _tool in _CUSTOMER_TOOLS:
    register_tool(_tool)
