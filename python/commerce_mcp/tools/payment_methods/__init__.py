from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_payment_methods, read_payment_methods, update_payment_methods
from .prompts import CREATE_PAYMENT_METHOD_PROMPT, READ_PAYMENT_METHOD_PROMPT, UPDATE_PAYMENT_METHOD_PROMPT
from .schemas import CreatePaymentMethodsParams, ReadPaymentMethodsParams, UpdatePaymentMethodsParams

_PAYMENT_METHODS_TOOLS = [
    ToolDefinition(
        method="read_payment_methods",
        name="Read Payment Method",
        description=READ_PAYMENT_METHOD_PROMPT,
        parameters=ReadPaymentMethodsParams,
        handler=read_payment_methods,
        actions={"payment_methods": {"read": True}},
    ),
    ToolDefinition(
        method="create_payment_methods",
        name="Create Payment Method",
        description=CREATE_PAYMENT_METHOD_PROMPT,
        parameters=CreatePaymentMethodsParams,
        handler=create_payment_methods,
        actions={"payment_methods": {"create": True}},
    ),
    ToolDefinition(
        method="update_payment_methods",
        name="Update Payment Method",
        description=UPDATE_PAYMENT_METHOD_PROMPT,
        parameters=UpdatePaymentMethodsParams,
        handler=update_payment_methods,
        actions={"payment_methods": {"update": True}},
    ),
]

for _tool in _PAYMENT_METHODS_TOOLS:
    register_tool(_tool)
