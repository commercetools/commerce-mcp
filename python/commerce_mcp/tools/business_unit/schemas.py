from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ReadBusinessUnitParams(BaseModel):
    id: str | None = Field(None, description="The ID of the business unit to fetch")
    key: str | None = Field(None, description="The key of the business unit to fetch")
    where: list[str] | None = Field(
        None,
        description='Query predicates for filtering business units. Example: ["status=\\"Active\\""]',
    )
    limit: int | None = Field(None, ge=1, le=500, description="Number of results to return (1-500, default 10)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    sort: list[str] | None = Field(
        None,
        description='Sort criteria. Example: ["createdAt desc"]',
    )
    expand: list[str] | None = Field(
        None,
        description='Fields to expand. Example: ["associates[*].customer"]',
    )


class StoreKeyReference(BaseModel):
    key: str = Field(description="Store key")
    type_id: str = Field("store", alias="typeId", description="Resource type identifier")
    model_config = {"populate_by_name": True}


class BusinessUnitReference(BaseModel):
    id: str | None = Field(None, description="ID of the business unit")
    key: str | None = Field(None, description="Key of the business unit")
    type_id: str = Field("business-unit", alias="typeId", description="Resource type identifier")
    model_config = {"populate_by_name": True}


class AssociateRoleAssignmentDraft(BaseModel):
    associate_role: dict[str, Any] = Field(
        alias="associateRole",
        description="Reference to the associate role (key and typeId='associate-role')",
    )
    inheritance: str | None = Field(None, description="Enabled or Disabled")
    model_config = {"populate_by_name": True}


class AssociateDraft(BaseModel):
    customer: dict[str, Any] = Field(description="Customer reference (id and typeId='customer')")
    associate_role_assignments: list[AssociateRoleAssignmentDraft] = Field(
        alias="associateRoleAssignments",
        description="Role assignments for this associate",
    )
    model_config = {"populate_by_name": True}


class Address(BaseModel):
    country: str = Field(description="Country code in ISO 3166-1 alpha-2 format")
    id: str | None = Field(None, description="Address ID")
    key: str | None = Field(None, description="Address key")
    title: str | None = Field(None, description="Title")
    salutation: str | None = Field(None, description="Salutation")
    first_name: str | None = Field(None, alias="firstName", description="First name")
    last_name: str | None = Field(None, alias="lastName", description="Last name")
    street_name: str | None = Field(None, alias="streetName", description="Street name")
    street_number: str | None = Field(None, alias="streetNumber", description="Street number")
    additional_street_info: str | None = Field(None, alias="additionalStreetInfo", description="Additional street info")
    postal_code: str | None = Field(None, alias="postalCode", description="Postal code")
    city: str | None = Field(None, description="City")
    region: str | None = Field(None, description="Region")
    state: str | None = Field(None, description="State")
    company: str | None = Field(None, description="Company name")
    department: str | None = Field(None, description="Department")
    building: str | None = Field(None, description="Building")
    apartment: str | None = Field(None, description="Apartment")
    po_box: str | None = Field(None, alias="pOBox", description="PO Box")
    phone: str | None = Field(None, description="Phone number")
    mobile: str | None = Field(None, description="Mobile number")
    email: str | None = Field(None, description="Email address")
    fax: str | None = Field(None, description="Fax number")
    additional_address_info: str | None = Field(None, alias="additionalAddressInfo", description="Additional address info")
    external_id: str | None = Field(None, alias="externalId", description="External ID")
    custom: dict[str, Any] | None = Field(None, description="Custom fields")
    model_config = {"populate_by_name": True}


class CreateBusinessUnitParams(BaseModel):
    key: str = Field(
        description="User-defined unique and immutable identifier (2-256 chars, alphanumeric with _ and -)",
    )
    name: str = Field(description="Name of the Business Unit")
    unit_type: str = Field(alias="unitType", description="Type of the Business Unit: Company or Division")
    contact_email: str | None = Field(None, alias="contactEmail", description="Email address of the Business Unit")
    status: str | None = Field(None, description="Status of the Business Unit: Active or Inactive (default Active)")
    stores: list[StoreKeyReference] | None = Field(
        None,
        description="References to Stores the Business Unit is associated with",
    )
    store_mode: str | None = Field(None, alias="storeMode", description="Mode for Store inheritance: Explicit or FromParent")
    parent_unit: BusinessUnitReference | None = Field(
        None,
        alias="parentUnit",
        description="Parent Business Unit reference",
    )
    addresses: list[Address] | None = Field(None, description="Addresses of the Business Unit")
    shipping_address_ids: list[str] | None = Field(
        None, alias="shippingAddressIds", description="IDs of addresses suitable for shipping"
    )
    default_shipping_address_id: str | None = Field(
        None, alias="defaultShippingAddressId", description="ID of the default shipping address"
    )
    billing_address_ids: list[str] | None = Field(
        None, alias="billingAddressIds", description="IDs of addresses suitable for billing"
    )
    default_billing_address_id: str | None = Field(
        None, alias="defaultBillingAddressId", description="ID of the default billing address"
    )
    associates: list[AssociateDraft] | None = Field(None, description="Associates of the Business Unit")
    associate_mode: str | None = Field(
        None,
        alias="associateMode",
        description="Mode for Associate inheritance: Explicit or ExplicitAndFromParent",
    )
    approval_rule_mode: str | None = Field(
        None,
        alias="approvalRuleMode",
        description="Mode for Approval Rule inheritance: Explicit or ExplicitAndFromParent",
    )
    custom: dict[str, Any] | None = Field(None, description="Custom fields for the Business Unit")
    model_config = {"populate_by_name": True}


class BusinessUnitUpdateAction(BaseModel):
    action: str = Field(description="The update action type")
    model_config = {"extra": "allow"}


class UpdateBusinessUnitParams(BaseModel):
    id: str | None = Field(None, description="The ID of the business unit to update")
    key: str | None = Field(None, description="The key of the business unit to update")
    version: int | None = Field(
        None,
        ge=0,
        description="The current version of the business unit (fetched automatically if not provided)",
    )
    actions: list[BusinessUnitUpdateAction] = Field(description="Update actions to apply")
