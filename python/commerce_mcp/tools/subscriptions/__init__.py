from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_subscription, read_subscription, update_subscription
from .schemas import CreateSubscriptionParams, ReadSubscriptionParams, UpdateSubscriptionParams

_SUBSCRIPTIONS_TOOLS = [
    ToolDefinition(
        method="read_subscription",
        name="Read Subscription",
        description="Read or list subscriptions. Provide an id or key to fetch a specific subscription, or omit both to list subscriptions.",
        parameters=ReadSubscriptionParams,
        handler=read_subscription,
        actions={"subscriptions": {"read": True}},
    ),
    ToolDefinition(
        method="create_subscription",
        name="Create Subscription",
        description="Create a new subscription to receive notifications about resource changes (SQS, SNS, Pub/Sub, Azure, etc.).",
        parameters=CreateSubscriptionParams,
        handler=create_subscription,
        actions={"subscriptions": {"create": True}},
    ),
    ToolDefinition(
        method="update_subscription",
        name="Update Subscription",
        description="Apply update actions to an existing subscription identified by id or key.",
        parameters=UpdateSubscriptionParams,
        handler=update_subscription,
        actions={"subscriptions": {"update": True}},
    ),
]

for _tool in _SUBSCRIPTIONS_TOOLS:
    register_tool(_tool)
