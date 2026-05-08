from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_payments, read_payments, update_payments
from .schemas import CreatePaymentsParams, ReadPaymentsParams, UpdatePaymentsParams

_PAYMENTS_TOOLS = [
    ToolDefinition(
        method="read_payments",
        name="Read Payment",
        description="Read or list payments. Provide an id or key to fetch a specific payment, or omit both to list payments with optional filtering.",
        parameters=ReadPaymentsParams,
        handler=read_payments,
        actions={"payments": {"read": True}},
    ),
    ToolDefinition(
        method="create_payments",
        name="Create Payment",
        description="Create a new payment with a planned amount and optional payment method information.",
        parameters=CreatePaymentsParams,
        handler=create_payments,
        actions={"payments": {"create": True}},
    ),
    ToolDefinition(
        method="update_payments",
        name="Update Payment",
        description="Apply update actions to an existing payment identified by id or key.",
        parameters=UpdatePaymentsParams,
        handler=update_payments,
        actions={"payments": {"update": True}},
    ),
]

for _tool in _PAYMENTS_TOOLS:
    register_tool(_tool)
