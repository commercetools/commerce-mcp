from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ReadPaymentMethodsParams(BaseModel):
    id: str | None = Field(None, description="The ID of the payment method to fetch")
    key: str | None = Field(None, description="The key of the payment method to fetch")
    where: list[str] | None = Field(None, description="Query predicates for filtering payment methods")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 10)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(None, description="Sort criteria for the results")
    expand: list[str] | None = Field(None, description="Fields to expand in the response")


class CustomerRef(BaseModel):
    id: str = Field(description="ID of the customer")
    type_id: str = Field("customer", alias="typeId")
    model_config = {"populate_by_name": True}


class BusinessUnitRef(BaseModel):
    id: str = Field(description="ID of the business unit")
    type_id: str = Field("business-unit", alias="typeId")
    model_config = {"populate_by_name": True}


class CreatePaymentMethodsParams(BaseModel):
    name: dict[str, str] = Field(description="Localized name of the payment method")
    key: str | None = Field(None, description="User-defined unique identifier")
    description: dict[str, str] | None = Field(None, description="Localized description")
    payment_interface: str | None = Field(None, alias="paymentInterface", description="Payment interface identifier (e.g. Adyen, Stripe)")
    method: str | None = Field(None, description="Payment method type (e.g. Card, PayPal)")
    interface_account: str | None = Field(None, alias="interfaceAccount", description="Interface account identifier")
    default: bool | None = Field(None, description="Whether this is the default payment method")
    payment_method_status: Literal["Active", "Inactive"] | None = Field(None, alias="paymentMethodStatus", description="Status of the payment method")
    customer: CustomerRef | None = Field(None, description="Customer who owns this payment method")
    business_unit: BusinessUnitRef | None = Field(None, alias="businessUnit", description="Business unit that owns this payment method")
    custom: dict[str, Any] | None = Field(None, description="Custom fields")
    model_config = {"populate_by_name": True}


class PaymentMethodUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdatePaymentMethodsParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[PaymentMethodUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the payment method to update")
    key: str | None = Field(None, description="The key of the payment method to update")
