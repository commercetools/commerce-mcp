from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any

from .schemas import BulkCreateParams, BulkUpdateParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext

# Lazy import helpers to avoid circular imports at module load time

def _get_create_fn(entity_type: str):
    mapping: dict[str, Any] = {
        "product": ("commerce_mcp.tools.products.functions", "create_product"),
        "customer": ("commerce_mcp.tools.customer.functions", "create_customer"),
        "cart": ("commerce_mcp.tools.carts.functions", "create_cart"),
        "category": ("commerce_mcp.tools.category.functions", "create_category"),
        "channel": ("commerce_mcp.tools.channel.functions", "create_channel"),
        "discount-code": ("commerce_mcp.tools.discount_code.functions", "create_discount_code"),
        "cart-discount": ("commerce_mcp.tools.cart_discount.functions", "create_cart_discount"),
        "product-discount": ("commerce_mcp.tools.product_discount.functions", "create_product_discount"),
        "customer-group": ("commerce_mcp.tools.customer_group.functions", "create_customer_group"),
        "quote": ("commerce_mcp.tools.quote.functions", "create_quote"),
        "quote-request": ("commerce_mcp.tools.quote_request.functions", "create_quote_request"),
        "staged-quote": ("commerce_mcp.tools.staged_quote.functions", "create_staged_quote"),
        "standalone-price": ("commerce_mcp.tools.standalone_price.functions", "create_standalone_price"),
        "order": ("commerce_mcp.tools.orders.functions", "create_order"),
        "inventory": ("commerce_mcp.tools.inventory.functions", "create_inventory"),
        "store": ("commerce_mcp.tools.store.functions", "create_store"),
        "review": ("commerce_mcp.tools.reviews.functions", "create_review"),
        "recurring-orders": ("commerce_mcp.tools.recurring_orders.functions", "create_recurring_orders"),
        "shopping-lists": ("commerce_mcp.tools.shopping_lists.functions", "create_shopping_list"),
        "custom-objects": ("commerce_mcp.tools.custom_objects.functions", "create_custom_object"),
        "types": ("commerce_mcp.tools.types.functions", "create_type"),
        "transactions": ("commerce_mcp.tools.transactions.functions", "create_transaction"),
        "business-unit": ("commerce_mcp.tools.business_unit.functions", "create_business_unit"),
    }
    if entity_type not in mapping:
        raise SDKError("bulk create", Exception(f"Unknown entity type: {entity_type}"))
    module_path, fn_name = mapping[entity_type]
    import importlib
    mod = importlib.import_module(module_path)
    return getattr(mod, fn_name)


def _get_update_fn(entity_type: str):
    mapping: dict[str, Any] = {
        "product": ("commerce_mcp.tools.products.functions", "update_product"),
        "customer": ("commerce_mcp.tools.customer.functions", "update_customer"),
        "cart": ("commerce_mcp.tools.carts.functions", "update_cart"),
        "category": ("commerce_mcp.tools.category.functions", "update_category"),
        "channel": ("commerce_mcp.tools.channel.functions", "update_channel"),
        "discount-code": ("commerce_mcp.tools.discount_code.functions", "update_discount_code"),
        "cart-discount": ("commerce_mcp.tools.cart_discount.functions", "update_cart_discount"),
        "product-discount": ("commerce_mcp.tools.product_discount.functions", "update_product_discount"),
        "customer-group": ("commerce_mcp.tools.customer_group.functions", "update_customer_group"),
        "quote": ("commerce_mcp.tools.quote.functions", "update_quote"),
        "quote-request": ("commerce_mcp.tools.quote_request.functions", "update_quote_request"),
        "staged-quote": ("commerce_mcp.tools.staged_quote.functions", "update_staged_quote"),
        "standalone-price": ("commerce_mcp.tools.standalone_price.functions", "update_standalone_price"),
        "order": ("commerce_mcp.tools.orders.functions", "update_order"),
        "inventory": ("commerce_mcp.tools.inventory.functions", "update_inventory"),
        "store": ("commerce_mcp.tools.store.functions", "update_store"),
        "review": ("commerce_mcp.tools.reviews.functions", "update_review"),
        "recurring-orders": ("commerce_mcp.tools.recurring_orders.functions", "update_recurring_orders"),
        "shopping-lists": ("commerce_mcp.tools.shopping_lists.functions", "update_shopping_list"),
        "custom-objects": ("commerce_mcp.tools.custom_objects.functions", "update_custom_object"),
        "types": ("commerce_mcp.tools.types.functions", "update_type"),
        "business-unit": ("commerce_mcp.tools.business_unit.functions", "update_business_unit"),
        "product-selection": ("commerce_mcp.tools.product_selection.functions", "update_product_selection"),
        "product-type": ("commerce_mcp.tools.product_type.functions", "update_product_type"),
    }
    if entity_type not in mapping:
        raise SDKError("bulk update", Exception(f"Unknown entity type: {entity_type}"))
    module_path, fn_name = mapping[entity_type]
    import importlib
    mod = importlib.import_module(module_path)
    return getattr(mod, fn_name)


async def bulk_create(
    params: BulkCreateParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("bulk_create", "isAdmin")
    try:
        async def _create_one(item: Any) -> Any:
            fn = _get_create_fn(item.entity_type)
            schema_cls = fn.__annotations__.get("params") or fn.__annotations__.get("return")
            # Build params from data dict using the function's first parameter type
            import inspect
            sig = inspect.signature(fn)
            param_type = list(sig.parameters.values())[0].annotation
            if hasattr(param_type, "model_validate"):
                typed_params = param_type.model_validate(item.data)
            else:
                typed_params = item.data
            result_str = await fn(typed_params, api, ctx)
            return json.loads(result_str)

        results = await asyncio.gather(*[_create_one(item) for item in params.items], return_exceptions=True)
        output = {"success": True, "results": []}
        for r in results:
            if isinstance(r, Exception):
                output["results"].append({"error": str(r)})
            else:
                output["results"].append(r)
        return transform_tool_output(output)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("bulk create", e)


async def bulk_update(
    params: BulkUpdateParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("bulk_update", "isAdmin")
    try:
        async def _update_one(item: Any) -> Any:
            fn = _get_update_fn(item.entity_type)
            import inspect
            sig = inspect.signature(fn)
            param_type = list(sig.parameters.values())[0].annotation
            if hasattr(param_type, "model_validate"):
                typed_params = param_type.model_validate(item.data)
            else:
                typed_params = item.data
            result_str = await fn(typed_params, api, ctx)
            return json.loads(result_str)

        results = await asyncio.gather(*[_update_one(item) for item in params.items], return_exceptions=True)
        output = {"success": True, "results": []}
        for r in results:
            if isinstance(r, Exception):
                output["results"].append({"error": str(r)})
            else:
                output["results"].append(r)
        return transform_tool_output(output)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("bulk update", e)
