from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadOrderParams, CreateOrderParams, UpdateOrderParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output
from .base_functions import serialize_actions

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_order(
    params: ReadOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        prefix = (
            f"/as-associate/{ctx.customer_id}"
            f"/in-business-unit/key={ctx.business_unit_key}"
        )
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{prefix}/orders/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.order_number:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(
                f"{prefix}/orders/order-number={params.order_number}",
                params=query or None,
            )
            return transform_tool_output(result)
        query = {"limit": params.limit or 10}
        if params.where:
            query["where"] = params.where
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.expand:
            query["expand"] = params.expand
        result = await api.get(f"{prefix}/orders", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read associate order", e)


async def create_order(
    params: CreateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        prefix = (
            f"/as-associate/{ctx.customer_id}"
            f"/in-business-unit/key={ctx.business_unit_key}"
        )
        if params.quote_id:
            body: dict = {
                "quote": {"id": params.quote_id, "typeId": "quote"},
                "version": params.version,
            }
            if params.order_number:
                body["orderNumber"] = params.order_number
            result = await api.post(f"{prefix}/orders/order-quote", body=body)
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
        raise SDKError("create associate order", e)


async def update_order(
    params: UpdateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        prefix = (
            f"/as-associate/{ctx.customer_id}"
            f"/in-business-unit/key={ctx.business_unit_key}"
        )
        body = {
            "version": params.version,
            "actions": serialize_actions(params.actions),
        }
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
        raise SDKError("update associate order", e)
