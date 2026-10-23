from __future__ import annotations

from pydantic import BaseModel, Field


class ReadZoneParams(BaseModel):
    id: str | None = Field(None, description="The ID of the zone to retrieve")
    key: str | None = Field(None, description="The key of the zone to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of elements to skip (0–10000)")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["name asc"]')
    where: list[str] | None = Field(None, description='Query predicates. Example: ["name=\\"Europe\\""]')
    expand: list[str] | None = Field(None, description='Reference paths to expand. Example: ["locations"]')


class ZoneLocation(BaseModel):
    country: str = Field(description="Country code (ISO 3166-1 alpha-2)")
    state: str | None = Field(None, description="State or region within the country")


class CreateZoneParams(BaseModel):
    name: str = Field(description="Name of the zone")
    key: str | None = Field(None, description="User-defined unique identifier for the zone")
    description: str | None = Field(None, description="Description of the zone")
    locations: list[ZoneLocation] | None = Field(None, description="Locations that belong to the zone")


class ZoneUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateZoneParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[ZoneUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the zone to update")
    key: str | None = Field(None, description="The key of the zone to update")
