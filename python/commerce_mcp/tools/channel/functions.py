from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import CreateChannelParams, ReadChannelParams, UpdateChannelParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_channel(
    params: ReadChannelParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("read_channel", "isAdmin")
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/channels/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/channels/key={params.key}", params=query or None)
            return transform_tool_output(result)
        query = {"limit": params.limit if params.limit is not None else 20}
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.where:
            query["where"] = params.where
        if params.expand:
            query["expand"] = params.expand
        result = await api.get("/channels", params=query)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("read channel", e)


async def create_channel(
    params: CreateChannelParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_channel", "isAdmin")
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/channels", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("create channel", e)


async def update_channel(
    params: UpdateChannelParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_channel", "isAdmin")
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/channels/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/channels/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update channel", Exception("Either id or key must be provided"))
    except ContextError:
        raise
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update channel", e)
