from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import CreateDiscountCodeParams, ReadDiscountCodeParams, UpdateDiscountCodeParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_discount_code(
    params: ReadDiscountCodeParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("read_discount_code", "isAdmin")
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/discount-codes/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/discount-codes/key={params.key}", params=query or None)
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
        result = await api.get("/discount-codes", params=query or None)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("read discount code", e)


async def create_discount_code(
    params: CreateDiscountCodeParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_discount_code", "isAdmin")
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/discount-codes", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("create discount code", e)


async def update_discount_code(
    params: UpdateDiscountCodeParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_discount_code", "isAdmin")
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/discount-codes/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/discount-codes/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update discount code", Exception("Either id or key must be provided"))
    except ContextError:
        raise
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update discount code", e)
