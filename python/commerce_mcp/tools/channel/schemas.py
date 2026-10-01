from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ReadChannelParams(BaseModel):
    id: str | None = Field(None, description="The ID of the channel to fetch")
    key: str | None = Field(None, description="The key of the channel to fetch")
    where: list[str] | None = Field(None, description='Query predicates. Example: ["roles contains any \\"InventorySupply\\""]')
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["name.en asc"]')
    expand: list[str] | None = Field(None, description='Field paths to expand. Example: ["custom.type"]')


ChannelRole = Literal["InventorySupply", "ProductDistribution", "OrderExport", "OrderImport", "Primary"]


class GeoLocation(BaseModel):
    type: Literal["Point"] = Field(description="GeoJSON type — must be 'Point'")
    coordinates: list[float] = Field(description="[longitude, latitude]")


class CreateChannelParams(BaseModel):
    key: str = Field(description="User-defined unique identifier for the channel (1–256 chars)")
    roles: list[ChannelRole] = Field(description="Roles of the channel (at least one required)")
    name: dict[str, str] | None = Field(None, description="Localized name of the channel")
    description: dict[str, str] | None = Field(None, description="Localized description of the channel")
    address: dict[str, Any] | None = Field(None, description="Address where the channel is located")
    geo_location: GeoLocation | None = Field(None, alias="geoLocation", description="GeoJSON Point for the channel location")
    custom: dict[str, Any] | None = Field(None, description="Custom fields for the channel")
    model_config = {"populate_by_name": True}


class ChannelUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateChannelParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[ChannelUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the channel to update")
    key: str | None = Field(None, description="The key of the channel to update")
