from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# ── Read ──────────────────────────────────────────────────────────────────────

class ReadCategoryParams(BaseModel):
    id: str | None = Field(None, description="The ID of the category to fetch")
    key: str | None = Field(None, description="The key of the category to fetch")
    where: list[str] | None = Field(None, description='Query predicates for filtering categories. Example: ["name(en = \\"Clothes\\")"]')
    limit: int | None = Field(None, ge=1, le=500, description="Number of objects to return (1–500, default 10)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["name.en asc", "createdAt desc"]')
    expand: list[str] | None = Field(None, description='Field paths to expand. Example: ["parent", "ancestors[*]"]')


# ── Create ────────────────────────────────────────────────────────────────────

class _AssetSource(BaseModel):
    uri: str
    key: str | None = None
    dimensions: dict[str, int] | None = None
    content_type: str | None = Field(None, alias="contentType")
    model_config = {"populate_by_name": True}


class _Asset(BaseModel):
    sources: list[_AssetSource]
    name: dict[str, str]
    key: str | None = None
    description: dict[str, str] | None = None
    tags: list[str] | None = None


class _CategoryReference(BaseModel):
    id: str
    type_id: str = Field("category", alias="typeId")
    model_config = {"populate_by_name": True}


class _TypeReference(BaseModel):
    id: str
    type_id: str = Field("type", alias="typeId")
    model_config = {"populate_by_name": True}


class _CustomFields(BaseModel):
    type: _TypeReference
    fields: dict[str, Any]


class CreateCategoryParams(BaseModel):
    name: dict[str, str] = Field(description="Localized name of the category")
    slug: dict[str, str] = Field(description="Localized URL slug (unique across the project). Pattern: ^[A-Za-z0-9_-]{2,256}+$")
    description: dict[str, str] | None = Field(None, description="Localized description of the category")
    key: str | None = Field(None, description="User-defined unique identifier. Pattern: ^[A-Za-z0-9_-]+$")
    external_id: str | None = Field(None, alias="externalId", description="Additional identifier for external systems")
    parent: _CategoryReference | None = Field(None, description="Reference to the parent category")
    order_hint: str | None = Field(None, alias="orderHint", description="Decimal value between 0 and 1 for ordering categories at the same level")
    meta_title: dict[str, str] | None = Field(None, alias="metaTitle", description="SEO meta title")
    meta_description: dict[str, str] | None = Field(None, alias="metaDescription", description="SEO meta description")
    meta_keywords: dict[str, str] | None = Field(None, alias="metaKeywords", description="SEO meta keywords")
    assets: list[_Asset] | None = Field(None, description="Media related to the category")
    custom: _CustomFields | None = Field(None, description="Custom fields for the category")
    model_config = {"populate_by_name": True}


# ── Update ────────────────────────────────────────────────────────────────────

class CategoryUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateCategoryParams(BaseModel):
    version: int = Field(description="The current version of the category")
    actions: list[CategoryUpdateAction] = Field(description="Array of update actions to perform")
    id: str | None = Field(None, description="The ID of the category to update")
    key: str | None = Field(None, description="The key of the category to update")
