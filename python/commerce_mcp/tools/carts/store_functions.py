from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadCartParams, CreateCartParams, ReplicateCartParams, UpdateCartParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output
from .base_functions import get_cart_by_id, get_cart_by_key, query_carts, serialize_actions, verify_cart_belongs_to_store

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_cart(
    params: ReadCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        if ctx.cart_id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            cart = await api.get(f"/carts/{ctx.cart_id}", params=query or None)
            if (cart.get("store") or {}).get("key") != ctx.store_key:
                raise Exception("Cart not found")
            return transform_tool_output(cart)

        if params.id:
            cart = await get_cart_by_id(api, params.id, params.expand)
            if (cart.get("store") or {}).get("key") != ctx.store_key:
                raise Exception("Cart not found")
            return transform_tool_output(cart)

        if params.key:
            cart = await get_cart_by_key(api, params.key, params.expand)
            if (cart.get("store") or {}).get("key") != ctx.store_key:
                raise Exception("Cart not found")
            return transform_tool_output(cart)

        if params.customer_id:
            result = await query_carts(
                api,
                where=[f'customerId="{params.customer_id}"'],
                limit=params.limit,
                offset=params.offset,
                sort=params.sort,
                expand=params.expand,
                store_key=ctx.store_key,
            )
            return transform_tool_output(result)

        result = await query_carts(
            api,
            where=params.where,
            limit=params.limit,
            offset=params.offset,
            sort=params.sort,
            expand=params.expand,
            store_key=ctx.store_key,
        )
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read store cart", e)


async def create_cart(
    params: CreateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        body["store"] = {"key": ctx.store_key, "typeId": "store"}
        result = await api.post(f"/in-store/key={ctx.store_key}/carts", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create store cart", e)


async def replicate_cart(
    params: ReplicateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        is_store_cart = await verify_cart_belongs_to_store(
            api, ctx.store_key, cart_id=params.reference.id  # type: ignore[arg-type]
        )
        if not is_store_cart:
            raise Exception("Cannot replicate cart: not from this store")
        body: dict[str, Any] = {
            "reference": params.reference.model_dump(by_alias=True, exclude_none=True),
        }
        if params.key:
            body["key"] = params.key
        result = await api.post(f"/in-store/key={ctx.store_key}/carts/replicate", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("replicate store cart", e)


async def update_cart(
    params: UpdateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        cart_id = ctx.cart_id or params.id
        cart_key = params.key
        if not cart_id and not cart_key:
            raise Exception("Either cart ID or key must be provided")
        is_store_cart = await verify_cart_belongs_to_store(
            api, ctx.store_key, cart_id=cart_id, cart_key=cart_key  # type: ignore[arg-type]
        )
        if not is_store_cart:
            raise Exception("Cannot update cart: not from this store")
        actions = serialize_actions(params.actions)
        body = {"version": params.version, "actions": actions}
        if cart_id:
            result = await api.post(f"/in-store/key={ctx.store_key}/carts/{cart_id}", body=body)
        else:
            result = await api.post(f"/in-store/key={ctx.store_key}/carts/key={cart_key}", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update store cart", e)
