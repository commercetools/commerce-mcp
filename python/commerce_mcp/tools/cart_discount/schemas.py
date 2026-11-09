from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ReadCartDiscountParams(BaseModel):
    id: str | None = Field(None, description="The ID of the cart discount to fetch")
    key: str | None = Field(None, description="The key of the cart discount to fetch")
    where: list[str] | None = Field(
        None,
        description='Query predicates for filtering cart discounts. Example: ["name(en=\\"Black Friday Sale\\")"]',
    )
    limit: int | None = Field(None, ge=1, le=500, description="Number of results to return (1-500, default 10)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(
        None,
        description='Sort criteria. Example: ["name.en asc", "createdAt desc"]',
    )
    expand: list[str] | None = Field(
        None,
        description='Fields to expand. Example: ["references[*]"]',
    )


# CartDiscountValue schemas

class CartDiscountValueAbsolute(BaseModel):
    type: Literal["absolute"] = "absolute"
    money: list[dict[str, Any]] = Field(description="List of centPrecision money objects")


class CartDiscountValueRelative(BaseModel):
    type: Literal["relative"] = "relative"
    permyriad: int = Field(ge=0, le=10000, description="Permyriad value (e.g. 1000 = 10%)")


class CartDiscountValueFixed(BaseModel):
    type: Literal["fixed"] = "fixed"
    money: list[dict[str, Any]] = Field(description="List of centPrecision money objects")


class CartDiscountValueGiftLineItem(BaseModel):
    type: Literal["giftLineItem"] = "giftLineItem"
    product: dict[str, Any] = Field(description="Product reference with typeId='product' and id")
    variant_id: int = Field(alias="variantId", description="Variant ID of the gift product")
    distribution_channel: dict[str, Any] | None = Field(
        None, alias="distributionChannel", description="Distribution channel reference"
    )
    supply_channel: dict[str, Any] | None = Field(
        None, alias="supplyChannel", description="Supply channel reference"
    )
    model_config = {"populate_by_name": True}


# CartDiscountTarget schemas

class CartDiscountLineItemsTarget(BaseModel):
    type: Literal["lineItems"] = "lineItems"
    predicate: str = Field(description="Line item predicate")


class CartDiscountCustomLineItemsTarget(BaseModel):
    type: Literal["customLineItems"] = "customLineItems"
    predicate: str = Field(description="Custom line item predicate")


class CartDiscountShippingCostTarget(BaseModel):
    type: Literal["shipping"] = "shipping"


class CartDiscountTotalPriceTarget(BaseModel):
    type: Literal["totalPrice"] = "totalPrice"


class MultiBuyLineItemsTarget(BaseModel):
    type: Literal["multiBuyLineItems"] = "multiBuyLineItems"
    predicate: str = Field(description="Line item predicate")
    trigger_quantity: int = Field(alias="triggerQuantity", gt=0, description="Number of items required to trigger")
    discounted_quantity: int = Field(alias="discountedQuantity", gt=0, description="Number of items to discount")
    max_occurrence: int | None = Field(None, alias="maxOccurrence", gt=0, description="Maximum number of occurrences")
    selection_mode: str | None = Field(None, alias="selectionMode", description="Cheapest or MostExpensive")
    model_config = {"populate_by_name": True}


class MultiBuyCustomLineItemsTarget(BaseModel):
    type: Literal["multiBuyCustomLineItems"] = "multiBuyCustomLineItems"
    predicate: str = Field(description="Custom line item predicate")
    trigger_quantity: int = Field(alias="triggerQuantity", gt=0, description="Number of items required to trigger")
    discounted_quantity: int = Field(alias="discountedQuantity", gt=0, description="Number of items to discount")
    max_occurrence: int | None = Field(None, alias="maxOccurrence", gt=0, description="Maximum number of occurrences")
    selection_mode: str | None = Field(None, alias="selectionMode", description="Cheapest or MostExpensive")
    model_config = {"populate_by_name": True}


class CartDiscountPatternTarget(BaseModel):
    type: Literal["pattern"] = "pattern"
    components: list[dict[str, Any]] = Field(description="Pattern components")


class StoreKeyReference(BaseModel):
    type_id: Literal["store"] = Field("store", alias="typeId")
    key: str = Field(description="Store key")
    model_config = {"populate_by_name": True}


class CustomTypeIdReference(BaseModel):
    id: str = Field(description="ID of the custom type")
    type_id: Literal["type"] = Field("type", alias="typeId")
    model_config = {"populate_by_name": True}


class CustomFields(BaseModel):
    type: CustomTypeIdReference = Field(description="Reference to the custom type")
    fields: dict[str, Any] = Field(description="Custom field values")


class CreateCartDiscountParams(BaseModel):
    name: dict[str, str] = Field(description="Localized name of the CartDiscount")
    cart_predicate: str = Field(alias="cartPredicate", description="Valid Cart predicate")
    value: dict[str, Any] = Field(description="Type of Discount and its corresponding value")
    sort_order: str = Field(
        alias="sortOrder",
        description="Unique decimal value between 0 and 1 defining the application order",
    )
    key: str | None = Field(
        None,
        description="User-defined unique identifier (2-256 chars, alphanumeric with _ and -)",
    )
    description: dict[str, str] | None = Field(None, description="Localized description")
    target: dict[str, Any] | None = Field(None, description="Segment of the Cart that is discounted")
    is_active: bool | None = Field(None, alias="isActive", description="If true, discount is applied (default true)")
    valid_from: str | None = Field(None, alias="validFrom", description="ISO 8601 datetime from which discount is effective")
    valid_until: str | None = Field(None, alias="validUntil", description="ISO 8601 datetime until which discount is effective")
    requires_discount_code: bool | None = Field(
        None,
        alias="requiresDiscountCode",
        description="When true, a valid Discount Code must be provided (default false)",
    )
    stacking_mode: str | None = Field(
        None,
        alias="stackingMode",
        description="Stacking or StopAfterThisDiscount (default Stacking)",
    )
    stores: list[StoreKeyReference] | None = Field(
        None,
        description="Stores this discount applies to. If empty, applies to all stores.",
    )
    custom: CustomFields | None = Field(None, description="Custom fields for the Cart Discount")
    model_config = {"populate_by_name": True}


class CartDiscountUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateCartDiscountParams(BaseModel):
    id: str | None = Field(None, description="The ID of the cart discount to update")
    key: str | None = Field(None, description="The key of the cart discount to update")
    version: int = Field(description="The current version of the cart discount")
    actions: list[CartDiscountUpdateAction] = Field(description="Update actions to apply")
