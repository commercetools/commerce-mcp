from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadApprovalFlowParams, UpdateApprovalFlowParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


def _prefix(params_associate_id: str, params_business_unit_key: str) -> str:
    return (
        f"/as-associate/{params_associate_id}"
        f"/in-business-unit/key={params_business_unit_key}"
    )


async def read_approval_flow(
    params: ReadApprovalFlowParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not params.associate_id:
        raise ValueError("associateId is required for admin approval flow operations")
    if not params.business_unit_key:
        raise ValueError("businessUnitKey is required for admin approval flow operations")
    try:
        prefix = _prefix(params.associate_id, params.business_unit_key)
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{prefix}/approval-flows/{params.id}", params=query or None)
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
        result = await api.get(f"{prefix}/approval-flows", params=query)
        return transform_tool_output(result)
    except ValueError:
        raise
    except Exception as e:
        raise SDKError("read approval flow", e)


async def update_approval_flow(
    params: UpdateApprovalFlowParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not params.associate_id:
        raise ValueError("associateId is required for admin approval flow operations")
    if not params.business_unit_key:
        raise ValueError("businessUnitKey is required for admin approval flow operations")
    try:
        prefix = _prefix(params.associate_id, params.business_unit_key)
        body: dict[str, Any] = {"version": params.version, "actions": params.actions}
        result = await api.post(f"{prefix}/approval-flows/{params.id}", body=body)
        return transform_tool_output(result)
    except ValueError:
        raise
    except Exception as e:
        raise SDKError("update approval flow", e)
