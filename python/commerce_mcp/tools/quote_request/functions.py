from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import ReadQuoteRequestParams, CreateQuoteRequestParams, UpdateQuoteRequestParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


# ── Associate helpers ─────────────────────────────────────────────────────────

async def _read_quote_request_associate(
    params: ReadQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Associate context: /as-associate/{customerId}/in-business-unit/key={businessUnitKey}/quote-requests"""
    try:
        base = (
            f"/as-associate/{ctx.customer_id}"
            f"/in-business-unit/key={ctx.business_unit_key}"
            f"/quote-requests"
        )
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{base}/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{base}/key={params.key}", params=query or None)
            return transform_tool_output(result)
        query = {}
        if params.where:
            query["where"] = params.where
        if params.limit is not None:
            query["limit"] = params.limit
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.expand:
            query["expand"] = params.expand
        result = await api.get(base, params=query or None)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read quote request", e)


async def _create_quote_request_associate(
    params: CreateQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = (
            f"/as-associate/{ctx.customer_id}"
            f"/in-business-unit/key={ctx.business_unit_key}"
            f"/quote-requests"
        )
        body: dict[str, Any] = {
            "cart": params.cart.model_dump(by_alias=True, exclude_none=True),
            "cartVersion": params.cart_version,
        }
        if params.comment:
            body["comment"] = params.comment
        if params.key:
            body["key"] = params.key
        if params.custom:
            body["custom"] = params.custom
        result = await api.post(base, body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create quote request", e)


async def _update_quote_request_associate(
    params: UpdateQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = (
            f"/as-associate/{ctx.customer_id}"
            f"/in-business-unit/key={ctx.business_unit_key}"
            f"/quote-requests"
        )
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"{base}/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"{base}/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update quote request", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update quote request", e)


# ── Customer helpers ──────────────────────────────────────────────────────────

async def _read_quote_request_customer(
    params: ReadQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Customer-only context: read via /me/quote-requests (no create)."""
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/me/quote-requests/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/me/quote-requests/key={params.key}", params=query or None)
            return transform_tool_output(result)
        # Query with customer filter injected
        customer_where = [f'customer(id="{ctx.customer_id}")']
        combined_where = (customer_where + list(params.where)) if params.where else customer_where
        query = {"where": combined_where}
        if params.limit is not None:
            query["limit"] = params.limit
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.expand:
            query["expand"] = params.expand
        result = await api.get("/me/quote-requests", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read quote request", e)


async def _update_quote_request_customer(
    params: UpdateQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/me/quote-requests/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/me/quote-requests/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update quote request", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update quote request", e)


# ── Store helpers ─────────────────────────────────────────────────────────────

async def _read_quote_request_store(
    params: ReadQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = f"/in-store/key={ctx.store_key}/quote-requests"
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{base}/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{base}/key={params.key}", params=query or None)
            return transform_tool_output(result)
        query = {}
        if params.customer_id:
            query["where"] = [f'customer(id="{params.customer_id}")']
        elif params.where:
            query["where"] = params.where
        if params.limit is not None:
            query["limit"] = params.limit
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.expand:
            query["expand"] = params.expand
        result = await api.get(base, params=query or None)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read quote request", e)


async def _create_quote_request_store(
    params: CreateQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body: dict[str, Any] = {
            "cart": params.cart.model_dump(by_alias=True, exclude_none=True),
            "cartVersion": params.cart_version,
        }
        if params.comment:
            body["comment"] = params.comment
        if params.key:
            body["key"] = params.key
        if params.custom:
            body["custom"] = params.custom
        result = await api.post(f"/in-store/key={ctx.store_key}/quote-requests", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create quote request", e)


async def _update_quote_request_store(
    params: UpdateQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = f"/in-store/key={ctx.store_key}/quote-requests"
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"{base}/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"{base}/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update quote request", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update quote request", e)


# ── Admin helpers ─────────────────────────────────────────────────────────────

async def _read_quote_request_admin(
    params: ReadQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        store_key = params.store_key
        prefix = f"/in-store/key={store_key}" if store_key else ""
        base = f"{prefix}/quote-requests"
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{base}/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{base}/key={params.key}", params=query or None)
            return transform_tool_output(result)
        if params.customer_id:
            query = {"where": [f'customer(id="{params.customer_id}")'], "limit": params.limit or 10}
        else:
            query = {"limit": params.limit or 10}
            if params.where:
                query["where"] = params.where
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.expand:
            query["expand"] = params.expand
        result = await api.get(base, params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read quote request", e)


async def _create_quote_request_admin(
    params: CreateQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body: dict[str, Any] = {
            "cart": params.cart.model_dump(by_alias=True, exclude_none=True),
            "cartVersion": params.cart_version,
        }
        if params.comment:
            body["comment"] = params.comment
        if params.key:
            body["key"] = params.key
        if params.custom:
            body["custom"] = params.custom
        store_key = params.store_key
        prefix = f"/in-store/key={store_key}" if store_key else ""
        result = await api.post(f"{prefix}/quote-requests", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create quote request", e)


async def _update_quote_request_admin(
    params: UpdateQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        store_key = params.store_key
        prefix = f"/in-store/key={store_key}" if store_key else ""
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"{prefix}/quote-requests/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"{prefix}/quote-requests/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update quote request", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update quote request", e)


# ── Public dispatchers ────────────────────────────────────────────────────────

async def read_quote_request(
    params: ReadQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Mirrors contextToQuoteRequestFunctionMapping
    if ctx.customer_id and ctx.business_unit_key:
        return await _read_quote_request_associate(params, api, ctx)
    if ctx.customer_id:
        return await _read_quote_request_customer(params, api, ctx)
    if ctx.store_key:
        return await _read_quote_request_store(params, api, ctx)
    if ctx.is_admin:
        return await _read_quote_request_admin(params, api, ctx)
    raise ContextError(
        "read_quote_request",
        "isAdmin, customerId, storeKey, or customerId+businessUnitKey",
    )


async def create_quote_request(
    params: CreateQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Customer-only context has no create — matches contextToQuoteRequestFunctionMapping
    if ctx.customer_id and ctx.business_unit_key:
        return await _create_quote_request_associate(params, api, ctx)
    if ctx.store_key:
        return await _create_quote_request_store(params, api, ctx)
    if ctx.is_admin:
        return await _create_quote_request_admin(params, api, ctx)
    raise ContextError(
        "create_quote_request",
        "isAdmin, storeKey, or customerId+businessUnitKey",
    )


async def update_quote_request(
    params: UpdateQuoteRequestParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await _update_quote_request_associate(params, api, ctx)
    if ctx.customer_id:
        return await _update_quote_request_customer(params, api, ctx)
    if ctx.store_key:
        return await _update_quote_request_store(params, api, ctx)
    if ctx.is_admin:
        return await _update_quote_request_admin(params, api, ctx)
    raise ContextError(
        "update_quote_request",
        "isAdmin, customerId, storeKey, or customerId+businessUnitKey",
    )
