from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadApprovalRuleParams, CreateApprovalRuleParams, UpdateApprovalRuleParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


def _prefix(associate_id: str, business_unit_key: str) -> str:
    return (
        f"/as-associate/{associate_id}"
        f"/in-business-unit/key={business_unit_key}"
    )


def _require_identity(params_associate_id: str | None, params_business_unit_key: str | None) -> tuple[str, str]:
    if not params_associate_id:
        raise ValueError("associateId is required for admin approval rule operations")
    if not params_business_unit_key:
        raise ValueError("businessUnitKey is required for admin approval rule operations")
    return params_associate_id, params_business_unit_key


async def read_approval_rule(
    params: ReadApprovalRuleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    associate_id, bu_key = _require_identity(params.associate_id, params.business_unit_key)
    try:
        prefix = _prefix(associate_id, bu_key)
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
    except ValueError:
        raise
    except Exception as e:
        raise SDKError("read approval rule", e)


async def create_approval_rule(
    params: CreateApprovalRuleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    associate_id, bu_key = _require_identity(params.associate_id, params.business_unit_key)
    try:
        prefix = _prefix(associate_id, bu_key)
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
    except ValueError:
        raise
    except Exception as e:
        raise SDKError("create approval rule", e)


async def update_approval_rule(
    params: UpdateApprovalRuleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    associate_id, bu_key = _require_identity(params.associate_id, params.business_unit_key)
    try:
        prefix = _prefix(associate_id, bu_key)
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
        raise SDKError("update approval rule", e)
