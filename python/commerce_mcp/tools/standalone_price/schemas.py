from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ReadStandalonePriceParams(BaseModel):
    id: str | None = Field(None, description="The ID of the standalone price to fetch")
    key: str | None = Field(None, description="The key of the standalone price to fetch")
    where: list[str] | None = Field(None, description='Query predicates. Example: ["sku=\\"SKU-1\\""]')
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 10)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["value.centAmount asc"]')
    expand: list[str] | None = Field(None, description='Reference paths to expand. Example: ["customerGroup", "channel"]')


class MoneyValue(BaseModel):
    type: str = Field("centPrecision", description="Money type")
    currency_code: str = Field(alias="currencyCode", description="Currency code (e.g. EUR, USD)")
    cent_amount: int = Field(alias="centAmount", description="Amount in cents")
    fraction_digits: int | None = Field(None, alias="fractionDigits", description="Number of fraction digits")
    model_config = {"populate_by_name": True}


class CreateStandalonePriceParams(BaseModel):
    sku: str = Field(description="SKU of the ProductVariant this price belongs to")
    value: MoneyValue = Field(description="Money value of this price")
    key: str | None = Field(None, description="User-defined unique identifier (2–256 alphanumeric chars)")
    country: str | None = Field(None, description="Country code (ISO 3166-1 alpha-2, e.g. DE)")
    customer_group: dict[str, Any] | None = Field(None, alias="customerGroup", description="CustomerGroup reference for which this price is valid")
    channel: dict[str, Any] | None = Field(None, description="Channel reference for which this price is valid")
    valid_from: str | None = Field(None, alias="validFrom", description="ISO 8601 date from which this price is valid")
    valid_until: str | None = Field(None, alias="validUntil", description="ISO 8601 date until which this price is valid")
    tiers: list[dict[str, Any]] | None = Field(None, description="Price tiers for bulk discounts")
    active: bool | None = Field(None, description="Whether the price is active")
    staged: bool | None = Field(None, description="Whether to create a staged price")
    model_config = {"populate_by_name": True}


class StandalonePriceUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateStandalonePriceParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[StandalonePriceUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the standalone price to update")
    key: str | None = Field(None, description="The key of the standalone price to update")
