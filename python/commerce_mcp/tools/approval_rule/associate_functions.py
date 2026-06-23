from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadApprovalRuleParams, CreateApprovalRuleParams, UpdateApprovalRuleParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


def _prefix(ctx: "CTContext") -> str:
    return (
        f"/as-associate/{ctx.customer_id}"
        f"/in-business-unit/key={ctx.business_unit_key}"
    )


async def read_approval_rule(
    params: ReadApprovalRuleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        prefix = _prefix(ctx)
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{prefix}/approval-rules/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{prefix}/approval-rules/key={params.key}", params=query or None)
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
        result = await api.get(f"{prefix}/approval-rules", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read approval rule as associate", e)


async def create_approval_rule(
    params: CreateApprovalRuleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        prefix = _prefix(ctx)
        body: dict[str, Any] = {
            "name": params.name,
            "predicate": params.predicate,
            "approvers": params.approvers,
            "requesters": params.requesters,
            "status": params.status,
        }
        if params.key:
            body["key"] = params.key
        if params.description:
            body["description"] = params.description
        result = await api.post(f"{prefix}/approval-rules", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create approval rule as associate", e)


async def update_approval_rule(
    params: UpdateApprovalRuleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        prefix = _prefix(ctx)
        body: dict[str, Any] = {"version": params.version, "actions": params.actions}
        if params.id:
            result = await api.post(f"{prefix}/approval-rules/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"{prefix}/approval-rules/key={params.key}", body=body)
            return transform_tool_output(result)
        raise ValueError("Either id or key must be provided to update an approval rule")
    except ValueError:
        raise
    except Exception as e:
        raise SDKError("update approval rule as associate", e)
