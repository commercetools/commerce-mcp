from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ReadPaymentsParams(BaseModel):
    id: str | None = Field(None, description="The ID of the payment to fetch")
    key: str | None = Field(None, description="The key of the payment to fetch")
    where: list[str] | None = Field(None, description="Query predicates for filtering payments")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 10)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(None, description="Sort criteria for the results")
    expand: list[str] | None = Field(None, description="Fields to expand in the response")


class MoneyValue(BaseModel):
    type: str = Field("centPrecision", description="Money type")
    currency_code: str = Field(alias="currencyCode", description="Currency code (e.g. EUR)")
    cent_amount: int = Field(alias="centAmount", description="Amount in cents")
    fraction_digits: int | None = Field(None, alias="fractionDigits")
    model_config = {"populate_by_name": True}


class PaymentMethodInfo(BaseModel):
    payment_interface: str | None = Field(None, alias="paymentInterface", description="Payment interface identifier")
    method: str | None = Field(None, description="Payment method type")
    name: dict[str, str] | None = Field(None, description="Localized name")
    model_config = {"populate_by_name": True}


class CreatePaymentsParams(BaseModel):
    amount_planned: MoneyValue = Field(alias="amountPlanned", description="Planned amount for the payment")
    key: str | None = Field(None, description="User-defined unique identifier")
    interface_id: str | None = Field(None, alias="interfaceId", description="Interface ID for the payment")
    payment_method_info: PaymentMethodInfo | None = Field(None, alias="paymentMethodInfo", description="Payment method information")
    custom: dict[str, Any] | None = Field(None, description="Custom fields")
    transaction: dict[str, Any] | None = Field(None, description="Transaction details")
    model_config = {"populate_by_name": True}


class PaymentUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdatePaymentsParams(BaseModel):
    version: int = Field(description="Current version for optimistic locking")
    actions: list[PaymentUpdateAction] = Field(description="Update actions to apply")
    id: str | None = Field(None, description="The ID of the payment to update")
    key: str | None = Field(None, description="The key of the payment to update")
