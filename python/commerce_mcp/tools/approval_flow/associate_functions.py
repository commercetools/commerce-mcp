from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadApprovalFlowParams, UpdateApprovalFlowParams
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


async def read_approval_flow(
    params: ReadApprovalFlowParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        prefix = _prefix(ctx)
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
    except Exception as e:
        raise SDKError("read approval flow as associate", e)


async def update_approval_flow(
    params: UpdateApprovalFlowParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        prefix = _prefix(ctx)
        body: dict[str, Any] = {"version": params.version, "actions": params.actions}
        result = await api.post(f"{prefix}/approval-flows/{params.id}", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update approval flow as associate", e)
