from __future__ import annotations

from typing import TYPE_CHECKING
from .schemas import ReadCartParams, CreateCartParams, ReplicateCartParams, UpdateCartParams
from ...shared.errors import ContextError
from . import admin_functions as admin
from . import customer_functions as customer
from . import store_functions as store
from . import as_associate_functions as associate

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_cart(
    params: ReadCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await associate.read_cart(params, api, ctx)
    if ctx.customer_id:
        return await customer.read_cart(params, api, ctx)
    if ctx.store_key:
        return await store.read_cart(params, api, ctx)
    if ctx.is_admin:
        return await admin.read_cart(params, api, ctx)
    raise ContextError("read_cart", "isAdmin, customerId, storeKey, or customerId+businessUnitKey")


async def create_cart(
    params: CreateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await associate.create_cart(params, api, ctx)
    if ctx.customer_id:
        return await customer.create_cart(params, api, ctx)
    if ctx.store_key:
        return await store.create_cart(params, api, ctx)
    if ctx.is_admin:
        return await admin.create_cart(params, api, ctx)
    raise ContextError("create_cart", "isAdmin, customerId, storeKey, or customerId+businessUnitKey")


async def replicate_cart(
    params: ReplicateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await associate.replicate_cart(params, api, ctx)
    if ctx.customer_id:
        return await customer.replicate_cart(params, api, ctx)
    if ctx.store_key:
        return await store.replicate_cart(params, api, ctx)
    if ctx.is_admin:
        return await admin.replicate_cart(params, api, ctx)
    raise ContextError("replicate_cart", "isAdmin, customerId, storeKey, or customerId+businessUnitKey")


async def update_cart(
    params: UpdateCartParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await associate.update_cart(params, api, ctx)
    if ctx.customer_id:
        return await customer.update_cart(params, api, ctx)
    if ctx.store_key:
        return await store.update_cart(params, api, ctx)
    if ctx.is_admin:
        return await admin.update_cart(params, api, ctx)
    raise ContextError("update_cart", "isAdmin, customerId, storeKey, or customerId+businessUnitKey")
