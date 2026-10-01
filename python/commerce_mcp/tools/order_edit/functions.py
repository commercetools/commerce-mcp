from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadOrderEditParams, CreateOrderEditParams, UpdateOrderEditParams, ApplyOrderEditParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_order_edit(
    params: ReadOrderEditParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("read_order_edit", "isAdmin")
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/orders/edits/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/orders/edits/key={params.key}", params=query or None)
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
        result = await api.get("/orders/edits", params=query)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("read order edit", e)


async def create_order_edit(
    params: CreateOrderEditParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_order_edit", "isAdmin")
    try:
        body: dict[str, Any] = {"resource": params.resource}
        if params.staged_actions is not None:
            body["stagedActions"] = params.staged_actions
        if params.key:
            body["key"] = params.key
        if params.comment:
            body["comment"] = params.comment
        if params.dry_run is not None:
            body["dryRun"] = params.dry_run
        if params.custom:
            body["custom"] = params.custom
        result = await api.post("/orders/edits", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("create order edit", e)


async def update_order_edit(
    params: UpdateOrderEditParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_order_edit", "isAdmin")
    try:
        body: dict[str, Any] = {"version": params.version, "actions": params.actions}
        if params.dry_run is not None:
            body["dryRun"] = params.dry_run
        if params.id:
            result = await api.post(f"/orders/edits/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/orders/edits/key={params.key}", body=body)
            return transform_tool_output(result)
        raise ValueError("Either id or key must be provided to update an order edit")
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("update order edit", e)


async def apply_order_edit(
    params: ApplyOrderEditParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("apply_order_edit", "isAdmin")
    try:
        body: dict[str, Any] = {
            "editVersion": params.edit_version,
            "resourceVersion": params.resource_version,
        }
        result = await api.post(f"/orders/edits/{params.id}/apply", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("apply order edit", e)
