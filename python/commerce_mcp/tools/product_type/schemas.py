from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class ReadProductTypeParams(BaseModel):
    id: str | None = Field(None, description="The ID of the product type to retrieve")
    expand: list[str] | None = Field(
        None, description='An array of field paths to expand. Example: ["attributes[*].type"]'
    )
    limit: int | None = Field(
        None, ge=1, le=500, description="Number of product types to return (1–500, default 10)"
    )
    offset: int | None = Field(
        None, ge=0, description="Number of items to skip before starting to collect the result set"
    )
    sort: list[str] | None = Field(
        None, description='Sort criteria. Example: ["name asc", "createdAt desc"]'
    )
    where: list[str] | None = Field(
        None, description='Query predicates. Example: ["name = \\"Standard product type\\""]'
    )


class AttributeType(BaseModel):
    name: str = Field(description="The type name (e.g., text, number, boolean, enum, etc.)")
    model_config = {"extra": "allow"}


class AttributeDefinition(BaseModel):
    name: str = Field(description="The name of the attribute")
    label: dict[str, str] = Field(description="The localized label for the attribute")
    is_required: bool | None = Field(
        None, alias="isRequired", description="Whether the attribute is required"
    )
    is_searchable: bool | None = Field(
        None, alias="isSearchable", description="Whether the attribute is searchable"
    )
    type: AttributeType = Field(description="The type definition of the attribute")
    attribute_constraint: str | None = Field(
        None,
        alias="attributeConstraint",
        description="The constraint of the attribute (None, Unique, CombinationUnique, SameForAll)",
    )
    input_tip: dict[str, str] | None = Field(
        None, alias="inputTip", description="The input tip for the attribute"
    )
    input_hint: str | None = Field(
        None, alias="inputHint", description="The input hint for the attribute (SingleLine, MultiLine)"
    )
    model_config = {"populate_by_name": True}


class CreateProductTypeParams(BaseModel):
    key: str = Field(description="The unique key of the product type")
    name: str = Field(description="The name of the product type")
    description: str = Field(description="The description of the product type")
    attributes: list[AttributeDefinition] | None = Field(
        None, description="The attributes of the product type"
    )


class ProductTypeUpdateAction(BaseModel):
    action: str = Field(description="The name of the update action to perform")
    model_config = {"extra": "allow"}


class UpdateProductTypeParams(BaseModel):
    id: str = Field(description="The ID of the product type to update")
    version: int = Field(description="The current version of the product type")
    actions: list[ProductTypeUpdateAction] = Field(
        description="Array of update actions to perform on the product type"
    )
