from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import CreateCustomObjectParams, ReadCustomObjectParams, UpdateCustomObjectParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_custom_object(
    params: ReadCustomObjectParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("read_custom_object", "isAdmin")
    try:
        if params.container and params.key:
            result = await api.get(f"/custom-objects/{params.container}/{params.key}")
            return transform_tool_output(result)
        if params.container:
            query: dict[str, Any] = {}
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
            result = await api.get(f"/custom-objects/{params.container}", params=query or None)
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
        result = await api.get("/custom-objects", params=query or None)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("read custom object", e)


async def create_custom_object(
    params: CreateCustomObjectParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_custom_object", "isAdmin")
    try:
        body: dict[str, Any] = {
            "container": params.container,
            "key": params.key,
            "value": params.value,
        }
        if params.version is not None:
            body["version"] = params.version
        result = await api.post("/custom-objects", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("create custom object", e)


async def update_custom_object(
    params: UpdateCustomObjectParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_custom_object", "isAdmin")
    try:
        body: dict[str, Any] = {
            "container": params.container,
            "key": params.key,
            "value": params.value,
        }
        if params.version is not None:
            body["version"] = params.version
        result = await api.post("/custom-objects", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("update custom object", e)
