from __future__ import annotations

from pydantic import BaseModel, Field


class ReadApprovalFlowParams(BaseModel):
    id: str | None = None
    where: list[str] | None = None
    limit: int | None = Field(None, ge=1, le=500)
    offset: int | None = Field(None, ge=0)
    sort: list[str] | None = None
    expand: list[str] | None = None
    associate_id: str | None = Field(None, alias="associateId")
    business_unit_key: str | None = Field(None, alias="businessUnitKey")

    model_config = {"populate_by_name": True}


class UpdateApprovalFlowParams(BaseModel):
    id: str
    version: int
    actions: list[dict]
    associate_id: str | None = Field(None, alias="associateId")
    business_unit_key: str | None = Field(None, alias="businessUnitKey")

    model_config = {"populate_by_name": True}
