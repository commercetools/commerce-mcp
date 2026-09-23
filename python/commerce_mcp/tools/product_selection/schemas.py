from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ReadProductSelectionParams(BaseModel):
    id: str | None = Field(None, description="The ID of the product selection to retrieve")
    key: str | None = Field(None, description="The key of the product selection to retrieve")
    where: list[str] | None = Field(None, description='Query predicates. Example: ["mode=\\"Individual\\""]')
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["createdAt desc"]')
    expand: list[str] | None = Field(None, description='Reference paths to expand')


class CreateProductSelectionParams(BaseModel):
    name: dict[str, str] = Field(description="Localized name of the product selection")
    key: str | None = Field(None, description="User-defined unique identifier")
    mode: Literal["Individual", "IndividualExclusion"] | None = Field(None, description="Selection mode (default: Individual)")
    custom: dict[str, Any] | None = Field(None, description="Custom fields")


class ProductSelectionUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateProductSelectionParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[ProductSelectionUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the product selection to update")
    key: str | None = Field(None, description="The key of the product selection to update")
