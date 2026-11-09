from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


# ── Shared sub-models ──────────────────────────────────────────────────────────

class CartReference(BaseModel):
    id: str = Field(description="ID of the cart to reference")
    type_id: Literal["cart"] = Field("cart", alias="typeId")
    model_config = {"populate_by_name": True}


class CartCustomerGroup(BaseModel):
    id: str = Field(description="ID of the customer group")
    type_id: Literal["customer-group"] = Field("customer-group", alias="typeId")
    model_config = {"populate_by_name": True}


class CartStore(BaseModel):
    key: str = Field(description="Key of the store")
    type_id: Literal["store"] = Field("store", alias="typeId")
    model_config = {"populate_by_name": True}


class CartShippingMethod(BaseModel):
    id: str = Field(description="ID of the shipping method")
    type_id: Literal["shipping-method"] = Field("shipping-method", alias="typeId")
    model_config = {"populate_by_name": True}


class CartChannel(BaseModel):
    id: str = Field(description="ID of the channel")
    type_id: Literal["channel"] = Field("channel", alias="typeId")
    model_config = {"populate_by_name": True}


class CartTaxCategory(BaseModel):
    id: str = Field(description="ID of the tax category")
    type_id: Literal["tax-category"] = Field("tax-category", alias="typeId")
    model_config = {"populate_by_name": True}


class CartMoney(BaseModel):
    currency_code: str = Field(alias="currencyCode", description="ISO 4217 currency code")
    cent_amount: int = Field(alias="centAmount", description="Amount in the smallest currency unit (cents)")
    model_config = {"populate_by_name": True}


class LineItemDraft(BaseModel):
    product_id: str | None = Field(None, alias="productId", description="ID of the Product")
    variant_id: int | None = Field(None, alias="variantId", description="ID of the Product Variant")
    sku: str | None = Field(None, description="SKU of the Product Variant")
    quantity: int = Field(description="Quantity of the line item", ge=1)
    distribution_channel: CartChannel | None = Field(None, alias="distributionChannel", description="Reference to a distribution Channel")
    supply_channel: CartChannel | None = Field(None, alias="supplyChannel", description="Reference to a supply Channel")
    custom: dict[str, Any] | None = Field(None, description="Custom fields for the line item")
    external_tax_rate: dict[str, Any] | None = Field(None, alias="externalTaxRate", description="External tax rate for the line item")
    external_price: dict[str, Any] | None = Field(None, alias="externalPrice", description="External price for the line item")
    external_total_price: dict[str, Any] | None = Field(None, alias="externalTotalPrice", description="External total price for the line item")
    model_config = {"populate_by_name": True}


class CustomLineItemDraft(BaseModel):
    name: dict[str, str] = Field(description="Localized name of the custom line item")
    money: CartMoney = Field(description="Price of the custom line item")
    quantity: int = Field(description="Quantity of the custom line item", ge=1)
    slug: str = Field(description="Slug of the custom line item")
    tax_category: CartTaxCategory | None = Field(None, alias="taxCategory", description="Reference to a Tax Category")
    custom: dict[str, Any] | None = Field(None, description="Custom fields")
    external_tax_rate: dict[str, Any] | None = Field(None, alias="externalTaxRate", description="External tax rate")
    model_config = {"populate_by_name": True}


class CartUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


# ── Tool parameter models ──────────────────────────────────────────────────────

class ReadCartParams(BaseModel):
    id: str | None = Field(None, description="The ID of the cart to fetch")
    key: str | None = Field(None, description="The key of the cart to fetch")
    customer_id: str | None = Field(None, alias="customerId", description="The customer ID to fetch the cart for")
    where: list[str] | None = Field(None, description='Query predicates for filtering carts. Example: ["customerId=\\"1001\\""]')
    limit: int | None = Field(None, ge=1, le=500, description="Maximum number of results (1–500), default 10")
    offset: int | None = Field(None, ge=0, description="Number of items to skip before starting to collect the result set")
    sort: list[str] | None = Field(None, description='Sort criteria for the results. Example: ["createdAt desc"]')
    expand: list[str] | None = Field(None, description='Fields to expand. Example: ["customer", "lineItems[*].variant"]')
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store to read the cart from (admin context only)")
    model_config = {"populate_by_name": True}


class CreateCartParams(BaseModel):
    currency: str = Field(description="ISO 4217 currency code for the cart")
    customer_email: str | None = Field(None, alias="customerEmail", description="Email address of the Customer")
    customer_id: str | None = Field(None, alias="customerId", description="ID of the customer that the Cart belongs to")
    customer_group: CartCustomerGroup | None = Field(None, alias="customerGroup", description="Reference to a Customer Group")
    anonymous_id: str | None = Field(None, alias="anonymousId", description="Anonymous session ID")
    country: str | None = Field(None, description="Country for the cart")
    inventory_mode: Literal["None", "TrackOnly", "ReserveOnOrder"] | None = Field(None, alias="inventoryMode", description="Inventory mode of the cart")
    tax_mode: Literal["Platform", "External", "ExternalAmount", "Disabled"] | None = Field(None, alias="taxMode", description="Tax mode of the cart")
    tax_rounding_mode: Literal["HalfEven", "HalfUp", "HalfDown"] | None = Field(None, alias="taxRoundingMode", description="Tax rounding mode of the cart")
    tax_calculation_mode: Literal["LineItemLevel", "UnitPriceLevel"] | None = Field(None, alias="taxCalculationMode", description="Tax calculation mode of the cart")
    store: CartStore | None = Field(None, description="Reference to a Store")
    billing_address: dict[str, Any] | None = Field(None, alias="billingAddress", description="Billing address for the cart")
    shipping_address: dict[str, Any] | None = Field(None, alias="shippingAddress", description="Shipping address for the cart")
    shipping_method: CartShippingMethod | None = Field(None, alias="shippingMethod", description="Reference to a Shipping Method")
    shipping_mode: Literal["Single", "Multiple"] | None = Field(None, alias="shippingMode", description="Shipping mode of the cart")
    line_items: list[LineItemDraft] | None = Field(None, alias="lineItems", description="Line items to add to the cart")
    custom_line_items: list[CustomLineItemDraft] | None = Field(None, alias="customLineItems", description="Custom line items to add to the cart")
    discount_codes: list[str] | None = Field(None, alias="discountCodes", description="Discount codes to apply to the cart")
    key: str | None = Field(None, description="User-defined unique identifier of the Cart")
    locale: str | None = Field(None, description="Locale for the cart")
    origin: Literal["Customer", "Merchant"] | None = Field(None, description="Origin of the cart")
    custom: dict[str, Any] | None = Field(None, description="Custom fields for the cart")
    model_config = {"populate_by_name": True}


class ReplicateCartParams(BaseModel):
    reference: CartReference = Field(description="Reference to the cart to replicate")
    key: str | None = Field(None, description="User-defined unique identifier for the new replicated cart")
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store to create the replicated cart in")
    model_config = {"populate_by_name": True}


class UpdateCartParams(BaseModel):
    id: str | None = Field(None, description="The ID of the cart to update")
    key: str | None = Field(None, description="The key of the cart to update")
    version: int = Field(description="The current version of the cart")
    actions: list[CartUpdateAction] = Field(default_factory=list, description="Array of update actions to perform on the cart")
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store the cart belongs to")
    model_config = {"populate_by_name": True}
