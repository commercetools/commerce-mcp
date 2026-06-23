from __future__ import annotations

from pydantic import BaseModel, Field


class PaymentIntentAmount(BaseModel):
    cent_amount: int = Field(alias="centAmount", description="Amount in cents")
    currency_code: str = Field(alias="currencyCode", description="Currency code (e.g. EUR)")
    model_config = {"populate_by_name": True}


class PaymentIntentAction(BaseModel):
    action: str = Field(description="Action type: capturePayment, refundPayment, cancelPayment, or reversePayment")
    model_config = {"extra": "allow"}


class UpdatePaymentIntentsParams(BaseModel):
    payment_id: str = Field(alias="paymentId", description="The ID of the payment to manage")
    actions: list[PaymentIntentAction] = Field(description="Action to execute (exactly one: capturePayment, refundPayment, cancelPayment, reversePayment)")
    model_config = {"populate_by_name": True}
