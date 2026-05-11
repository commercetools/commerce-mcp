from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadCartParams, CreateCartParams, ReplicateCartParams, UpdateCartParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output
from .base_functions import query_carts, serialize_actions, verify_cart_belongs_to_customer

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
            if cart.get("customerId") != ctx.customer_id:
                raise Exception("Cart not found")
            return transform_tool_output(cart)

        where = list(params.where) if params.where else []
        where.append(f'customerId="{ctx.customer_id}"')
        result = await query_carts(
            api,
            where=where,
            limit=params.limit,
            offset=params.offset,
            sort=params.sort,
            expand=params.expand,
            store_key=params.store_key,
        )
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read customer cart", e)


async def create_cart(
    params: CreateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        body["customerId"] = ctx.customer_id
        store_key = params.store.key if params.store else None
        path = f"/in-store/key={store_key}/carts" if store_key else "/carts"
        result = await api.post(path, body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create customer cart", e)


async def replicate_cart(
    params: ReplicateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        is_customer_cart = await verify_cart_belongs_to_customer(
            api, ctx.customer_id, cart_id=params.reference.id  # type: ignore[arg-type]
        )
        if not is_customer_cart:
            raise Exception("Cannot replicate cart: not owned by customer")
        body: dict[str, Any] = {
            "reference": params.reference.model_dump(by_alias=True, exclude_none=True),
        }
        if params.key:
            body["key"] = params.key
        prefix = f"/in-store/key={params.store_key}" if params.store_key else ""
        result = await api.post(f"{prefix}/carts/replicate", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("replicate customer cart", e)


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
        is_customer_cart = await verify_cart_belongs_to_customer(
            api, ctx.customer_id, cart_id=cart_id, cart_key=cart_key  # type: ignore[arg-type]
        )
        if not is_customer_cart:
            raise Exception("Cannot update cart: not owned by customer")
        actions = serialize_actions(params.actions)
        body = {"version": params.version, "actions": actions}
        prefix = f"/in-store/key={params.store_key}" if params.store_key else ""
        if cart_id:
            result = await api.post(f"{prefix}/carts/{cart_id}", body=body)
        else:
            result = await api.post(f"{prefix}/carts/key={cart_key}", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update customer cart", e)
