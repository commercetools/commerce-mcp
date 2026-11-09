from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import CreateRecurringOrdersParams, ReadRecurringOrdersParams, UpdateRecurringOrdersParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


# ── Customer helpers ──────────────────────────────────────────────────────────

async def _read_recurring_orders_customer(
    params: ReadRecurringOrdersParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Read recurring orders filtered to the current customer."""
    try:
        customer_filter = f'customerId="{ctx.customer_id}"'

        if params.id:
            query: dict[str, Any] = {
                "where": [f'id="{params.id}"', customer_filter],
                "limit": 1,
            }
            if params.expand:
                query["expand"] = params.expand
            result = await api.get("/recurring-orders", params=query)
            results = result.get("results", [])
            if not results:
                raise Exception(
                    f"Recurring order with ID {params.id} not found for customer {ctx.customer_id}"
                )
            return transform_tool_output(results[0])

        if params.key:
            query = {
                "where": [f'key="{params.key}"', customer_filter],
                "limit": 1,
            }
            if params.expand:
                query["expand"] = params.expand
            result = await api.get("/recurring-orders", params=query)
            results = result.get("results", [])
            if not results:
                raise Exception(
                    f"Recurring order with key {params.key} not found for customer {ctx.customer_id}"
                )
            return transform_tool_output(results[0])

        # List — inject customer filter
        where = list(params.where or [])
        where.append(customer_filter)
        query = {"where": where}
        if params.limit is not None:
            query["limit"] = params.limit
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.expand:
            query["expand"] = params.expand
        result = await api.get("/recurring-orders", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read recurring orders", e)


# ── Admin helpers ─────────────────────────────────────────────────────────────

async def _read_recurring_orders_admin(
    params: ReadRecurringOrdersParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/recurring-orders/{params.id}", params=query or None)
            return transform_tool_output(result)

        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/recurring-orders/key={params.key}", params=query or None)
            return transform_tool_output(result)

        query = {"limit": params.limit if params.limit is not None else 20}
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.where:
            query["where"] = params.where
        if params.expand:
            query["expand"] = params.expand
        result = await api.get("/recurring-orders", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read recurring orders", e)


# ── Public dispatch functions ─────────────────────────────────────────────────

async def read_recurring_orders(
    params: ReadRecurringOrdersParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id:
        return await _read_recurring_orders_customer(params, api, ctx)
    if ctx.is_admin:
        return await _read_recurring_orders_admin(params, api, ctx)
    raise ContextError("read_recurring_orders", "isAdmin or customerId")


async def create_recurring_orders(
    params: CreateRecurringOrdersParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_recurring_orders", "isAdmin")
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/recurring-orders", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("create recurring orders", e)


async def update_recurring_orders(
    params: UpdateRecurringOrdersParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_recurring_orders", "isAdmin")
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/recurring-orders/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/recurring-orders/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError(
            "update recurring orders",
            Exception("Either id or key must be provided"),
        )
    except ContextError:
        raise
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update recurring orders", e)
