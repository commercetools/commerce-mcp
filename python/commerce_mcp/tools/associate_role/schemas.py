from __future__ import annotations

from pydantic import BaseModel, Field


class ReadAssociateRoleParams(BaseModel):
    id: str | None = None
    key: str | None = None
    where: list[str] | None = None
    limit: int | None = Field(None, ge=1, le=500)
    offset: int | None = Field(None, ge=0)
    sort: list[str] | None = None
    expand: list[str] | None = None

    model_config = {"populate_by_name": True}


class CreateAssociateRoleParams(BaseModel):
    key: str
    buyer_assignable: bool = Field(alias="buyerAssignable")
    name: str | None = None
    permissions: list[str] | None = None
    custom: dict | None = None

    model_config = {"populate_by_name": True}


class UpdateAssociateRoleParams(BaseModel):
    id: str | None = None
    key: str | None = None
    version: int
    actions: list[dict]

    model_config = {"populate_by_name": True}
