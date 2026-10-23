from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field

# Localized string: any locale key → text (matches TypeScript z.record(z.string(), z.string()))
LocalizedString = dict[str, str]


class ProductTypeReference(BaseModel):
    id: str = Field(description="ID of the product type")
    type_id: Literal["product-type"] = Field("product-type", alias="typeId")
    model_config = {"populate_by_name": True}


class CategoryReference(BaseModel):
    id: str = Field(description="ID of the category")
    type_id: Literal["category"] = Field("category", alias="typeId")
    model_config = {"populate_by_name": True}


class TaxCategoryReference(BaseModel):
    id: str = Field(description="ID of the tax category")
    type_id: Literal["tax-category"] = Field("tax-category", alias="typeId")
    model_config = {"populate_by_name": True}


class StateReference(BaseModel):
    id: str = Field(description="ID of the state")
    type_id: Literal["state"] = Field("state", alias="typeId")
    model_config = {"populate_by_name": True}


class PriceValue(BaseModel):
    type: Literal["centPrecision"] = "centPrecision"
    currency_code: str = Field(alias="currencyCode")
    cent_amount: int = Field(alias="centAmount")
    fraction_digits: int = Field(alias="fractionDigits")
    model_config = {"populate_by_name": True}


class PriceDraft(BaseModel):
    value: PriceValue
    model_config = {"populate_by_name": True}


class ImageDimensions(BaseModel):
    w: int
    h: int


class ImageDraft(BaseModel):
    url: str
    dimensions: ImageDimensions | None = None
    model_config = {"populate_by_name": True}


class AttributeDraft(BaseModel):
    name: str
    value: Any
    model_config = {"populate_by_name": True}


class ProductVariantDraft(BaseModel):
    sku: str | None = None
    key: str | None = None
    prices: list[PriceDraft] | None = None
    images: list[ImageDraft] | None = None
    attributes: list[AttributeDraft] | None = None
    model_config = {"populate_by_name": True}


class SearchKeywordEntry(BaseModel):
    text: str


class ListProductsParams(BaseModel):
    id: str | None = Field(None, description="The ID of the product to read")
    limit: int | None = Field(
        None,
        ge=1,
        le=500,
        description="A limit on the number of objects to be returned. Limit can range between 1 and 500, and the default is 10.",
    )
    offset: int | None = Field(
        None,
        ge=0,
        description="The number of items to skip before starting to collect the result set.",
    )
    sort: list[str] | None = Field(
        None,
        description='Sort criteria for the results. Example: ["name.en asc", "createdAt desc"]',
    )
    where: list[str] | None = Field(
        None,
        description='Query predicates specified as strings. Example: ["masterData(current(name(en = \\"Product Name\\")))"]',
    )
    expand: list[str] | None = Field(
        None,
        description='An array of field paths to expand. Example: ["masterData.current.categories[*]", "masterData.current.masterVariant.attributes[*]"]',
    )
    model_config = {"populate_by_name": True}


class CreateProductParams(BaseModel):
    product_type: ProductTypeReference = Field(
        alias="productType",
        description="Reference to the product type",
    )
    name: LocalizedString = Field(description="Localized name of the product")
    slug: LocalizedString = Field(description="Localized slug of the product")
    description: LocalizedString | None = Field(None, description="Localized description of the product")
    categories: list[CategoryReference] | None = Field(None, description="References to categories")
    master_variant: ProductVariantDraft | None = Field(
        None,
        alias="masterVariant",
        description="The master variant of the product",
    )
    variants: list[ProductVariantDraft] | None = Field(None, description="Additional product variants")
    key: str | None = Field(None, description="User-defined unique identifier")
    meta_title: LocalizedString | None = Field(None, alias="metaTitle", description="Localized meta title")
    meta_description: LocalizedString | None = Field(None, alias="metaDescription", description="Localized meta description")
    meta_keywords: LocalizedString | None = Field(None, alias="metaKeywords", description="Localized meta keywords")
    search_keywords: dict[str, list[SearchKeywordEntry]] | None = Field(
        None,
        alias="searchKeywords",
        description="Search keywords per locale",
    )
    tax_category: TaxCategoryReference | None = Field(
        None,
        alias="taxCategory",
        description="Reference to a tax category",
    )
    state: StateReference | None = Field(None, description="Reference to a state")
    model_config = {"populate_by_name": True}


class ProductUpdateAction(BaseModel):
    action: str = Field(description="The name of the update action to perform")
    model_config = {"extra": "allow"}


class UpdateProductParams(BaseModel):
    id: str = Field(description="The ID of the product to update")
    version: int = Field(description="The current version of the product")
    actions: list[ProductUpdateAction] = Field(
        description='Array of update actions to perform on the product. Each action should have an "action" field and other fields specific to that action type.',
    )
    model_config = {"populate_by_name": True}
