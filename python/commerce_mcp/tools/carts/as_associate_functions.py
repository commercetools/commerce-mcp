from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadCartParams, CreateCartParams, ReplicateCartParams, UpdateCartParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output
from .base_functions import serialize_actions

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_cart(
    params: ReadCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = f"/as-associate/{ctx.customer_id}/in-business-unit/key={ctx.business_unit_key}"

        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{base}/carts/{params.id}", params=query or None)
            return transform_tool_output(result)

        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{base}/carts/key={params.key}", params=query or None)
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
        result = await api.get(f"{base}/carts", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read associate cart", e)


async def create_cart(
    params: CreateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        body["customerId"] = ctx.customer_id
        body["businessUnit"] = {"typeId": "business-unit", "key": ctx.business_unit_key}
        path = f"/as-associate/{ctx.customer_id}/in-business-unit/key={ctx.business_unit_key}/carts"
        result = await api.post(path, body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create associate cart", e)


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
        path = (
            f"/as-associate/{ctx.customer_id}"
            f"/in-business-unit/key={ctx.business_unit_key}/carts/replicate"
        )
        result = await api.post(path, body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("replicate associate cart", e)


async def update_cart(
    params: UpdateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        if not params.actions:
            raise Exception("At least one action is required to update a cart")
        base = f"/as-associate/{ctx.customer_id}/in-business-unit/key={ctx.business_unit_key}"
        actions = serialize_actions(params.actions)
        body = {"version": params.version, "actions": actions}
        if params.id:
            result = await api.post(f"{base}/carts/{params.id}", body=body)
        elif params.key:
            result = await api.post(f"{base}/carts/key={params.key}", body=body)
        else:
            raise Exception("Either cart ID or key must be provided")
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update associate cart", e)
