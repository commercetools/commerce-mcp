from __future__ import annotations

from typing import TYPE_CHECKING
from .schemas import ReadApprovalFlowParams, UpdateApprovalFlowParams
from ...shared.errors import ContextError
from . import admin_functions, associate_functions

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_approval_flow(
    params: ReadApprovalFlowParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Mirrors contextToApprovalFlowFunctionMapping — associate context takes priority.
    if ctx.customer_id and ctx.business_unit_key:
        return await associate_functions.read_approval_flow(params, api, ctx)
    if ctx.is_admin:
        return await admin_functions.read_approval_flow(params, api, ctx)
    raise ContextError("read_approval_flow", "isAdmin or customerId+businessUnitKey")


async def update_approval_flow(
    params: UpdateApprovalFlowParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await associate_functions.update_approval_flow(params, api, ctx)
    if ctx.is_admin:
        return await admin_functions.update_approval_flow(params, api, ctx)
    raise ContextError("update_approval_flow", "isAdmin or customerId+businessUnitKey")
