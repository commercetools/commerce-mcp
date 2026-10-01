from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ReadInventoryParams(BaseModel):
    id: str | None = Field(None, description="The ID of the inventory entry to retrieve")
    key: str | None = Field(None, description="The key of the inventory entry to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of items to skip (0–10000)")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["sku asc"]')
    where: list[str] | None = Field(None, description='Query predicates. Example: ["sku=\\"SKU-123\\""]')
    expand: list[str] | None = Field(None, description='Reference paths to expand. Example: ["supplyChannel"]')


class ChannelReference(BaseModel):
    id: str = Field(description="ID of the supply channel")
    type_id: str = Field("channel", alias="typeId", description="Resource type identifier")
    model_config = {"populate_by_name": True}


class CreateInventoryParams(BaseModel):
    sku: str = Field(description="ProductVariant SKU for this inventory entry")
    quantity_on_stock: int = Field(alias="quantityOnStock", description="Current quantity on stock")
    key: str | None = Field(None, description="User-defined unique identifier")
    supply_channel: ChannelReference | None = Field(None, alias="supplyChannel", description="Reference to the supply channel")
    restockable_in_days: int | None = Field(None, alias="restockableInDays", description="Frequency in days between restock events")
    expected_delivery: str | None = Field(None, alias="expectedDelivery", description="ISO 8601 date of expected delivery")
    custom: dict[str, Any] | None = Field(None, description="Custom fields for the inventory entry")
    model_config = {"populate_by_name": True}


class InventoryUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateInventoryParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[InventoryUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the inventory entry to update")
    key: str | None = Field(None, description="The key of the inventory entry to update")
