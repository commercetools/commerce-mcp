from __future__ import annotations

from typing import TYPE_CHECKING
from .schemas import ReadOrderParams, CreateOrderParams, UpdateOrderParams
from ...shared.errors import ContextError
from . import admin_functions, customer_functions, store_functions, as_associate_functions

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_order(
    params: ReadOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Mirrors contextToOrderFunctionMapping — explicit context required, no fallthrough.
    if ctx.customer_id and ctx.business_unit_key:
        return await as_associate_functions.read_order(params, api, ctx)
    if ctx.customer_id:
        return await customer_functions.read_order(params, api, ctx)
    if ctx.store_key:
        return await store_functions.read_order(params, api, ctx)
    if ctx.is_admin:
        return await admin_functions.read_order(params, api, ctx)
    raise ContextError(
        "read_order", "isAdmin, customerId, storeKey, or customerId+businessUnitKey"
    )


async def create_order(
    params: CreateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Customer-only context cannot create orders — matches contextToOrderFunctionMapping.
    if ctx.customer_id and ctx.business_unit_key:
        return await as_associate_functions.create_order(params, api, ctx)
    if ctx.store_key:
        return await store_functions.create_order(params, api, ctx)
    if ctx.is_admin:
        return await admin_functions.create_order(params, api, ctx)
    raise ContextError(
        "create_order", "isAdmin, storeKey, or customerId+businessUnitKey"
    )


async def update_order(
    params: UpdateOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Customer-only context cannot update orders — matches contextToOrderFunctionMapping.
    if ctx.customer_id and ctx.business_unit_key:
        return await as_associate_functions.update_order(params, api, ctx)
    if ctx.store_key:
        return await store_functions.update_order(params, api, ctx)
    if ctx.is_admin:
        return await admin_functions.update_order(params, api, ctx)
    raise ContextError(
        "update_order", "isAdmin, storeKey, or customerId+businessUnitKey"
    )
