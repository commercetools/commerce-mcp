from __future__ import annotations

from pydantic import BaseModel, Field


class ReadCartParams(BaseModel):
    id: str | None = Field(None, description="Cart ID")
    limit: int = Field(10, ge=1, le=500, description="Maximum number of results (1–500)")


class CreateCartParams(BaseModel):
    currency: str = Field(description="ISO 4217 currency code, e.g. USD")
    line_items: list[dict] | None = Field(None, description="Initial line items to add")


class UpdateCartParams(BaseModel):
    id: str = Field(description="Cart ID")
    version: int = Field(description="Current cart version for optimistic locking")
    actions: list[dict] = Field(default_factory=list, description="Update actions to apply")
