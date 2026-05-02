from __future__ import annotations

from typing import TYPE_CHECKING
from .schemas import ReadOrderParams, CreateOrderParams, UpdateOrderParams
from ...shared.errors import SDKError, ContextError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


# ── Private scope-specific implementations ────────────────────────────────────

async def _read_order_admin(
    params: ReadOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        query: dict = {"limit": params.limit}
        if params.id:
            query["where"] = f'id="{params.id}"'
        if params.order_number:
            query.setdefault("where", f'orderNumber="{params.order_number}"')
        result = await api.get("/orders", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read order", e)


async def _read_order_customer(
    params: ReadOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        where = [f'customerId="{ctx.customer_id}"']
        if params.id:
            where.append(f'id="{params.id}"')
        result = await api.get("/orders", params={"limit": params.limit, "where": " and ".join(where)})
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read customer order", e)


async def _read_order_store(
    params: ReadOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        query: dict = {"limit": params.limit}
        if params.id:
            query["where"] = f'id="{params.id}"'
        result = await api.get(f"/in-store/key={ctx.store_key}/orders", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read store order", e)


async def _read_order_as_associate(
    params: ReadOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        path = (
            f"/as-associate/{ctx.customer_id}"
            f"/in-business-unit/key={ctx.business_unit_key}/orders"
        )
        result = await api.get(path, params={"limit": params.limit})
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read associate order", e)


async def _create_order_as_associate(
    params: CreateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        path = f"/as-associate/{ctx.customer_id}/in-business-unit/key={ctx.business_unit_key}/orders"
        body = {"cart": {"typeId": "cart", "id": params.cart_id}, "version": params.version}
        result = await api.post(path, body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create associate order", e)


async def _create_order_store(
    params: CreateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {"cart": {"typeId": "cart", "id": params.cart_id}, "version": params.version}
        result = await api.post(f"/in-store/key={ctx.store_key}/orders", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create store order", e)


async def _create_order_admin(
    params: CreateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {"cart": {"typeId": "cart", "id": params.cart_id}, "version": params.version}
        result = await api.post("/orders", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create order", e)


async def _update_order_as_associate(
    params: UpdateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        path = f"/as-associate/{ctx.customer_id}/in-business-unit/key={ctx.business_unit_key}/orders/{params.id}"
        body = {"version": params.version, "actions": params.actions}
        result = await api.post(path, body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update associate order", e)


async def _update_order_store(
    params: UpdateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {"version": params.version, "actions": params.actions}
        result = await api.post(f"/in-store/key={ctx.store_key}/orders/{params.id}", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update store order", e)


async def _update_order_admin(
    params: UpdateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {"version": params.version, "actions": params.actions}
        result = await api.post(f"/orders/{params.id}", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update order", e)


# ── Public dispatch functions — mirrors contextToOrderFunctionMapping ──────────

async def read_order(
    params: ReadOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Mirrors contextToOrderFunctionMapping: explicit context required, no fallthrough.
    if ctx.customer_id and ctx.business_unit_key:
        return await _read_order_as_associate(params, api, ctx)
    if ctx.customer_id:
        return await _read_order_customer(params, api, ctx)
    if ctx.store_key:
        return await _read_order_store(params, api, ctx)
    if ctx.is_admin:
        return await _read_order_admin(params, api, ctx)
    raise ContextError("read_order", "isAdmin, customerId, storeKey, or customerId+businessUnitKey")


async def create_order(
    params: CreateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Customer-only context cannot create orders (no businessUnitKey) — matches TypeScript mapping.
    if ctx.customer_id and ctx.business_unit_key:
        return await _create_order_as_associate(params, api, ctx)
    if ctx.store_key:
        return await _create_order_store(params, api, ctx)
    if ctx.is_admin:
        return await _create_order_admin(params, api, ctx)
    raise ContextError("create_order", "isAdmin, storeKey, or customerId+businessUnitKey")


async def update_order(
    params: UpdateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Customer-only context cannot update orders — matches TypeScript mapping.
    if ctx.customer_id and ctx.business_unit_key:
        return await _update_order_as_associate(params, api, ctx)
    if ctx.store_key:
        return await _update_order_store(params, api, ctx)
    if ctx.is_admin:
        return await _update_order_admin(params, api, ctx)
    raise ContextError("update_order", "isAdmin, storeKey, or customerId+businessUnitKey")
