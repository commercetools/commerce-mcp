from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class ReadTaxCategoryParams(BaseModel):
    id: str | None = Field(None, description="The ID of the tax category to retrieve")
    key: str | None = Field(None, description="The key of the tax category to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of elements to skip (0–10000)")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["name asc", "createdAt desc"]')
    where: list[str] | None = Field(
        None, description='Query predicates. Example: ["name=\\"Standard Tax\\""]'
    )
    expand: list[str] | None = Field(
        None, description='Reference paths to expand. Example: ["custom.type"]'
    )


class TaxSubRate(BaseModel):
    name: str = Field(description="Name of the sub-rate")
    amount: float = Field(ge=0, le=1, description="Sub-rate as a decimal (e.g., 0.05 for 5%)")
    id: str | None = Field(None, description="Unique identifier for the sub-rate")
    key: str | None = Field(None, description="User-defined unique identifier for the sub-rate")


class TaxRate(BaseModel):
    name: str = Field(description="Name of the tax rate")
    amount: float = Field(ge=0, le=1, description="Tax rate as a decimal (e.g., 0.19 for 19%)")
    included_in_price: bool | None = Field(
        None, alias="includedInPrice", description="Whether the tax is included in the price"
    )
    country: str = Field(min_length=2, max_length=2, description="Country code (ISO 3166-1 alpha-2)")
    state: str | None = Field(None, description="State or region within the country")
    id: str | None = Field(None, description="Unique identifier for the tax rate")
    key: str | None = Field(None, description="User-defined unique identifier for the tax rate")
    sub_rates: list[TaxSubRate] | None = Field(
        None, alias="subRates", description="Sub-rates for this tax rate"
    )
    model_config = {"populate_by_name": True}


class CustomTypeRef(BaseModel):
    id: str
    type_id: str = Field(alias="typeId")
    model_config = {"populate_by_name": True}


class CustomFields(BaseModel):
    type: CustomTypeRef
    fields: dict[str, Any]


class CreateTaxCategoryParams(BaseModel):
    name: str = Field(description="Name of the tax category")
    key: str | None = Field(None, description="User-defined unique identifier for the tax category")
    description: str | None = Field(None, description="Description of the tax category")
    rates: list[TaxRate] = Field(description="Tax rates for this category")
    custom: CustomFields | None = Field(None, description="Custom fields for the tax category")


class TaxCategoryUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateTaxCategoryParams(BaseModel):
    version: int = Field(
        description="Expected version of the tax category on which the changes should be applied"
    )
    actions: list[TaxCategoryUpdateAction] = Field(
        description="Update actions to be performed on the tax category"
    )
    id: str | None = Field(None, description="The ID of the tax category to update")
    key: str | None = Field(None, description="The key of the tax category to update")
