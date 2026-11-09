from __future__ import annotations

from typing import TYPE_CHECKING
from .schemas import ReadAssociateRoleParams, CreateAssociateRoleParams, UpdateAssociateRoleParams
from ...shared.errors import ContextError
from . import admin_functions, associate_functions

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_associate_role(
    params: ReadAssociateRoleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Mirrors contextToAssociateRoleFunctionMapping — both contexts share same URL.
    if ctx.customer_id and ctx.business_unit_key:
        return await associate_functions.read_associate_role(params, api, ctx)
    if ctx.is_admin:
        return await admin_functions.read_associate_role(params, api, ctx)
    raise ContextError("read_associate_role", "isAdmin or customerId+businessUnitKey")


async def create_associate_role(
    params: CreateAssociateRoleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Associates cannot create roles — admin only.
    if ctx.is_admin:
        return await admin_functions.create_associate_role(params, api, ctx)
    raise ContextError("create_associate_role", "isAdmin")


async def update_associate_role(
    params: UpdateAssociateRoleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Associates cannot update roles — admin only.
    if ctx.is_admin:
        return await admin_functions.update_associate_role(params, api, ctx)
    raise ContextError("update_associate_role", "isAdmin")
