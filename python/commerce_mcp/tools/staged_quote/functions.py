from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import CreateStagedQuoteParams, ReadStagedQuoteParams, UpdateStagedQuoteParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def _read_staged_quote_store(
    params: ReadStagedQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = f"/in-store/key={ctx.store_key}/staged-quotes"
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
        raise SDKError("read staged quote", e)


async def _read_staged_quote_admin(
    params: ReadStagedQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/staged-quotes/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/staged-quotes/key={params.key}", params=query or None)
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
        result = await api.get("/staged-quotes", params=query or None)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read staged quote", e)


async def _create_staged_quote_store(
    params: CreateStagedQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post(f"/in-store/key={ctx.store_key}/staged-quotes", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create staged quote", e)


async def _create_staged_quote_admin(
    params: CreateStagedQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/staged-quotes", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create staged quote", e)


async def _update_staged_quote_store(
    params: UpdateStagedQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = f"/in-store/key={ctx.store_key}/staged-quotes"
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
        raise SDKError("update staged quote", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update staged quote", e)


async def _update_staged_quote_admin(
    params: UpdateStagedQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/staged-quotes/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/staged-quotes/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update staged quote", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update staged quote", e)


async def read_staged_quote(
    params: ReadStagedQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _read_staged_quote_store(params, api, ctx)
    if ctx.is_admin:
        return await _read_staged_quote_admin(params, api, ctx)
    raise ContextError("read_staged_quote", "isAdmin or storeKey")


async def create_staged_quote(
    params: CreateStagedQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _create_staged_quote_store(params, api, ctx)
    if ctx.is_admin:
        return await _create_staged_quote_admin(params, api, ctx)
    raise ContextError("create_staged_quote", "isAdmin or storeKey")


async def update_staged_quote(
    params: UpdateStagedQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _update_staged_quote_store(params, api, ctx)
    if ctx.is_admin:
        return await _update_staged_quote_admin(params, api, ctx)
    raise ContextError("update_staged_quote", "isAdmin or storeKey")
