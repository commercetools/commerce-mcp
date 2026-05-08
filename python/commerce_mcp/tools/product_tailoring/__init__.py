from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .schemas import (
    ReadProductTailoringParams,
    CreateProductTailoringParams,
    UpdateProductTailoringParams,
)
from .functions import read_product_tailoring, create_product_tailoring, update_product_tailoring

_PRODUCT_TAILORING_TOOLS = [
    ToolDefinition(
        method="read_product_tailoring",
        name="Read product tailoring",
        description=(
            "Read product tailoring entries from the commercetools platform. "
            "Get a single entry by ID or key, get tailoring for a specific product in a store, "
            "or list multiple entries with optional filtering, sorting, and pagination. "
            "Admin and store contexts have full read access; customer context is read-only."
        ),
        parameters=ReadProductTailoringParams,
        handler=read_product_tailoring,
        actions={"product_tailoring": {"read": True}},
    ),
    ToolDefinition(
        method="create_product_tailoring",
        name="Create product tailoring",
        description=(
            "Create a new product tailoring entry in the commercetools platform. "
            "Allows customizing product information (name, description, slug, variants) "
            "for different stores or regions. Requires admin or store context."
        ),
        parameters=CreateProductTailoringParams,
        handler=create_product_tailoring,
        actions={"product_tailoring": {"create": True}},
    ),
    ToolDefinition(
        method="update_product_tailoring",
        name="Update product tailoring",
        description=(
            "Update or delete a product tailoring entry in the commercetools platform. "
            "Identify the entry by ID or key, then apply update actions such as setName, "
            "setDescription, setSlug, setVariants, publish, unpublish, or delete. "
            "Requires admin or store context."
        ),
        parameters=UpdateProductTailoringParams,
        handler=update_product_tailoring,
        actions={"product_tailoring": {"update": True}},
    ),
]

for _tool in _PRODUCT_TAILORING_TOOLS:
    register_tool(_tool)
