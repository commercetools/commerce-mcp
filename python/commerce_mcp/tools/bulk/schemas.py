from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class BulkCreateItem(BaseModel):
    entity_type: str = Field(alias="entityType", description="Entity type to create (e.g. product, customer, cart, category, channel, discount-code, cart-discount, product-discount, customer-group, quote, quote-request, staged-quote, standalone-price, order, inventory, store, review, recurring-orders, shopping-lists, custom-objects, types, transactions, business-unit)")
    data: dict[str, Any] = Field(description="Create parameters for the entity type")
    model_config = {"populate_by_name": True}


class BulkCreateParams(BaseModel):
    items: list[BulkCreateItem] = Field(description="List of items to create in parallel")


class BulkUpdateItem(BaseModel):
    entity_type: str = Field(alias="entityType", description="Entity type to update (e.g. product, customer, cart, category, channel, discount-code, cart-discount, product-discount, customer-group, quote, quote-request, staged-quote, standalone-price, order, inventory, store, review, recurring-orders, shopping-lists, custom-objects, types, business-unit, product-selection, product-type)")
    data: dict[str, Any] = Field(description="Update parameters for the entity type (must include version and actions)")
    model_config = {"populate_by_name": True}


class BulkUpdateParams(BaseModel):
    items: list[BulkUpdateItem] = Field(description="List of items to update in parallel")
