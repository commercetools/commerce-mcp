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
        store_key = ctx.store_key
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
        raise SDKError("read store order", e)


async def create_order(
    params: CreateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        store_key = ctx.store_key
        prefix = f"/in-store/key={store_key}"

        if params.quote_id:
            body: dict = {
                "quote": {"id": params.quote_id, "typeId": "quote"},
                "version": params.version,
            }
            if params.order_number:
                body["orderNumber"] = params.order_number
            result = await api.post(f"{prefix}/orders", body=body)
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
        raise SDKError("create store order", e)


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
        store_key = ctx.store_key
        prefix = f"/in-store/key={store_key}"
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
        raise SDKError("update store order", e)
