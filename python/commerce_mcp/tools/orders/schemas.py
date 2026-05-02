from __future__ import annotations

from pydantic import BaseModel, Field


class ReadOrderParams(BaseModel):
    id: str | None = Field(None, description="Order ID")
    order_number: str | None = Field(None, description="Order number")
    limit: int = Field(20, ge=1, le=500, description="Maximum number of results (1–500)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    where: list[str] | None = Field(None, description="Query predicates")


class CreateOrderParams(BaseModel):
    cart_id: str = Field(description="Cart ID to convert to an order")
    version: int = Field(description="Cart version for optimistic locking")


class UpdateOrderParams(BaseModel):
    id: str = Field(description="Order ID")
    version: int = Field(description="Current order version for optimistic locking")
    actions: list[dict] = Field(default_factory=list, description="Update actions to apply")
