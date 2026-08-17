from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ReadDiscountCodeParams(BaseModel):
    id: str | None = Field(None, description="The ID of the discount code to retrieve")
    key: str | None = Field(None, description="The key of the discount code to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 10)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["createdAt desc"]')
    where: list[str] | None = Field(None, description='Query predicates. Example: ["isActive=true"]')
    expand: list[str] | None = Field(None, description='Reference paths to expand. Example: ["cartDiscounts[*]"]')


class CartDiscountReference(BaseModel):
    id: str = Field(description="ID of the cart discount")
    type_id: str = Field("cart-discount", alias="typeId", description="Resource type identifier")
    model_config = {"populate_by_name": True}


class CreateDiscountCodeParams(BaseModel):
    code: str = Field(description="Unique code value of the discount code")
    cart_discounts: list[CartDiscountReference] = Field(alias="cartDiscounts", description="Cart discounts applied when this code is used (1–10)")
    name: dict[str, str] | None = Field(None, description="Localized name of the discount code")
    description: dict[str, str] | None = Field(None, description="Localized description")
    key: str | None = Field(None, description="User-defined unique identifier")
    cart_predicate: str | None = Field(None, alias="cartPredicate", description="Predicate that must match the cart")
    is_active: bool | None = Field(None, alias="isActive", description="Whether the code is active (default true)")
    max_applications: int | None = Field(None, alias="maxApplications", description="Maximum total uses")
    max_applications_per_customer: int | None = Field(None, alias="maxApplicationsPerCustomer", description="Maximum uses per customer")
    groups: list[str] | None = Field(None, description="Groups this code belongs to")
    valid_from: str | None = Field(None, alias="validFrom", description="ISO 8601 date when code becomes valid")
    valid_until: str | None = Field(None, alias="validUntil", description="ISO 8601 date when code expires")
    custom: dict[str, Any] | None = Field(None, description="Custom fields for the discount code")
    model_config = {"populate_by_name": True}


class DiscountCodeUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateDiscountCodeParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[DiscountCodeUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the discount code to update")
    key: str | None = Field(None, description="The key of the discount code to update")
