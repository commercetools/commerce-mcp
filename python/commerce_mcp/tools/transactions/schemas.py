from __future__ import annotations

from pydantic import BaseModel, Field


class ReadTransactionParams(BaseModel):
    id: str | None = Field(None, description="The ID of the transaction to retrieve")
    key: str | None = Field(None, description="The key of the transaction to retrieve")
    limit: int | None = Field(None, ge=1, le=500, description="Number of results (1–500, default 20)")
    offset: int | None = Field(None, ge=0, le=10000, description="Number of items to skip (0–10000)")
    sort: list[str] | None = Field(None, description='Sort criteria. Example: ["createdAt desc"]')
    where: list[str] | None = Field(None, description='Query predicates. Example: ["key=\\"tx-key\\""]')
    expand: list[str] | None = Field(None, description='Reference paths to expand. Example: ["cart", "order"]')


class ApplicationReference(BaseModel):
    type_id: str = Field("application", alias="typeId", description="Resource type identifier")
    id: str | None = Field(None, description="ID of the application")
    key: str | None = Field(None, description="Key of the application")
    model_config = {"populate_by_name": True}


class CartReference(BaseModel):
    type_id: str = Field("cart", alias="typeId", description="Resource type identifier")
    id: str | None = Field(None, description="ID of the cart")
    key: str | None = Field(None, description="Key of the cart")
    model_config = {"populate_by_name": True}


class PaymentIntegrationReference(BaseModel):
    type_id: str = Field("payment-integration", alias="typeId", description="Resource type identifier")
    id: str | None = Field(None, description="ID of the payment integration")
    key: str | None = Field(None, description="Key of the payment integration")
    model_config = {"populate_by_name": True}


class TransactionAmount(BaseModel):
    cent_amount: int = Field(alias="centAmount", description="Amount in cents")
    currency_code: str = Field(alias="currencyCode", description="Currency code (e.g. EUR, USD)")
    model_config = {"populate_by_name": True}


class TransactionItem(BaseModel):
    payment_integration: PaymentIntegrationReference = Field(alias="paymentIntegration", description="Payment integration to use")
    amount: TransactionAmount = Field(description="Money value of the transaction item")
    model_config = {"populate_by_name": True}


class CreateTransactionParams(BaseModel):
    application: ApplicationReference = Field(description="Application for which the payment is executed")
    cart: CartReference = Field(description="Cart for which the payment must be executed")
    transaction_items: list[TransactionItem] = Field(alias="transactionItems", description="Transaction items (exactly one required)")
    key: str | None = Field(None, description="User-defined unique identifier (2–256 chars)")
    model_config = {"populate_by_name": True}
