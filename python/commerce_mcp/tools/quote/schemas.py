from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


class StagedQuoteReference(BaseModel):
    id: str | None = Field(None, description="ID of the staged quote")
    key: str | None = Field(None, description="Key of the staged quote")
    type_id: Literal["staged-quote"] = Field("staged-quote", alias="typeId")
    model_config = {"populate_by_name": True}


class StateReference(BaseModel):
    id: str | None = Field(None, description="ID of the state")
    type_id: Literal["state"] = Field("state", alias="typeId")
    model_config = {"populate_by_name": True}


class CustomTypeReference(BaseModel):
    id: str | None = Field(None, description="ID of the custom type")
    key: str | None = Field(None, description="Key of the custom type")
    type_id: Literal["type"] = Field("type", alias="typeId")
    model_config = {"populate_by_name": True}


class CustomFields(BaseModel):
    type: CustomTypeReference
    fields: dict[str, Any] | None = None
    model_config = {"populate_by_name": True}


class ReadQuoteParams(BaseModel):
    id: str | None = Field(None, description="The ID of the quote to fetch")
    key: str | None = Field(None, description="The key of the quote to fetch")
    where: list[str] | None = Field(
        None,
        description='Query predicates specified as strings for filtering quotes. Example: ["customer(id=\\"1001\\")"]',
    )
    limit: int | None = Field(
        None,
        ge=1,
        le=500,
        description="A limit on the number of objects to be returned. Limit can range between 1 and 500, and the default is 10.",
    )
    offset: int | None = Field(
        None,
        ge=0,
        description="The number of items to skip before starting to collect the result set.",
    )
    sort: list[str] | None = Field(
        None,
        description='Sort criteria for the results. Example: ["createdAt desc"]',
    )
    expand: list[str] | None = Field(
        None,
        description='An array of field paths to expand. Example: ["customer", "quoteRequest"]',
    )
    store_key: str | None = Field(
        None,
        alias="storeKey",
        description="Key of the store to read the quote from",
    )
    business_unit_key: str | None = Field(
        None,
        alias="businessUnitKey",
        description="Key of the business unit to read the quote from",
    )
    associate_id: str | None = Field(
        None,
        alias="associateId",
        description="ID of the associate acting on behalf of the business unit",
    )
    model_config = {"populate_by_name": True}


class CreateQuoteParams(BaseModel):
    key: str | None = Field(None, description="User-defined unique identifier for the Quote")
    staged_quote: StagedQuoteReference = Field(alias="stagedQuote", description="Reference to the staged quote")
    staged_quote_version: int = Field(alias="stagedQuoteVersion", description="Current version of the staged quote")
    staged_quote_state_to_sent: bool = Field(
        False,
        alias="stagedQuoteStateToSent",
        description="If true, the stagedQuoteState of the referenced StagedQuote will be set to Sent",
    )
    state: StateReference | None = Field(None, description="Reference to a State")
    custom: CustomFields | None = Field(None, description="Custom fields for the quote")
    expand: list[str] | None = Field(
        None,
        description='An array of field paths to expand. Example: ["customer", "quoteRequest"]',
    )
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store to create the quote in")
    business_unit_key: str | None = Field(None, alias="businessUnitKey", description="Key of the business unit to create the quote in")
    associate_id: str | None = Field(None, alias="associateId", description="ID of the associate acting on behalf of the business unit")
    model_config = {"populate_by_name": True}


class QuoteUpdateAction(BaseModel):
    action: str = Field(description="The name of the update action to perform")
    model_config = {"extra": "allow"}


class UpdateQuoteParams(BaseModel):
    id: str | None = Field(None, description="The ID of the quote to update")
    key: str | None = Field(None, description="The key of the quote to update")
    version: int = Field(description="The expected version of the quote")
    actions: list[QuoteUpdateAction] = Field(description="Update actions to be performed on the quote")
    expand: list[str] | None = Field(
        None,
        description='An array of field paths to expand. Example: ["customer", "quoteRequest"]',
    )
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store to update the quote in")
    business_unit_key: str | None = Field(None, alias="businessUnitKey", description="Key of the business unit to update the quote in")
    associate_id: str | None = Field(None, alias="associateId", description="ID of the associate acting on behalf of the business unit")
    model_config = {"populate_by_name": True}
