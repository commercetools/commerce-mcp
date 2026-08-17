from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ReadProductDiscountParams(BaseModel):
    id: str | None = Field(None, description="The ID of the product discount to retrieve")
    key: str | None = Field(None, description="The key of the product discount to retrieve")
    where: list[str] | None = Field(None, description='Query predicates. Example: ["isActive=true"]')
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["sortOrder asc"]')
    expand: list[str] | None = Field(None, description='Reference paths to expand')


class CreateProductDiscountParams(BaseModel):
    name: dict[str, str] = Field(description="Localized name of the product discount")
    value: dict[str, Any] = Field(description="Discount value (absolute, relative, or external)")
    predicate: str = Field(description="Predicate that determines which products this discount applies to")
    sort_order: str = Field(alias="sortOrder", description="Numeric sort order (e.g. '0.5') — higher values take priority")
    is_active: bool | None = Field(None, alias="isActive", description="Whether the discount is active")
    key: str | None = Field(None, description="User-defined unique identifier (2–256 alphanumeric chars)")
    description: dict[str, str] | None = Field(None, description="Localized description")
    valid_from: str | None = Field(None, alias="validFrom", description="ISO 8601 date from which this discount is valid")
    valid_until: str | None = Field(None, alias="validUntil", description="ISO 8601 date until which this discount is valid")
    model_config = {"populate_by_name": True}


class ProductDiscountUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateProductDiscountParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[ProductDiscountUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the product discount to update")
    key: str | None = Field(None, description="The key of the product discount to update")
