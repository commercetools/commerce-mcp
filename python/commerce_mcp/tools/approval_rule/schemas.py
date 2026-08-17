from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class ReadApprovalRuleParams(BaseModel):
    id: str | None = None
    key: str | None = None
    where: list[str] | None = None
    limit: int | None = Field(None, ge=1, le=500)
    offset: int | None = Field(None, ge=0)
    sort: list[str] | None = None
    expand: list[str] | None = None
    associate_id: str | None = Field(None, alias="associateId")
    business_unit_key: str | None = Field(None, alias="businessUnitKey")

    model_config = {"populate_by_name": True}


class CreateApprovalRuleParams(BaseModel):
    name: str
    predicate: str
    approvers: dict
    requesters: list[dict]
    status: Literal["Active", "Inactive"]
    key: str | None = None
    description: str | None = None
    associate_id: str | None = Field(None, alias="associateId")
    business_unit_key: str | None = Field(None, alias="businessUnitKey")

    model_config = {"populate_by_name": True}


class UpdateApprovalRuleParams(BaseModel):
    id: str | None = None
    key: str | None = None
    version: int
    actions: list[dict]
    associate_id: str | None = Field(None, alias="associateId")
    business_unit_key: str | None = Field(None, alias="businessUnitKey")

    model_config = {"populate_by_name": True}
