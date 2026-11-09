from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadAssociateRoleParams, CreateAssociateRoleParams, UpdateAssociateRoleParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_associate_role(
    params: ReadAssociateRoleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/associate-roles/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/associate-roles/key={params.key}", params=query or None)
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
        result = await api.get("/associate-roles", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read associate role", e)


async def create_associate_role(
    params: CreateAssociateRoleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body: dict[str, Any] = {
            "key": params.key,
            "buyerAssignable": params.buyer_assignable,
        }
        if params.name:
            body["name"] = params.name
        if params.permissions:
            body["permissions"] = params.permissions
        if params.custom:
            body["custom"] = params.custom
        result = await api.post("/associate-roles", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create associate role", e)


async def update_associate_role(
    params: UpdateAssociateRoleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body: dict[str, Any] = {"version": params.version, "actions": params.actions}
        if params.id:
            result = await api.post(f"/associate-roles/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/associate-roles/key={params.key}", body=body)
            return transform_tool_output(result)
        raise ValueError("Either id or key must be provided to update an associate role")
    except Exception as e:
        raise SDKError("update associate role", e)
