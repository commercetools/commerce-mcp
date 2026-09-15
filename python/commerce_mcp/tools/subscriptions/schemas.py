from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ReadSubscriptionParams(BaseModel):
    id: str | None = Field(None, description="The ID of the subscription to retrieve")
    key: str | None = Field(None, description="The key of the subscription to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of items to skip (0–10000)")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["createdAt desc"]')
    where: list[str] | None = Field(None, description='Query predicates. Example: ["key=\\"my-sub\\""]')
    expand: list[str] | None = Field(None, description='Reference paths to expand')


class SubscriptionMessageType(BaseModel):
    resource_type_id: str = Field(alias="resourceTypeId", description="Resource type to subscribe to")
    types: list[str] | None = Field(None, description="Message types to subscribe to; omit for all types")
    model_config = {"populate_by_name": True}


class SubscriptionChangeType(BaseModel):
    resource_type_id: str = Field(alias="resourceTypeId", description="Resource type to track changes for")
    model_config = {"populate_by_name": True}


class CreateSubscriptionParams(BaseModel):
    destination: dict[str, Any] = Field(description="Destination config (SQS, SNS, GoogleCloudPubSub, AzureEventGrid, AzureServiceBus, RabbitMQ)")
    key: str | None = Field(None, description="User-defined unique identifier (2–256 chars)")
    changes: list[SubscriptionChangeType] | None = Field(None, description="Resource types to track changes for")
    messages: list[SubscriptionMessageType] | None = Field(None, description="Message subscriptions for specific resource types")
    format: dict[str, Any] | None = Field(None, description="Message format: Platform or CloudEvents")


class SubscriptionUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateSubscriptionParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[SubscriptionUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the subscription to update")
    key: str | None = Field(None, description="The key of the subscription to update")
