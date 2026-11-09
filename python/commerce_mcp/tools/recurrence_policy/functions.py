from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadRecurrencePolicyParams, CreateRecurrencePolicyParams, UpdateRecurrencePolicyParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_recurrence_policy(
    params: ReadRecurrencePolicyParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("read_recurrence_policy", "isAdmin")
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/recurrence-policies/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/recurrence-policies/key={params.key}", params=query or None)
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
        result = await api.get("/recurrence-policies", params=query)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("read recurrence policy", e)


async def create_recurrence_policy(
    params: CreateRecurrencePolicyParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_recurrence_policy", "isAdmin")
    try:
        body: dict[str, Any] = {"key": params.key, "schedule": params.schedule}
        if params.name:
            body["name"] = params.name
        if params.description:
            body["description"] = params.description
        result = await api.post("/recurrence-policies", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("create recurrence policy", e)


async def update_recurrence_policy(
    params: UpdateRecurrencePolicyParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_recurrence_policy", "isAdmin")
    try:
        body: dict[str, Any] = {"version": params.version, "actions": params.actions}
        if params.id:
            result = await api.post(f"/recurrence-policies/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/recurrence-policies/key={params.key}", body=body)
            return transform_tool_output(result)
        raise ValueError("Either id or key must be provided to update a recurrence policy")
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("update recurrence policy", e)
