from __future__ import annotations

from pydantic import BaseModel, Field


class ReadOrderEditParams(BaseModel):
    id: str | None = None
    key: str | None = None
    where: list[str] | None = None
    limit: int | None = Field(None, ge=1, le=500)
    offset: int | None = Field(None, ge=0)
    sort: list[str] | None = None
    expand: list[str] | None = None

    model_config = {"populate_by_name": True}


class CreateOrderEditParams(BaseModel):
    resource: dict
    staged_actions: list[dict] | None = Field(None, alias="stagedActions")
    key: str | None = None
    comment: str | None = None
    dry_run: bool | None = Field(None, alias="dryRun")
    custom: dict | None = None

    model_config = {"populate_by_name": True}


class UpdateOrderEditParams(BaseModel):
    id: str | None = None
    key: str | None = None
    version: int
    actions: list[dict]
    dry_run: bool | None = Field(None, alias="dryRun")

    model_config = {"populate_by_name": True}


class ApplyOrderEditParams(BaseModel):
    id: str
    edit_version: int = Field(alias="editVersion")
    resource_version: int = Field(alias="resourceVersion")

    model_config = {"populate_by_name": True}
