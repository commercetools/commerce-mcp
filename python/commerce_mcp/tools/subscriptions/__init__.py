from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_subscription, read_subscription, update_subscription
from .schemas import CreateSubscriptionParams, ReadSubscriptionParams, UpdateSubscriptionParams
from .prompts import CREATE_SUBSCRIPTION_PROMPT, READ_SUBSCRIPTION_PROMPT, UPDATE_SUBSCRIPTION_PROMPT

_SUBSCRIPTIONS_TOOLS = [
    ToolDefinition(
        method="read_subscription",
        name="Read Subscription",
        description=READ_SUBSCRIPTION_PROMPT,
        parameters=ReadSubscriptionParams,
        handler=read_subscription,
        actions={"subscriptions": {"read": True}},
    ),
    ToolDefinition(
        method="create_subscription",
        name="Create Subscription",
        description=CREATE_SUBSCRIPTION_PROMPT,
        parameters=CreateSubscriptionParams,
        handler=create_subscription,
        actions={"subscriptions": {"create": True}},
    ),
    ToolDefinition(
        method="update_subscription",
        name="Update Subscription",
        description=UPDATE_SUBSCRIPTION_PROMPT,
        parameters=UpdateSubscriptionParams,
        handler=update_subscription,
        actions={"subscriptions": {"update": True}},
    ),
]

for _tool in _SUBSCRIPTIONS_TOOLS:
    register_tool(_tool)
