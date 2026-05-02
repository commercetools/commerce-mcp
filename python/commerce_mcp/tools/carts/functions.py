from __future__ import annotations

from typing import TYPE_CHECKING
from .schemas import ReadCartParams, CreateCartParams, UpdateCartParams
from ...shared.errors import SDKError, ContextError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


# ── Private scope-specific implementations ────────────────────────────────────

async def _read_cart_as_associate(
    params: ReadCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        path = f"/as-associate/{ctx.customer_id}/in-business-unit/key={ctx.business_unit_key}/me/carts"
        query: dict = {"limit": params.limit}
        if params.id:
            query["where"] = f'id="{params.id}"'
        result = await api.get(path, params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read associate cart", e)


async def _read_cart_customer(
    params: ReadCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        query: dict = {"limit": params.limit}
        if params.id:
            query["where"] = f'id="{params.id}"'
        result = await api.get("/me/carts", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read customer cart", e)


async def _read_cart_store(
    params: ReadCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        query: dict = {"limit": params.limit}
        if params.id:
            query["where"] = f'id="{params.id}"'
        result = await api.get(f"/in-store/key={ctx.store_key}/carts", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read store cart", e)


async def _read_cart_admin(
    params: ReadCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        query: dict = {"limit": params.limit}
        if params.id:
            query["where"] = f'id="{params.id}"'
        result = await api.get("/carts", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read cart", e)


async def _create_cart_as_associate(
    params: CreateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body: dict = {"currency": params.currency}
        if params.line_items:
            body["lineItems"] = params.line_items
        path = f"/as-associate/{ctx.customer_id}/in-business-unit/key={ctx.business_unit_key}/me/carts"
        result = await api.post(path, body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create associate cart", e)


async def _create_cart_customer(
    params: CreateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body: dict = {"currency": params.currency}
        if params.line_items:
            body["lineItems"] = params.line_items
        result = await api.post("/me/carts", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create customer cart", e)


async def _create_cart_store(
    params: CreateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body: dict = {"currency": params.currency}
        if params.line_items:
            body["lineItems"] = params.line_items
        result = await api.post(f"/in-store/key={ctx.store_key}/carts", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create store cart", e)


async def _create_cart_admin(
    params: CreateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body: dict = {"currency": params.currency}
        if params.line_items:
            body["lineItems"] = params.line_items
        result = await api.post("/carts", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create cart", e)


async def _update_cart_as_associate(
    params: UpdateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        path = f"/as-associate/{ctx.customer_id}/in-business-unit/key={ctx.business_unit_key}/me/carts/{params.id}"
        body = {"version": params.version, "actions": params.actions}
        result = await api.post(path, body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update associate cart", e)


async def _update_cart_customer(
    params: UpdateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {"version": params.version, "actions": params.actions}
        result = await api.post(f"/me/carts/{params.id}", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update customer cart", e)


async def _update_cart_store(
    params: UpdateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {"version": params.version, "actions": params.actions}
        result = await api.post(f"/in-store/key={ctx.store_key}/carts/{params.id}", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update store cart", e)


async def _update_cart_admin(
    params: UpdateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {"version": params.version, "actions": params.actions}
        result = await api.post(f"/carts/{params.id}", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update cart", e)


# ── Public dispatch functions — mirrors contextToCartFunctionMapping ───────────

async def read_cart(
    params: ReadCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await _read_cart_as_associate(params, api, ctx)
    if ctx.customer_id:
        return await _read_cart_customer(params, api, ctx)
    if ctx.store_key:
        return await _read_cart_store(params, api, ctx)
    if ctx.is_admin:
        return await _read_cart_admin(params, api, ctx)
    raise ContextError("read_cart", "isAdmin, customerId, storeKey, or customerId+businessUnitKey")


async def create_cart(
    params: CreateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await _create_cart_as_associate(params, api, ctx)
    if ctx.customer_id:
        return await _create_cart_customer(params, api, ctx)
    if ctx.store_key:
        return await _create_cart_store(params, api, ctx)
    if ctx.is_admin:
        return await _create_cart_admin(params, api, ctx)
    raise ContextError("create_cart", "isAdmin, customerId, storeKey, or customerId+businessUnitKey")


async def update_cart(
    params: UpdateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await _update_cart_as_associate(params, api, ctx)
    if ctx.customer_id:
        return await _update_cart_customer(params, api, ctx)
    if ctx.store_key:
        return await _update_cart_store(params, api, ctx)
    if ctx.is_admin:
        return await _update_cart_admin(params, api, ctx)
    raise ContextError("update_cart", "isAdmin, customerId, storeKey, or customerId+businessUnitKey")
