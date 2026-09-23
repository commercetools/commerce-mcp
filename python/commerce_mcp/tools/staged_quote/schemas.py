from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ReadStagedQuoteParams(BaseModel):
    id: str | None = Field(None, description="ID of the staged quote to retrieve")
    key: str | None = Field(None, description="Key of the staged quote to retrieve")
    where: list[str] | None = Field(None, description="Query predicates for filtering staged quotes")
    sort: list[str] | None = Field(None, description="Sort expressions for ordering results")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results to return (max 500)")
    offset: int | None = Field(None, ge=0, description="Number of results to skip")
    expand: list[str] | None = Field(None, description="Fields to expand in the response")


class QuoteRequestReference(BaseModel):
    type_id: str = Field("quote-request", alias="typeId", description="Resource type identifier")
    id: str | None = Field(None, description="ID of the quote request")
    key: str | None = Field(None, description="Key of the quote request")
    model_config = {"populate_by_name": True}


class StateReference(BaseModel):
    type_id: str = Field("state", alias="typeId", description="Resource type identifier")
    id: str | None = Field(None, description="ID of the state")
    key: str | None = Field(None, description="Key of the state")
    model_config = {"populate_by_name": True}


class CustomTypeReference(BaseModel):
    key: str = Field(description="Key of the type")
    type_id: str | None = Field(None, alias="typeId", description="Resource type identifier")
    model_config = {"populate_by_name": True}


class CustomFields(BaseModel):
    type: CustomTypeReference = Field(description="Reference to the custom type")
    fields: dict[str, Any] | None = Field(None, description="Custom field values")


class CreateStagedQuoteParams(BaseModel):
    quote_request: QuoteRequestReference = Field(
        alias="quoteRequest",
        description="QuoteRequest from which the StagedQuote is created",
    )
    quote_request_version: int = Field(
        alias="quoteRequestVersion",
        description="Current version of the QuoteRequest",
    )
    key: str | None = Field(
        None,
        description="User-defined unique identifier for the StagedQuote (2-256 chars, alphanumeric with _ and -)",
    )
    quote_request_state_to_accepted: bool | None = Field(
        None,
        alias="quoteRequestStateToAccepted",
        description="If true, the quoteRequestState of the referenced QuoteRequest will be set to Accepted",
    )
    state: StateReference | None = Field(
        None,
        description="State of the Staged Quote. This reference can point to a State in a custom workflow",
    )
    custom: CustomFields | None = Field(
        None,
        description="Custom Fields to be added to the StagedQuote",
    )
    model_config = {"populate_by_name": True}


class StagedQuoteUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateStagedQuoteParams(BaseModel):
    id: str | None = Field(None, description="ID of the staged quote to update")
    key: str | None = Field(None, description="Key of the staged quote to update")
    version: int = Field(description="Current version of the staged quote for optimistic locking")
    actions: list[StagedQuoteUpdateAction] = Field(description="Update actions to apply to the staged quote")
