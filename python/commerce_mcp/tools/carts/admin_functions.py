from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadCartParams, CreateCartParams, ReplicateCartParams, UpdateCartParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output
from .base_functions import get_cart_by_id, get_cart_by_key, query_carts, serialize_actions

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_cart(
    params: ReadCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        if params.id:
            result = await get_cart_by_id(api, params.id, params.expand)
            return transform_tool_output(result)

        if params.key:
            result = await get_cart_by_key(api, params.key, params.expand)
            return transform_tool_output(result)

        if params.customer_id:
            result = await query_carts(
                api,
                where=[f'customerId="{params.customer_id}"'],
                limit=params.limit,
                offset=params.offset,
                sort=params.sort,
                expand=params.expand,
                store_key=params.store_key,
            )
            return transform_tool_output(result)

        if params.where:
            result = await query_carts(
                api,
                where=params.where,
                limit=params.limit,
                offset=params.offset,
                sort=params.sort,
                expand=params.expand,
                store_key=params.store_key,
            )
            return transform_tool_output(result)

        raise Exception("At least one of id, key, customerId, or where must be provided")
    except Exception as e:
        raise SDKError("read cart", e)


async def create_cart(
    params: CreateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        store_key = params.store.key if params.store else None
        path = f"/in-store/key={store_key}/carts" if store_key else "/carts"
        result = await api.post(path, body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create cart", e)


async def replicate_cart(
    params: ReplicateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body: dict[str, Any] = {
            "reference": params.reference.model_dump(by_alias=True, exclude_none=True),
        }
        if params.key:
            body["key"] = params.key
        prefix = f"/in-store/key={params.store_key}" if params.store_key else ""
        result = await api.post(f"{prefix}/carts/replicate", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("replicate cart", e)


async def update_cart(
    params: UpdateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        actions = serialize_actions(params.actions)
        body = {"version": params.version, "actions": actions}
        prefix = f"/in-store/key={params.store_key}" if params.store_key else ""
        if params.id:
            result = await api.post(f"{prefix}/carts/{params.id}", body=body)
        elif params.key:
            result = await api.post(f"{prefix}/carts/key={params.key}", body=body)
        else:
            raise Exception("Either id or key must be provided")
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update cart", e)
