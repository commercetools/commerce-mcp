from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import (
    ReadShippingMethodsParams,
    CreateShippingMethodsParams,
    UpdateShippingMethodsParams,
)
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_shipping_methods(
    params: ReadShippingMethodsParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("read_shipping_methods", "isAdmin")
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/shipping-methods/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/shipping-methods/key={params.key}", params=query or None)
            return transform_tool_output(result)
        query = {}
        if params.limit is not None:
            query["limit"] = params.limit
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.where:
            query["where"] = params.where
        if params.expand:
            query["expand"] = params.expand
        result = await api.get("/shipping-methods", params=query or None)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("read shipping methods", e)


async def create_shipping_methods(
    params: CreateShippingMethodsParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_shipping_methods", "isAdmin")
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/shipping-methods", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("create shipping methods", e)


async def update_shipping_methods(
    params: UpdateShippingMethodsParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_shipping_methods", "isAdmin")
    try:
        body: dict[str, Any] = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/shipping-methods/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/shipping-methods/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError(
            "update shipping methods", Exception("Either id or key must be provided")
        )
    except ContextError:
        raise
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update shipping methods", e)
