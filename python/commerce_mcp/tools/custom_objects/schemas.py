from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ReadCustomObjectParams(BaseModel):
    container: str | None = Field(None, description="Container name to query objects in")
    key: str | None = Field(None, description="Key of the custom object (requires container)")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of items to skip (0–10000)")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["createdAt desc"]')
    where: list[str] | None = Field(None, description='Query predicates. Example: ["container=\\"my-app\\""]')
    expand: list[str] | None = Field(None, description='Reference paths to expand')


class CreateCustomObjectParams(BaseModel):
    container: str = Field(description="Container name (alphanumeric + dash, up to 256 chars)")
    key: str = Field(description="Key identifying the object within the container (1–256 chars)")
    value: Any = Field(description="Any valid JSON value to store")
    version: int | None = Field(None, description="Version for optimistic locking on update")


class UpdateCustomObjectParams(BaseModel):
    container: str = Field(description="Container name of the object to update")
    key: str = Field(description="Key of the object to update")
    value: Any = Field(description="New value to store")
    version: int | None = Field(None, description="Version for optimistic locking")
