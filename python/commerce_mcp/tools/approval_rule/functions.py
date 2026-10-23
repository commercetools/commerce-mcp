from __future__ import annotations

from typing import TYPE_CHECKING
from .schemas import ReadApprovalRuleParams, CreateApprovalRuleParams, UpdateApprovalRuleParams
from ...shared.errors import ContextError
from . import admin_functions, associate_functions

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_approval_rule(
    params: ReadApprovalRuleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Mirrors contextToApprovalRuleFunctionMapping — associate context takes priority.
    if ctx.customer_id and ctx.business_unit_key:
        return await associate_functions.read_approval_rule(params, api, ctx)
    if ctx.is_admin:
        return await admin_functions.read_approval_rule(params, api, ctx)
    raise ContextError("read_approval_rule", "isAdmin or customerId+businessUnitKey")


async def create_approval_rule(
    params: CreateApprovalRuleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await associate_functions.create_approval_rule(params, api, ctx)
    if ctx.is_admin:
        return await admin_functions.create_approval_rule(params, api, ctx)
    raise ContextError("create_approval_rule", "isAdmin or customerId+businessUnitKey")


async def update_approval_rule(
    params: UpdateApprovalRuleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await associate_functions.update_approval_rule(params, api, ctx)
    if ctx.is_admin:
        return await admin_functions.update_approval_rule(params, api, ctx)
    raise ContextError("update_approval_rule", "isAdmin or customerId+businessUnitKey")
