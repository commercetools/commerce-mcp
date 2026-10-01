from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


# ── Read ──────────────────────────────────────────────────────────────────────

class ReadRecurringOrdersParams(BaseModel):
    id: str | None = Field(None, description="The ID of the recurring order to retrieve")
    key: str | None = Field(None, description="The key of the recurring order to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results requested. Default: 20, Minimum: 1, Maximum: 500")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of elements skipped. Default: 0, Maximum: 10000")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["createdAt desc"]')
    where: list[str] | None = Field(None, description='Query predicates. Example: ["customerId=\\"customer-123\\""]')
    expand: list[str] | None = Field(None, description='Reference paths to expand. Example: ["cart", "customer", "store"]')


# ── Create ────────────────────────────────────────────────────────────────────

class _CartReference(BaseModel):
    id: str
    type_id: Literal["cart"] = Field("cart", alias="typeId")
    model_config = {"populate_by_name": True}


class _RecurrencePolicyReference(BaseModel):
    id: str
    type_id: Literal["recurrence-policy"] = Field("recurrence-policy", alias="typeId")
    model_config = {"populate_by_name": True}


class _Schedule(BaseModel):
    recurrence_policy: _RecurrencePolicyReference = Field(alias="recurrencePolicy", description="Reference to the RecurrencePolicy")
    model_config = {"populate_by_name": True}


class _StateReference(BaseModel):
    id: str
    type_id: Literal["state"] = Field("state", alias="typeId")
    model_config = {"populate_by_name": True}


class _TypeReference(BaseModel):
    id: str
    type_id: Literal["type"] = Field("type", alias="typeId")
    model_config = {"populate_by_name": True}


class _CustomFields(BaseModel):
    type: _TypeReference
    fields: dict[str, Any]


class CreateRecurringOrdersParams(BaseModel):
    cart: _CartReference = Field(description="Reference to the Cart for a RecurringOrder")
    cart_version: int = Field(alias="cartVersion", description="Current version of the Cart")
    key: str | None = Field(None, description="User-defined unique identifier for the recurring order")
    schedule: _Schedule | None = Field(None, description="Schedule of the RecurringOrder")
    starts_at: str | None = Field(None, alias="startsAt", description="Date and time (UTC) when the RecurringOrder starts creating new Orders")
    expires_at: str | None = Field(None, alias="expiresAt", description="Date and time (UTC) when the RecurringOrder expires")
    state: _StateReference | None = Field(None, description="State of the RecurringOrder in a custom workflow")
    custom: _CustomFields | None = Field(None, description="Custom fields for the recurring order")
    model_config = {"populate_by_name": True}


# ── Update ────────────────────────────────────────────────────────────────────

class RecurringOrderUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateRecurringOrdersParams(BaseModel):
    version: int = Field(description="Expected version of the recurring order on which the changes should be applied")
    actions: list[RecurringOrderUpdateAction] = Field(description="Update actions to be performed on the recurring order")
    id: str | None = Field(None, description="The ID of the recurring order to update")
    key: str | None = Field(None, description="The key of the recurring order to update")
