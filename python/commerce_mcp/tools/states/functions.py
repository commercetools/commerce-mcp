from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadStateParams, CreateStateParams, UpdateStateParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_state(
    params: ReadStateParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("read_state", "isAdmin")
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/states/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/states/key={params.key}", params=query or None)
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
        result = await api.get("/states", params=query)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("read state", e)


async def create_state(
    params: CreateStateParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_state", "isAdmin")
    try:
        body: dict[str, Any] = {"key": params.key, "type": params.type}
        if params.initial is not None:
            body["initial"] = params.initial
        if params.name:
            body["name"] = params.name
        if params.description:
            body["description"] = params.description
        if params.roles:
            body["roles"] = params.roles
        if params.transitions:
            body["transitions"] = params.transitions
        result = await api.post("/states", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("create state", e)


async def update_state(
    params: UpdateStateParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_state", "isAdmin")
    try:
        body: dict[str, Any] = {"version": params.version, "actions": params.actions}
        if params.id:
            result = await api.post(f"/states/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/states/key={params.key}", body=body)
            return transform_tool_output(result)
        raise ValueError("Either id or key must be provided to update a state")
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("update state", e)
