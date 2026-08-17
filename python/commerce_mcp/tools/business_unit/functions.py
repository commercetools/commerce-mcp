from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import CreateBusinessUnitParams, ReadBusinessUnitParams, UpdateBusinessUnitParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def _fetch_business_unit_version(
    id: str | None,
    key: str | None,
    api: "CommercetoolsAPI",
    store_key: str | None,
) -> int:
    """Fetch the current version of a business unit by ID or key."""
    if id:
        base = f"/in-store/key={store_key}/business-units/{id}" if store_key else f"/business-units/{id}"
        data = await api.get(base, params=None)
        return data["version"]
    if key:
        base = f"/in-store/key={store_key}/business-units/key={key}" if store_key else f"/business-units/key={key}"
        data = await api.get(base, params=None)
        return data["version"]
    raise SDKError("fetch business unit version", Exception("Either id or key must be provided"))


async def _read_business_unit_store(
    params: ReadBusinessUnitParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = f"/in-store/key={ctx.store_key}/business-units"
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
        raise SDKError("read business unit", e)


async def _read_business_unit_admin(
    params: ReadBusinessUnitParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/business-units/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/business-units/key={params.key}", params=query or None)
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
        result = await api.get("/business-units", params=query or None)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read business unit", e)


async def _create_business_unit_store(
    params: CreateBusinessUnitParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        # Ensure the business unit is associated with the store (mirrors store.functions.ts)
        if "stores" not in body:
            body["stores"] = [{"key": ctx.store_key, "typeId": "store"}]
        if "storeMode" not in body:
            body["storeMode"] = "Explicit"
        result = await api.post(f"/in-store/key={ctx.store_key}/business-units", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create business unit", e)


async def _create_business_unit_admin(
    params: CreateBusinessUnitParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/business-units", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create business unit", e)


async def _update_business_unit_store(
    params: UpdateBusinessUnitParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        # Auto-fetch version if not provided (mirrors TypeScript base.functions.ts behavior)
        version = params.version
        if version is None:
            version = await _fetch_business_unit_version(params.id, params.key, api, ctx.store_key)

        base = f"/in-store/key={ctx.store_key}/business-units"
        body = {
            "version": version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"{base}/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"{base}/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update business unit", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update business unit", e)


async def _update_business_unit_admin(
    params: UpdateBusinessUnitParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        # Auto-fetch version if not provided (mirrors TypeScript base.functions.ts behavior)
        version = params.version
        if version is None:
            version = await _fetch_business_unit_version(params.id, params.key, api, None)

        body = {
            "version": version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/business-units/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/business-units/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update business unit", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update business unit", e)


async def read_business_unit(
    params: ReadBusinessUnitParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _read_business_unit_store(params, api, ctx)
    if ctx.is_admin:
        return await _read_business_unit_admin(params, api, ctx)
    raise ContextError("read_business_unit", "isAdmin or storeKey")


async def create_business_unit(
    params: CreateBusinessUnitParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _create_business_unit_store(params, api, ctx)
    if ctx.is_admin:
        return await _create_business_unit_admin(params, api, ctx)
    raise ContextError("create_business_unit", "isAdmin or storeKey")


async def update_business_unit(
    params: UpdateBusinessUnitParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _update_business_unit_store(params, api, ctx)
    if ctx.is_admin:
        return await _update_business_unit_admin(params, api, ctx)
    raise ContextError("update_business_unit", "isAdmin or storeKey")
