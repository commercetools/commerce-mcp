from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_payment_methods, read_payment_methods, update_payment_methods
from .schemas import CreatePaymentMethodsParams, ReadPaymentMethodsParams, UpdatePaymentMethodsParams

_PAYMENT_METHODS_TOOLS = [
    ToolDefinition(
        method="read_payment_methods",
        name="Read Payment Method",
        description="Read or list payment methods. Provide an id or key to fetch a specific method, or omit both to list payment methods.",
        parameters=ReadPaymentMethodsParams,
        handler=read_payment_methods,
        actions={"payment_methods": {"read": True}},
    ),
    ToolDefinition(
        method="create_payment_methods",
        name="Create Payment Method",
        description="Create a new payment method with a localized name, payment interface, and optional customer or business unit association.",
        parameters=CreatePaymentMethodsParams,
        handler=create_payment_methods,
        actions={"payment_methods": {"create": True}},
    ),
    ToolDefinition(
        method="update_payment_methods",
        name="Update Payment Method",
        description="Apply update actions to an existing payment method identified by id or key.",
        parameters=UpdatePaymentMethodsParams,
        handler=update_payment_methods,
        actions={"payment_methods": {"update": True}},
    ),
]

for _tool in _PAYMENT_METHODS_TOOLS:
    register_tool(_tool)
