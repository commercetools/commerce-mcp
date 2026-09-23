from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class CustomerAddressDraft(BaseModel):
    street_name: str = Field(alias="streetName", description="Street name")
    street_number: str | None = Field(None, alias="streetNumber", description="Street number")
    additional_street_info: str | None = Field(None, alias="additionalStreetInfo", description="Additional street information")
    postal_code: str = Field(alias="postalCode", description="Postal code")
    city: str = Field(description="City")
    region: str | None = Field(None, description="Region")
    state: str | None = Field(None, description="State")
    country: str = Field(description="Country code (ISO 3166-1 alpha-2)")
    company: str | None = Field(None, description="Company name")
    department: str | None = Field(None, description="Department")
    building: str | None = Field(None, description="Building")
    apartment: str | None = Field(None, description="Apartment")
    p_o_box: str | None = Field(None, alias="pOBox", description="P.O. Box")
    phone: str | None = Field(None, description="Phone")
    mobile: str | None = Field(None, description="Mobile phone")
    email: str | None = Field(None, description="Email")
    fax: str | None = Field(None, description="Fax")
    additional_address_info: str | None = Field(None, alias="additionalAddressInfo", description="Additional address information")
    model_config = {"populate_by_name": True}


class CustomerGroupReference(BaseModel):
    id: str = Field(description="ID of the customer group")
    type_id: str = Field("customer-group", alias="typeId", description="Resource type identifier")
    model_config = {"populate_by_name": True}


class TypeReference(BaseModel):
    id: str = Field(description="ID of the type")
    type_id: str = Field("type", alias="typeId", description="Resource type identifier")
    model_config = {"populate_by_name": True}


class CustomFields(BaseModel):
    type: TypeReference = Field(description="Reference to the custom type")
    fields: dict[str, Any] = Field(description="Custom field values")
    model_config = {"populate_by_name": True}


class ReadCustomerParams(BaseModel):
    id: str | None = Field(None, description="Customer ID")
    store_key: str | None = Field(None, alias="storeKey", description="Store key")
    where: list[str] | None = Field(
        None,
        description='Query predicates specified as strings. Example: ["email = \\"customer@example.com\\""]',
    )
    sort: list[str] | None = Field(
        None,
        description='Sort criteria for the results. Example: ["firstName asc", "createdAt desc"]',
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
    expand: list[str] | None = Field(
        None,
        description='Fields to expand. Example: ["customerGroup"]',
    )
    model_config = {"populate_by_name": True}


class CreateCustomerParams(BaseModel):
    email: str = Field(description="Customer email address")
    password: str = Field(description="Customer password")
    store_key: str | None = Field(None, alias="storeKey", description="Store key")
    first_name: str | None = Field(None, alias="firstName", description="Customer first name")
    last_name: str | None = Field(None, alias="lastName", description="Customer last name")
    middle_name: str | None = Field(None, alias="middleName", description="Customer middle name")
    title: str | None = Field(None, description="Customer title (e.g., Mr., Mrs., Dr.)")
    date_of_birth: str | None = Field(None, alias="dateOfBirth", description="Customer date of birth in ISO 8601 format (YYYY-MM-DD)")
    company_name: str | None = Field(None, alias="companyName", description="Customer company name")
    vat_id: str | None = Field(None, alias="vatId", description="Customer VAT identification number")
    addresses: list[CustomerAddressDraft] | None = Field(None, description="Customer addresses")
    default_shipping_address: int | None = Field(None, alias="defaultShippingAddress", description="Index of default shipping address in the addresses array")
    default_billing_address: int | None = Field(None, alias="defaultBillingAddress", description="Index of default billing address in the addresses array")
    shipping_addresses: list[int] | None = Field(None, alias="shippingAddresses", description="Indices of shipping addresses in the addresses array")
    billing_addresses: list[int] | None = Field(None, alias="billingAddresses", description="Indices of billing addresses in the addresses array")
    is_email_verified: bool | None = Field(None, alias="isEmailVerified", description="Whether the customer email is verified")
    external_id: str | None = Field(None, alias="externalId", description="Customer external ID")
    customer_group: CustomerGroupReference | None = Field(None, alias="customerGroup", description="Customer group reference")
    custom: CustomFields | None = Field(None, description="Custom fields")
    locale: str | None = Field(None, description="Customer locale")
    salutation: str | None = Field(None, description="Customer salutation")
    key: str | None = Field(None, description="Customer key")
    model_config = {"populate_by_name": True}


class CustomerUpdateAction(BaseModel):
    action: str = Field(description="The name of the update action to perform")
    model_config = {"extra": "allow"}


class UpdateCustomerParams(BaseModel):
    id: str = Field(description="The ID of the customer to update")
    version: int = Field(description="The current version of the customer")
    actions: list[CustomerUpdateAction] = Field(
        description='Array of update actions to perform on the customer. Each action should have an "action" field and other fields specific to that action type.',
    )
    model_config = {"populate_by_name": True}
