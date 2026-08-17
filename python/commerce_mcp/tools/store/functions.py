from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import CreateStoreParams, ReadStoreParams, UpdateStoreParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


# ── Store-context helpers ─────────────────────────────────────────────────────

async def _read_store_store(
    params: ReadStoreParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Store context: read only the store's own record."""
    try:
        query: dict[str, Any] = {}
        if params.expand:
            query["expand"] = params.expand
        result = await api.get(
            f"/stores/key={ctx.store_key}",
            params=query or None,
        )
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read store", e)


async def _update_store_store(
    params: UpdateStoreParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Store context: update only the store's own record."""
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        result = await api.post(f"/stores/key={ctx.store_key}", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update store", e)


# ── Admin helpers ─────────────────────────────────────────────────────────────

async def _read_store_admin(
    params: ReadStoreParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/stores/{params.id}", params=query or None)
            return transform_tool_output(result)

        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/stores/key={params.key}", params=query or None)
            return transform_tool_output(result)

        query = {"limit": params.limit if params.limit is not None else 10}
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.where:
            query["where"] = params.where
        if params.expand:
            query["expand"] = params.expand
        result = await api.get("/stores", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read store", e)


async def _create_store_admin(
    params: CreateStoreParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/stores", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create store", e)


async def _update_store_admin(
    params: UpdateStoreParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/stores/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/stores/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError(
            "update store",
            Exception("Either id or key must be provided"),
        )
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update store", e)


# ── Public dispatch functions ─────────────────────────────────────────────────

async def read_store(
    params: ReadStoreParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _read_store_store(params, api, ctx)
    if ctx.is_admin:
        return await _read_store_admin(params, api, ctx)
    raise ContextError("read_store", "isAdmin or storeKey")


async def create_store(
    params: CreateStoreParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_store", "isAdmin")
    try:
        return await _create_store_admin(params, api, ctx)
    except ContextError:
        raise
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("create store", e)


async def update_store(
    params: UpdateStoreParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _update_store_store(params, api, ctx)
    if ctx.is_admin:
        return await _update_store_admin(params, api, ctx)
    raise ContextError("update_store", "isAdmin or storeKey")
