from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ReadTypeParams(BaseModel):
    id: str | None = Field(None, description="The ID of the type to retrieve")
    key: str | None = Field(None, description="The key of the type to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of elements to skip (0–10000)")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["name asc"]')
    where: list[str] | None = Field(None, description='Query predicates. Example: ["key=\\"my-type\\""]')
    expand: list[str] | None = Field(None, description='Reference paths to expand. Example: ["fieldDefinitions[*].type"]')


class FieldDefinition(BaseModel):
    name: str = Field(description="Name of the field definition")
    label: dict[str, str] = Field(description="Localized label for the field definition")
    type: dict[str, Any] = Field(description="Type of the field definition (e.g. {name: 'String'})")
    required: bool | None = Field(None, description="Whether the field is required")
    input_hint: Literal["SingleLine", "MultiLine"] | None = Field(None, alias="inputHint", description="Input hint for String fields")
    model_config = {"populate_by_name": True}


class CreateTypeParams(BaseModel):
    key: str = Field(description="User-defined unique identifier for the type (2–256 alphanumeric chars)")
    name: str = Field(description="Name of the type")
    resource_type_ids: list[str] = Field(alias="resourceTypeIds", description='Resource types to customize (e.g. ["category", "product"])')
    description: str | None = Field(None, description="Description of the type")
    field_definitions: list[FieldDefinition] | None = Field(None, alias="fieldDefinitions", description="Field definitions for the type")
    model_config = {"populate_by_name": True}


class TypeUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateTypeParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[TypeUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the type to update")
    key: str | None = Field(None, description="The key of the type to update")
