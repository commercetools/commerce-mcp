from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ReadReviewParams(BaseModel):
    id: str | None = Field(None, description="The ID of the review to retrieve")
    key: str | None = Field(None, description="The key of the review to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of items to skip (0–10000)")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["createdAt desc"]')
    where: list[str] | None = Field(None, description='Query predicates. Example: ["rating > 50"]')
    expand: list[str] | None = Field(None, description='Reference paths to expand. Example: ["customer", "target"]')


class ReviewTarget(BaseModel):
    type_id: str = Field(alias="typeId", description="Target resource type: 'product' or 'channel'")
    id: str | None = Field(None, description="ID of the target resource")
    key: str | None = Field(None, description="Key of the target resource")
    model_config = {"populate_by_name": True}


class StateReference(BaseModel):
    type_id: str = Field("state", alias="typeId", description="Resource type identifier")
    id: str | None = Field(None, description="ID of the state")
    key: str | None = Field(None, description="Key of the state")
    model_config = {"populate_by_name": True}


class CustomerReference(BaseModel):
    type_id: str = Field("customer", alias="typeId", description="Resource type identifier")
    id: str | None = Field(None, description="ID of the customer")
    key: str | None = Field(None, description="Key of the customer")
    model_config = {"populate_by_name": True}


class CreateReviewParams(BaseModel):
    key: str | None = Field(None, description="User-defined unique identifier (2–256 chars)")
    uniqueness_value: str | None = Field(None, alias="uniquenessValue", description="Ensures only one review per scope")
    locale: str | None = Field(None, description="Language in which the content is written")
    author_name: str | None = Field(None, alias="authorName", description="Name of the review author")
    title: str | None = Field(None, description="Title of the review")
    text: str | None = Field(None, description="Text content of the review")
    target: ReviewTarget | None = Field(None, description="Target product or channel")
    state: StateReference | None = Field(None, description="State for approval processes")
    rating: int | None = Field(None, ge=-100, le=100, description="Rating (-100 to 100)")
    customer: CustomerReference | None = Field(None, description="Customer who created the review")
    custom: dict[str, Any] | None = Field(None, description="Custom fields for the review")
    model_config = {"populate_by_name": True}


class ReviewUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateReviewParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[ReviewUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the review to update")
    key: str | None = Field(None, description="The key of the review to update")
