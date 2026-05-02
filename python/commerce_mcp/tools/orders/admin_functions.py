from __future__ import annotations

from typing import TYPE_CHECKING
from .schemas import ReadOrderParams, CreateOrderParams, UpdateOrderParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output
from .base_functions import (
    get_order_by_id,
    get_order_by_order_number,
    query_orders,
    serialize_actions,
)

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_order(
    params: ReadOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        store_key = params.store_key
        if params.id:
            result = await get_order_by_id(api, params.id, params.expand, store_key)
            return transform_tool_output(result)
        if params.order_number:
            result = await get_order_by_order_number(
                api, params.order_number, params.expand, store_key
            )
            return transform_tool_output(result)
        result = await query_orders(
            api,
            where=params.where,
            limit=params.limit,
            offset=params.offset,
            sort=params.sort,
            expand=params.expand,
            store_key=store_key,
        )
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read order", e)


async def create_order(
    params: CreateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        store_key = params.store_key or (params.store.key if params.store else None)
        prefix = f"/in-store/key={store_key}" if store_key else ""

        if params.quote_id:
            body: dict = {
                "quote": {"id": params.quote_id, "typeId": "quote"},
                "version": params.version,
            }
            if params.order_number:
                body["orderNumber"] = params.order_number
            result = await api.post(f"{prefix}/orders", body=body)
            return transform_tool_output(result)

        if params.total_price:
            import_body: dict = {
                "totalPrice": {
                    "type": "centPrecision",
                    "currencyCode": params.total_price.currency_code,
                    "centAmount": params.total_price.cent_amount,
                    "fractionDigits": 2,
                }
            }
            if params.order_number:
                import_body["orderNumber"] = params.order_number
            if params.customer_id:
                import_body["customerId"] = params.customer_id
            if params.customer_email:
                import_body["customerEmail"] = params.customer_email
            if params.store:
                import_body["store"] = params.store.model_dump(
                    by_alias=True, exclude_none=True
                )
            if params.line_items:
                import_body["lineItems"] = [
                    item.model_dump(by_alias=True, exclude_none=True)
                    for item in params.line_items
                ]
            result = await api.post("/orders/import", body=import_body)
            return transform_tool_output(result)

        body = {
            "cart": {"id": params.id or "", "typeId": "cart"},
            "version": params.version,
        }
        if params.order_number:
            body["orderNumber"] = params.order_number
        result = await api.post(f"{prefix}/orders", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create order", e)


async def update_order(
    params: UpdateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {
            "version": params.version,
            "actions": serialize_actions(params.actions),
        }
        store_key = params.store_key
        prefix = f"/in-store/key={store_key}" if store_key else ""
        if params.id:
            result = await api.post(f"{prefix}/orders/{params.id}", body=body)
        elif params.order_number:
            result = await api.post(
                f"{prefix}/orders/order-number={params.order_number}", body=body
            )
        else:
            raise Exception("Either id or orderNumber must be provided")
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update order", e)
