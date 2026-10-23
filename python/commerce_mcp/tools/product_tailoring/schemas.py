from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


# ── Sub-models ────────────────────────────────────────────────────────────────

class ImageDimensions(BaseModel):
    w: float = Field(description="Image width")
    h: float = Field(description="Image height")


class TailoringImage(BaseModel):
    url: str = Field(description="Image URL")
    dimensions: ImageDimensions = Field(description="Image dimensions")
    model_config = {"populate_by_name": True}


class AssetSource(BaseModel):
    uri: str = Field(description="Asset URI")
    key: str | None = Field(None, description="Asset key")
    dimensions: ImageDimensions = Field(description="Asset dimensions")
    content_type: str | None = Field(None, alias="contentType", description="Content type")
    model_config = {"populate_by_name": True}


class CustomTypeRef(BaseModel):
    type_id: str = Field("type", alias="typeId", description="Resource type identifier")
    id: str | None = Field(None, description="ID of the custom type")
    key: str = Field(description="Key of the custom type")
    model_config = {"populate_by_name": True}


class TailoringAsset(BaseModel):
    id: str = Field(description="Asset ID")
    key: str = Field(description="Asset key")
    sources: list[AssetSource] = Field(description="Asset sources")
    name: dict[str, str] = Field(description="Localized asset name")
    description: dict[str, str] | None = Field(None, description="Localized asset description")
    tags: list[str] | None = Field(None, description="Asset tags")
    custom: CustomTypeRef | None = Field(None, description="Custom fields for the asset")
    model_config = {"populate_by_name": True}


class AttributeDraft(BaseModel):
    name: str = Field(description="Product attribute name")
    value: Any = Field(description="Product attribute value")


class TailoringVariantDraft(BaseModel):
    id: int = Field(description="Product variant ID")
    sku: str | None = Field(None, description="Product variant SKU")
    images: list[TailoringImage] | None = Field(None, description="Variant images")
    assets: list[TailoringAsset] | None = Field(None, description="Variant assets")
    attributes: list[AttributeDraft] | None = Field(None, description="Variant attributes")
    model_config = {"populate_by_name": True}


class ProductReference(BaseModel):
    type_id: str = Field("product", alias="typeId", description="Resource type identifier")
    id: str | None = Field(None, description="ID of the product")
    key: str | None = Field(None, description="Key of the product")
    model_config = {"populate_by_name": True}


class StoreReference(BaseModel):
    type_id: str = Field("store", alias="typeId", description="Resource type identifier")
    key: str = Field(description="Key of the store")
    model_config = {"populate_by_name": True}


class ProductTailoringTypeRef(BaseModel):
    id: str = Field(description="ID of the custom type")
    type_id: str = Field("type", alias="typeId", description="Resource type identifier")
    model_config = {"populate_by_name": True}


# ── Read ──────────────────────────────────────────────────────────────────────

class ReadProductTailoringParams(BaseModel):
    id: str | None = Field(None, description="The ID of the product tailoring entry to retrieve")
    key: str | None = Field(None, description="The key of the product tailoring entry to retrieve")
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store to read product tailoring from")
    product_id: str | None = Field(None, alias="productId", description="ID of the product to get tailoring for")
    product_key: str | None = Field(None, alias="productKey", description="Key of the product to get tailoring for")
    limit: int | None = Field(
        None,
        ge=1,
        le=500,
        description="Number of results requested. Default: 20, Minimum: 1, Maximum: 500",
    )
    offset: int | None = Field(
        None,
        ge=0,
        le=10000,
        description="Number of elements skipped. Default: 0, Maximum: 10000",
    )
    sort: list[str] | None = Field(
        None,
        description='Sort criteria for the results. Example: ["createdAt desc"]',
    )
    where: list[str] | None = Field(
        None,
        description='Query predicates specified as strings. Example: ["product(id=\\"product-123\\")"]',
    )
    expand: list[str] | None = Field(
        None,
        description='An array of reference paths to expand. Example: ["product", "store"]',
    )
    model_config = {"populate_by_name": True}


# ── Create ────────────────────────────────────────────────────────────────────

class CreateProductTailoringParams(BaseModel):
    key: str = Field(description="Key of the product tailoring entry to create")
    product_id: str | None = Field(None, alias="productId", description="ID of the product to create tailoring for")
    product_key: str | None = Field(None, alias="productKey", description="Key of the product to create tailoring for")
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store to create tailoring for")
    product: ProductReference | None = Field(None, description="Reference to the product to create tailoring for")
    store: StoreReference | None = Field(None, description="Reference to the store to create tailoring for")
    name: dict[str, str] = Field(description="Localized product name")
    description: dict[str, str] | None = Field(None, description="Localized product description")
    meta_title: dict[str, str] | None = Field(None, alias="metaTitle", description="Localized meta title")
    meta_description: dict[str, str] | None = Field(None, alias="metaDescription", description="Localized meta description")
    meta_keywords: dict[str, str] | None = Field(None, alias="metaKeywords", description="Localized meta keywords")
    slug: dict[str, str] | None = Field(None, description="Localized product slug")
    published: bool = Field(False, description="Whether the product tailoring is published")
    variants: list[TailoringVariantDraft] | None = Field(None, description="Product variants")
    attributes: list[AttributeDraft] | None = Field(None, description="Product attributes")
    custom_type: ProductTailoringTypeRef | None = Field(
        None,
        alias="customType",
        description="The Type that extends the product tailoring entry with custom fields",
    )
    model_config = {"populate_by_name": True}


# ── Update ────────────────────────────────────────────────────────────────────

class ProductTailoringUpdateAction(BaseModel):
    action: str = Field(description="The name of the update action to perform")
    model_config = {"extra": "allow"}


class UpdateProductTailoringParams(BaseModel):
    id: str | None = Field(None, description="The ID of the product tailoring entry to update")
    key: str | None = Field(None, description="The key of the product tailoring entry to update")
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store the product tailoring belongs to")
    product_id: str | None = Field(None, alias="productId", description="ID of the product to update tailoring for")
    product_key: str | None = Field(None, alias="productKey", description="Key of the product to update tailoring for")
    version: int = Field(description="Expected version of the product tailoring entry on which the changes should be applied")
    actions: list[ProductTailoringUpdateAction] = Field(
        description="Update actions to be performed on the product tailoring entry",
    )
    model_config = {"populate_by_name": True}
