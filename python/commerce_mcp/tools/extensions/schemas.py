from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ReadExtensionParams(BaseModel):
    id: str | None = Field(None, description="The ID of the extension to retrieve")
    key: str | None = Field(None, description="The key of the extension to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of items to skip (0–10000)")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["createdAt desc"]')
    where: list[str] | None = Field(None, description='Query predicates. Example: ["key=\\"my-ext\\""]')
    expand: list[str] | None = Field(None, description='Reference paths to expand')


class ExtensionTrigger(BaseModel):
    resource_type_id: str = Field(alias="resourceTypeId", description="Resource type to trigger on (e.g. cart, order, payment)")
    actions: list[Literal["Create", "Update"]] = Field(description="Trigger on Create, Update, or both")
    condition: str | None = Field(None, description="Optional predicate for conditional triggering")
    model_config = {"populate_by_name": True}


class CreateExtensionParams(BaseModel):
    triggers: list[ExtensionTrigger] = Field(description="Triggers that activate this extension")
    destination: dict[str, Any] = Field(description="Destination config (HTTP, AWSLambda, or GoogleCloudFunction)")
    key: str | None = Field(None, description="User-defined unique identifier")
    timeout_in_ms: int | None = Field(None, alias="timeoutInMs", ge=1, le=10000, description="Timeout in milliseconds (1–10000, default 2000)")
    model_config = {"populate_by_name": True}


class ExtensionUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateExtensionParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[ExtensionUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the extension to update")
    key: str | None = Field(None, description="The key of the extension to update")
