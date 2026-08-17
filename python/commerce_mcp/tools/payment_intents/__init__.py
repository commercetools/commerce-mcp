from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import update_payment_intents
from .prompts import UPDATE_PAYMENT_INTENT_PROMPT
from .schemas import UpdatePaymentIntentsParams

_PAYMENT_INTENTS_TOOLS = [
    ToolDefinition(
        method="update_payment_intents",
        name="Update Payment Intent",
        description=UPDATE_PAYMENT_INTENT_PROMPT,
        parameters=UpdatePaymentIntentsParams,
        handler=update_payment_intents,
        actions={"payment_intents": {"update": True}},
    ),
]

for _tool in _PAYMENT_INTENTS_TOOLS:
    register_tool(_tool)
