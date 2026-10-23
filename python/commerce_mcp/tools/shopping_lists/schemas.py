from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field

LocalizedString = dict[str, str]


class CustomerReference(BaseModel):
    id: str
    type_id: Literal["customer"] = Field("customer", alias="typeId")
    model_config = {"populate_by_name": True}


class StoreKeyReference(BaseModel):
    key: str
    type_id: Literal["store"] = Field("store", alias="typeId")
    model_config = {"populate_by_name": True}


class BusinessUnitKeyReference(BaseModel):
    key: str
    type_id: Literal["business-unit"] = Field("business-unit", alias="typeId")
    model_config = {"populate_by_name": True}


class LineItemDraft(BaseModel):
    product_id: str | None = Field(None, alias="productId", description="ID of the Product")
    sku: str | None = Field(None, description="SKU of the Product Variant")
    variant_id: int | None = Field(None, alias="variantId", description="ID of the Product Variant")
    quantity: int = Field(description="Quantity of the line item", ge=1)
    added_at: str | None = Field(None, alias="addedAt", description="Date and time (UTC) the line item was added to the ShoppingList")
    custom: dict[str, Any] | None = Field(None, description="Custom fields for the line item")
    model_config = {"populate_by_name": True}


class TextLineItemDraft(BaseModel):
    name: LocalizedString = Field(description="Name of the text line item (localized string)")
    description: LocalizedString | None = Field(None, description="Description of the text line item (localized string)")
    quantity: int = Field(description="Quantity of the text line item", ge=1)
    added_at: str | None = Field(None, alias="addedAt", description="Date and time (UTC) the text line item was added to the ShoppingList")
    custom: dict[str, Any] | None = Field(None, description="Custom fields for the text line item")
    model_config = {"populate_by_name": True}


class CustomTypeReference(BaseModel):
    id: str
    type_id: Literal["type"] = Field("type", alias="typeId")
    model_config = {"populate_by_name": True}


class CustomFields(BaseModel):
    type: CustomTypeReference
    fields: dict[str, Any]
    model_config = {"populate_by_name": True}


class ReadShoppingListParams(BaseModel):
    id: str | None = Field(None, description="The ID of the shopping list to retrieve")
    key: str | None = Field(None, description="The key of the shopping list to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results requested. Default: 20, Minimum: 0, Maximum: 500")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of elements skipped. Default: 0, Maximum: 10000")
    sort: list[str] | None = Field(None, description='Sort criteria for the results. Example: ["name asc", "createdAt desc"]')
    where: list[str] | None = Field(None, description='Query predicates specified as strings. Example: ["customer(id=\\"customer-123\\")"]')
    expand: list[str] | None = Field(None, description='An array of reference paths to expand. Example: ["customer", "lineItems[*].variant"]')
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store to read the shopping list from")
    model_config = {"populate_by_name": True}


class CreateShoppingListParams(BaseModel):
    key: str | None = Field(None, min_length=2, max_length=256, description="User-defined unique identifier for the shopping list")
    name: LocalizedString = Field(description="Name of the shopping list (localized string)")
    slug: LocalizedString | None = Field(None, description="Human-readable identifiers usually used as deep-link URL to the related ShoppingList")
    description: LocalizedString | None = Field(None, description="Description of the shopping list (localized string)")
    customer: CustomerReference | None = Field(None, description="Reference to a Customer associated with the ShoppingList")
    store: StoreKeyReference | None = Field(None, description="Reference to a Store the ShoppingList is associated with")
    business_unit: BusinessUnitKeyReference | None = Field(None, alias="businessUnit", description="Reference to a Business Unit the ShoppingList is associated with")
    line_items: list[LineItemDraft] | None = Field(None, alias="lineItems", description="Line Items (containing Products) of the ShoppingList")
    text_line_items: list[TextLineItemDraft] | None = Field(None, alias="textLineItems", description="Line Items (containing text values) of the ShoppingList")
    delete_days_after_last_modification: int | None = Field(None, alias="deleteDaysAfterLastModification", ge=1, le=365250, description="Number of days after the last modification before a ShoppingList is deleted")
    anonymous_id: str | None = Field(None, alias="anonymousId", description="Identifies ShoppingLists belonging to an anonymous session")
    custom: CustomFields | None = Field(None, description="Custom fields for the shopping list")
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store to create the shopping list in")
    model_config = {"populate_by_name": True}


class ShoppingListUpdateAction(BaseModel):
    action: str = Field(description="The name of the update action to perform")
    model_config = {"extra": "allow"}


class UpdateShoppingListParams(BaseModel):
    id: str | None = Field(None, description="The ID of the shopping list to update")
    key: str | None = Field(None, description="The key of the shopping list to update")
    version: int = Field(description="Expected version of the shopping list on which the changes should be applied")
    actions: list[ShoppingListUpdateAction] = Field(description='Update actions to be performed on the shopping list')
    store_key: str | None = Field(None, alias="storeKey", description="Key of the store the shopping list belongs to")
    model_config = {"populate_by_name": True}
