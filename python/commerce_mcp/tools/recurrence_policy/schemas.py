from __future__ import annotations

from pydantic import BaseModel, Field


class ReadRecurrencePolicyParams(BaseModel):
    id: str | None = None
    key: str | None = None
    where: list[str] | None = None
    limit: int | None = Field(None, ge=1, le=500)
    offset: int | None = Field(None, ge=0)
    sort: list[str] | None = None
    expand: list[str] | None = None

    model_config = {"populate_by_name": True}


class CreateRecurrencePolicyParams(BaseModel):
    key: str
    schedule: dict
    name: dict[str, str] | None = None
    description: dict[str, str] | None = None

    model_config = {"populate_by_name": True}


class UpdateRecurrencePolicyParams(BaseModel):
    id: str | None = None
    key: str | None = None
    version: int
    actions: list[dict]

    model_config = {"populate_by_name": True}
