from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_payments, read_payments, update_payments
from .prompts import CREATE_PAYMENT_PROMPT, READ_PAYMENT_PROMPT, UPDATE_PAYMENT_PROMPT
from .schemas import CreatePaymentsParams, ReadPaymentsParams, UpdatePaymentsParams

_PAYMENTS_TOOLS = [
    ToolDefinition(
        method="read_payments",
        name="Read Payment",
        description=READ_PAYMENT_PROMPT,
        parameters=ReadPaymentsParams,
        handler=read_payments,
        actions={"payments": {"read": True}},
    ),
    ToolDefinition(
        method="create_payments",
        name="Create Payment",
        description=CREATE_PAYMENT_PROMPT,
        parameters=CreatePaymentsParams,
        handler=create_payments,
        actions={"payments": {"create": True}},
    ),
    ToolDefinition(
        method="update_payments",
        name="Update Payment",
        description=UPDATE_PAYMENT_PROMPT,
        parameters=UpdatePaymentsParams,
        handler=update_payments,
        actions={"payments": {"update": True}},
    ),
]

for _tool in _PAYMENTS_TOOLS:
    register_tool(_tool)
