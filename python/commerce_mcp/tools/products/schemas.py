from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class ListProductsParams(BaseModel):
    id: str | None = Field(None, description="Filter by product ID")
    limit: int = Field(20, ge=1, le=500, description="Maximum number of results (1–500)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(
        None,
        description='Sort criteria, e.g. ["name.en asc", "createdAt desc"]',
    )
    where: list[str] | None = Field(
        None,
        description='Query predicates, e.g. ["masterData(current(name(en=\\"Product\\")))"]',
    )
    expand: list[str] | None = Field(
        None,
        description='Fields to expand, e.g. ["masterData.current.categories[*]"]',
    )


class LocalizedString(BaseModel):
    en: str | None = None
    de: str | None = None
    fr: str | None = None


class PriceValue(BaseModel):
    type: str = "centPrecision"
    currency_code: str = Field(alias="currencyCode")
    cent_amount: int = Field(alias="centAmount")
    fraction_digits: int = Field(default=2, alias="fractionDigits")
    model_config = {"populate_by_name": True}


class PriceDraft(BaseModel):
    value: PriceValue


class ImageDraft(BaseModel):
    url: str
    dimensions: dict[str, int] | None = None


class AttributeDraft(BaseModel):
    name: str
    value: Any


class ProductVariantDraft(BaseModel):
    sku: str | None = None
    key: str | None = None
    prices: list[PriceDraft] | None = None
    images: list[ImageDraft] | None = None
    attributes: list[AttributeDraft] | None = None


class CreateProductParams(BaseModel):
    name: LocalizedString
    product_type_id: str = Field(alias="productTypeId", description="ID of the product type")
    slug: LocalizedString
    description: LocalizedString | None = None
    categories: list[str] | None = Field(None, description="Category IDs")
    master_variant: ProductVariantDraft | None = Field(None, alias="masterVariant")
    publish: bool | None = Field(None, description="Publish immediately after creation")
    model_config = {"populate_by_name": True}


class ProductUpdateAction(BaseModel):
    action: str
    model_config = {"extra": "allow"}


class UpdateProductParams(BaseModel):
    id: str = Field(description="Product ID")
    version: int = Field(description="Current product version for optimistic locking")
    actions: list[ProductUpdateAction] = Field(description="Update actions to apply")
