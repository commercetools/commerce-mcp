from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ReadCustomerGroupParams(BaseModel):
    id: str | None = Field(None, description="The ID of the customer group to retrieve")
    key: str | None = Field(None, description="The key of the customer group to retrieve")
    where: list[str] | None = Field(None, description='Query predicates. Example: ["name=\\"VIP\\""]')
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["name asc"]')
    expand: list[str] | None = Field(None, description='Reference paths to expand')


class CreateCustomerGroupParams(BaseModel):
    group_name: str = Field(alias="groupName", description="Name of the customer group")
    key: str | None = Field(None, description="User-defined unique identifier (2–256 alphanumeric chars)")
    custom: dict[str, Any] | None = Field(None, description="Custom fields")
    model_config = {"populate_by_name": True}


class CustomerGroupUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateCustomerGroupParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[CustomerGroupUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the customer group to update")
    key: str | None = Field(None, description="The key of the customer group to update")
