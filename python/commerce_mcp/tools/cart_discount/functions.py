from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import CreateCartDiscountParams, ReadCartDiscountParams, UpdateCartDiscountParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def _read_cart_discount_store(
    params: ReadCartDiscountParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = f"/in-store/key={ctx.store_key}/cart-discounts"
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{base}/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{base}/key={params.key}", params=query or None)
            return transform_tool_output(result)
        query = {}
        if params.where:
            query["where"] = params.where
        if params.limit is not None:
            query["limit"] = params.limit
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.expand:
            query["expand"] = params.expand
        result = await api.get(base, params=query or None)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read cart discount", e)


async def _read_cart_discount_admin(
    params: ReadCartDiscountParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/cart-discounts/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/cart-discounts/key={params.key}", params=query or None)
            return transform_tool_output(result)
        query = {}
        if params.where:
            query["where"] = params.where
        if params.limit is not None:
            query["limit"] = params.limit
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.expand:
            query["expand"] = params.expand
        result = await api.get("/cart-discounts", params=query or None)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read cart discount", e)


async def _create_cart_discount_store(
    params: CreateCartDiscountParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post(f"/in-store/key={ctx.store_key}/cart-discounts", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create cart discount", e)


async def _create_cart_discount_admin(
    params: CreateCartDiscountParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/cart-discounts", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create cart discount", e)


async def _update_cart_discount_store(
    params: UpdateCartDiscountParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = f"/in-store/key={ctx.store_key}/cart-discounts"
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"{base}/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"{base}/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update cart discount", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update cart discount", e)


async def _update_cart_discount_admin(
    params: UpdateCartDiscountParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/cart-discounts/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/cart-discounts/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update cart discount", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update cart discount", e)


async def read_cart_discount(
    params: ReadCartDiscountParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _read_cart_discount_store(params, api, ctx)
    if ctx.is_admin:
        return await _read_cart_discount_admin(params, api, ctx)
    raise ContextError("read_cart_discount", "isAdmin or storeKey")


async def create_cart_discount(
    params: CreateCartDiscountParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _create_cart_discount_store(params, api, ctx)
    if ctx.is_admin:
        return await _create_cart_discount_admin(params, api, ctx)
    raise ContextError("create_cart_discount", "isAdmin or storeKey")


async def update_cart_discount(
    params: UpdateCartDiscountParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _update_cart_discount_store(params, api, ctx)
    if ctx.is_admin:
        return await _update_cart_discount_admin(params, api, ctx)
    raise ContextError("update_cart_discount", "isAdmin or storeKey")
