from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field

LocalizedString = dict[str, str]


class StoreReference(BaseModel):
    key: str
    type_id: Literal["store"] = Field("store", alias="typeId")
    model_config = {"populate_by_name": True}


class LineItemVariantPrice(BaseModel):
    value: dict[str, Any]
    model_config = {"populate_by_name": True}


class LineItemVariant(BaseModel):
    id: int
    sku: str | None = None
    prices: list[LineItemVariantPrice] | None = None
    model_config = {"populate_by_name": True}


class ImportLineItem(BaseModel):
    id: str
    product_id: str = Field(alias="productId")
    name: LocalizedString
    product_slug: LocalizedString | None = Field(None, alias="productSlug")
    variant: LineItemVariant
    quantity: int
    model_config = {"populate_by_name": True}


class TotalPrice(BaseModel):
    currency_code: str = Field(alias="currencyCode")
    cent_amount: int = Field(alias="centAmount")
    model_config = {"populate_by_name": True}


class ReadOrderParams(BaseModel):
    id: str | None = Field(None, description="The ID of the order to fetch")
    order_number: str | None = Field(
        None,
        alias="orderNumber",
        description="The order number of the order to fetch",
    )
    where: list[str] | None = Field(
        None,
        description='Query predicates specified as strings for filtering orders. Example: ["orderNumber=\\"1001\\""]',
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
        description="Key of the store to read orders from",
    )
    model_config = {"populate_by_name": True}


class CreateOrderParams(BaseModel):
    # Cart-based creation
    id: str | None = Field(None, description="The ID of the cart to create the order from")
    version: int = Field(description="The current version of the cart or quote")
    order_number: str | None = Field(
        None,
        alias="orderNumber",
        description="User-defined identifier of the Order",
    )
    store_key: str | None = Field(
        None,
        alias="storeKey",
        description="Key of the store to create the order in",
    )
    # Quote-based creation
    quote_id: str | None = Field(
        None,
        alias="quoteId",
        description="The ID of the quote to create the order from",
    )
    # Import parameters
    customer_id: str | None = Field(
        None,
        alias="customerId",
        description="ID of the customer that the Order belongs to",
    )
    customer_email: str | None = Field(
        None,
        alias="customerEmail",
        description="Email address of the Customer",
    )
    store: StoreReference | None = Field(
        None,
        description="Reference to a Store the Order belongs to",
    )
    line_items: list[ImportLineItem] | None = Field(
        None,
        alias="lineItems",
        description="Line items in the order",
    )
    total_price: TotalPrice | None = Field(
        None,
        alias="totalPrice",
        description="Total price of the order (required for import)",
    )
    model_config = {"populate_by_name": True}


class OrderUpdateAction(BaseModel):
    action: str = Field(description="The name of the update action to perform")
    model_config = {"extra": "allow"}


class UpdateOrderParams(BaseModel):
    id: str | None = Field(None, description="The ID of the order to update")
    order_number: str | None = Field(
        None,
        alias="orderNumber",
        description="The order number of the order to update",
    )
    version: int = Field(description="The current version of the order")
    store_key: str | None = Field(
        None,
        alias="storeKey",
        description="Key of the store the order belongs to",
    )
    actions: list[OrderUpdateAction] = Field(
        description='Array of update actions to perform on the order. Each action should have an "action" field and other fields specific to that action type.',
    )
    model_config = {"populate_by_name": True}
