from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class ReadShippingMethodsParams(BaseModel):
    id: str | None = Field(None, description="The ID of the shipping method to retrieve")
    key: str | None = Field(None, description="The key of the shipping method to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of elements to skip (0–10000)")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["createdAt desc"]')
    where: list[str] | None = Field(
        None, description='Query predicates. Example: ["name=\\"Standard Shipping\\""]'
    )
    expand: list[str] | None = Field(
        None, description='Reference paths to expand. Example: ["zoneRates[*].zone"]'
    )


class MoneyDraft(BaseModel):
    type: str = Field(description='Must be "centPrecision"')
    currency_code: str = Field(alias="currencyCode", description="Currency code (ISO 4217)")
    cent_amount: int = Field(alias="centAmount", description="Amount in the smallest currency unit")
    fraction_digits: int = Field(alias="fractionDigits", description="Number of fraction digits")
    model_config = {"populate_by_name": True}


class ShippingRateTier(BaseModel):
    type: str = Field(description='Must be "CartValue"')
    minimum_cent_amount: int = Field(alias="minimumCentAmount", description="Minimum cart value in cents")
    price: MoneyDraft = Field(description="Price for this tier")
    model_config = {"populate_by_name": True}


class ShippingRate(BaseModel):
    price: MoneyDraft = Field(description="Shipping price")
    free_above: MoneyDraft | None = Field(
        None, alias="freeAbove", description="Cart value above which shipping is free"
    )
    tiers: list[ShippingRateTier] | None = Field(None, description="Price tiers for this shipping rate")
    model_config = {"populate_by_name": True}


class ZoneReference(BaseModel):
    id: str = Field(description="The ID of the zone")
    type_id: str = Field(alias="typeId", description='Must be "zone"')
    model_config = {"populate_by_name": True}


class ZoneRate(BaseModel):
    zone: ZoneReference = Field(description="Reference to the zone")
    shipping_rates: list[ShippingRate] = Field(
        alias="shippingRates", description="Shipping rates for this zone"
    )
    model_config = {"populate_by_name": True}


class TaxCategoryReference(BaseModel):
    id: str = Field(description="The ID of the tax category")
    type_id: str = Field(alias="typeId", description='Must be "tax-category"')
    model_config = {"populate_by_name": True}


class CustomTypeRef(BaseModel):
    id: str
    type_id: str = Field(alias="typeId")
    model_config = {"populate_by_name": True}


class CustomFields(BaseModel):
    type: CustomTypeRef
    fields: dict[str, Any]


class CreateShippingMethodsParams(BaseModel):
    name: str = Field(description="Name of the shipping method")
    key: str | None = Field(None, description="User-defined unique identifier for the shipping method")
    description: str | None = Field(None, description="Description of the shipping method")
    zone_rates: list[ZoneRate] = Field(
        alias="zoneRates", description="Zone rates for the shipping method"
    )
    is_default: bool | None = Field(
        None, alias="isDefault", description="Whether this is the default shipping method"
    )
    tax_category: TaxCategoryReference | None = Field(
        None, alias="taxCategory", description="Tax category for the shipping method"
    )
    custom: CustomFields | None = Field(None, description="Custom fields for the shipping method")
    model_config = {"populate_by_name": True}


class ShippingMethodUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateShippingMethodsParams(BaseModel):
    version: int = Field(
        description="Expected version of the shipping method on which the changes should be applied"
    )
    actions: list[ShippingMethodUpdateAction] = Field(
        description="Update actions to be performed on the shipping method"
    )
    id: str | None = Field(None, description="The ID of the shipping method to update")
    key: str | None = Field(None, description="The key of the shipping method to update")
