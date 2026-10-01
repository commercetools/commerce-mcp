from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


class CartReference(BaseModel):
    id: str
    type_id: Literal["cart"] = Field("cart", alias="typeId")
    model_config = {"populate_by_name": True}


class ReadQuoteRequestParams(BaseModel):
    id: str | None = Field(None, description="The ID of the quote request to fetch")
    key: str | None = Field(None, description="The key of the quote request to fetch")
    customer_id: str | None = Field(
        None,
        alias="customerId",
        description="The customer ID to fetch the quote request for",
    )
    where: list[str] | None = Field(
        None,
        description='Query predicates specified as strings for filtering quote requests. Example: ["customerId=\\"1001\\""]',
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
        description='An array of field paths to expand. Example: ["customer", "lineItems[*].variant"]',
    )
    store_key: str | None = Field(
        None,
        alias="storeKey",
        description="Key of the store to read the quote request from",
    )
    model_config = {"populate_by_name": True}


class CreateQuoteRequestParams(BaseModel):
    cart: CartReference = Field(description="Reference to the cart to create the quote request from")
    cart_version: int = Field(alias="cartVersion", description="Version of the cart to create the quote request from")
    comment: str | None = Field(None, description="Comment describing the quote request")
    custom: dict[str, Any] | None = Field(None, description="Custom fields for the quote request")
    key: str | None = Field(None, description="User-defined unique identifier of the quote request")
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store to create the quote request in")
    model_config = {"populate_by_name": True}


class QuoteRequestUpdateAction(BaseModel):
    action: str = Field(description="The name of the update action to perform")
    model_config = {"extra": "allow"}


class UpdateQuoteRequestParams(BaseModel):
    id: str | None = Field(None, description="The ID of the quote request to update")
    key: str | None = Field(None, description="The key of the quote request to update")
    version: int = Field(description="The current version of the quote request")
    actions: list[QuoteRequestUpdateAction] = Field(
        description='Array of update actions to perform on the quote request. Each action should have an "action" field and other fields specific to that action type.'
    )
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store the quote request belongs to")
    model_config = {"populate_by_name": True}
