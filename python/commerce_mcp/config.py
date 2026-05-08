from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


class ResourceActions(BaseModel):
    read: bool = False
    create: bool = False
    update: bool = False


class Actions(BaseModel):
    """Permission matrix — mirrors TypeScript Actions type.
    Set a permission to True to enable the corresponding tool category.
    """
    business_unit: ResourceActions | None = Field(None, alias="business-unit")
    products: ResourceActions | None = None
    project: ResourceActions | None = None
    product_search: ResourceActions | None = Field(None, alias="product-search")
    category: ResourceActions | None = None
    product_selection: ResourceActions | None = Field(None, alias="product-selection")
    order: ResourceActions | None = None
    cart: ResourceActions | None = None
    customer: ResourceActions | None = None
    customer_group: ResourceActions | None = Field(None, alias="customer-group")
    standalone_price: ResourceActions | None = Field(None, alias="standalone-price")
    product_discount: ResourceActions | None = Field(None, alias="product-discount")
    cart_discount: ResourceActions | None = Field(None, alias="cart-discount")
    discount_code: ResourceActions | None = Field(None, alias="discount-code")
    product_type: ResourceActions | None = Field(None, alias="product-type")
    bulk: ResourceActions | None = None
    inventory: ResourceActions | None = None
    store: ResourceActions | None = None
    review: ResourceActions | None = None
    tax_category: ResourceActions | None = Field(None, alias="tax-category")
    shipping_methods: ResourceActions | None = Field(None, alias="shipping-methods")
    payments: ResourceActions | None = None
    zones: ResourceActions | None = None
    product_tailoring: ResourceActions | None = Field(None, alias="product-tailoring")
    payment_methods: ResourceActions | None = Field(None, alias="payment-methods")
    recurring_orders: ResourceActions | None = Field(None, alias="recurring-orders")
    shopping_lists: ResourceActions | None = Field(None, alias="shopping-lists")
    extensions: ResourceActions | None = None
    subscriptions: ResourceActions | None = None
    custom_objects: ResourceActions | None = Field(None, alias="custom-objects")
    payment_intents: ResourceActions | None = Field(None, alias="payment-intents")
    transactions: ResourceActions | None = None
    types: ResourceActions | None = None
    channel: ResourceActions | None = None
    quote: ResourceActions | None = None
    quote_request: ResourceActions | None = Field(None, alias="quote-request")
    staged_quote: ResourceActions | None = Field(None, alias="staged-quote")

    model_config = {"populate_by_name": True}

    def all_enabled() -> "Actions":
        """Returns an Actions object with all permissions enabled."""
        ra = ResourceActions(read=True, create=True, update=True)
        return Actions(**{f.alias or name: ra for name, f in Actions.model_fields.items()})

    def read_only() -> "Actions":
        """Returns an Actions object with all read permissions enabled."""
        ra = ResourceActions(read=True)
        return Actions(**{f.alias or name: ra for name, f in Actions.model_fields.items()})


class CTContext(BaseModel):
    """Runtime context applied to all requests. Mirrors TypeScript Context type."""
    customer_id: str | None = None
    store_key: str | None = None
    distribution_channel_id: str | None = None
    supply_channel_id: str | None = None
    is_admin: bool = False
    cart_id: str | None = None
    business_unit_key: str | None = None
    dynamic_tool_loading_threshold: int = 30
    session_id: str | None = None
    logging: bool = False


class FieldFilteringConfig(BaseModel):
    filter_paths: list[str] = Field(default_factory=list)
    redact_paths: list[str] = Field(default_factory=list)
    filter_properties: list[str] = Field(default_factory=list)
    whitelist_paths: list[str] = Field(default_factory=list)
    filter_includes: list[str] = Field(default_factory=list)
    case_sensitive: bool = False


class CustomTool(BaseModel):
    method: str
    name: str
    description: str
    parameters: Any  # Pydantic model class
    handler: Any     # async callable
    actions: dict[str, dict[str, bool]] = Field(default_factory=dict)


class Configuration(BaseModel):
    """Top-level configuration for the commerce-mcp server."""
    actions: Actions | None = None
    context: CTContext = Field(default_factory=CTContext)
    custom_tools: list[CustomTool] = Field(default_factory=list)
    field_filtering: FieldFilteringConfig | None = None


# ── Auth ──────────────────────────────────────────────────────────────────────

class _BaseAuth(BaseModel):
    auth_url: str
    api_url: str
    project_key: str


class ClientCredentialsAuth(_BaseAuth):
    type: Literal["client_credentials"] = "client_credentials"
    client_id: str
    client_secret: str


class ExistingTokenAuth(_BaseAuth):
    type: Literal["auth_token"] = "auth_token"
    access_token: str
    client_id: str | None = None
    client_secret: str | None = None


AuthConfig = ClientCredentialsAuth | ExistingTokenAuth
