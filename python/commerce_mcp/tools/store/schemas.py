from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


# ── Read ──────────────────────────────────────────────────────────────────────

class ReadStoreParams(BaseModel):
    id: str | None = Field(None, description="The ID of the store to fetch")
    key: str | None = Field(None, description="The key of the store to fetch")
    where: list[str] | None = Field(None, description='Query predicates for filtering stores. Example: ["name=\\"My Store\\""]')
    limit: int | None = Field(None, ge=1, le=500, description="Number of objects to return (1–500, default 10)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["createdAt desc"]')
    expand: list[str] | None = Field(None, description='Field paths to expand. Example: ["distributionChannels[*]", "supplyChannels[*]"]')


# ── Create ────────────────────────────────────────────────────────────────────

class _StoreCountryDraft(BaseModel):
    code: str = Field(description="Two-digit country code as per ISO 3166-1 alpha-2")


class _ChannelReference(BaseModel):
    type_id: Literal["channel"] = Field("channel", alias="typeId")
    key: str | None = None
    id: str | None = None
    model_config = {"populate_by_name": True}


class _ProductSelectionReference(BaseModel):
    type_id: Literal["product-selection"] = Field("product-selection", alias="typeId")
    key: str | None = None
    id: str | None = None
    model_config = {"populate_by_name": True}


class _ProductSelectionSettingDraft(BaseModel):
    product_selection: _ProductSelectionReference = Field(alias="productSelection", description="Reference to a Product Selection")
    active: bool | None = Field(None, description="If true, the Product Selection is active for the Store")
    model_config = {"populate_by_name": True}


class _TypeReference(BaseModel):
    type_id: Literal["type"] = Field("type", alias="typeId")
    key: str | None = None
    id: str | None = None
    model_config = {"populate_by_name": True}


class _CustomFields(BaseModel):
    type: _TypeReference
    fields: dict[str, Any] | None = None


class CreateStoreParams(BaseModel):
    key: str = Field(description="User-defined unique and immutable identifier for the Store. Min: 2, Max: 256, Pattern: ^[A-Za-z0-9_-]+$")
    name: dict[str, str] = Field(description="Name of the Store as a localized string")
    languages: list[str] | None = Field(None, description="Languages configured for the Store (locale strings)")
    countries: list[_StoreCountryDraft] | None = Field(None, description="Countries defined for the Store")
    distribution_channels: list[_ChannelReference] | None = Field(None, alias="distributionChannels", description="Product Distribution Channels allowed for the Store. Max: 100")
    supply_channels: list[_ChannelReference] | None = Field(None, alias="supplyChannels", description="Inventory Supply Channels allowed for the Store. Max: 100")
    product_selections: list[_ProductSelectionSettingDraft] | None = Field(None, alias="productSelections", description="Controls availability of Products for this Store via Product Selections. Max: 100")
    custom: _CustomFields | None = Field(None, description="Custom fields for the Store")
    model_config = {"populate_by_name": True}


# ── Update ────────────────────────────────────────────────────────────────────

class StoreUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateStoreParams(BaseModel):
    version: int = Field(description="Current version of the Store")
    actions: list[StoreUpdateAction] = Field(description="Update actions to be performed on the Store")
    id: str | None = Field(None, description="The ID of the store to update")
    key: str | None = Field(None, description="The key of the store to update")
