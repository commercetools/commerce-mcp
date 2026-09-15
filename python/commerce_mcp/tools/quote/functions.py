from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import ReadQuoteParams, CreateQuoteParams, UpdateQuoteParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


# ── Associate helpers ─────────────────────────────────────────────────────────

async def _read_quote_associate(
    params: ReadQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Associate context: /as-associate/{customerId}/in-business-unit/key={businessUnitKey}/quotes"""
    try:
        base = (
            f"/as-associate/{ctx.customer_id}"
            f"/in-business-unit/key={ctx.business_unit_key}"
            f"/quotes"
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
        raise SDKError("read quote", e)


async def _update_quote_associate(
    params: UpdateQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Associate context update — validates allowed actions then posts."""
    try:
        base = (
            f"/as-associate/{ctx.customer_id}"
            f"/in-business-unit/key={ctx.business_unit_key}"
            f"/quotes"
        )
        # Validate allowed actions for associates
        allowed_associate_actions = {"changeQuoteState", "requestQuoteRenegotiation", "changeCustomer"}
        for action in params.actions:
            if action.action not in allowed_associate_actions:
                raise SDKError(
                    "update quote",
                    Exception(f"Action '{action.action}' is not allowed for associates"),
                )
            if action.action == "changeQuoteState":
                action_data = action.model_dump(by_alias=True, exclude_none=True)
                quote_state = action_data.get("quoteState")
                if quote_state not in ("Accepted", "Declined"):
                    raise SDKError(
                        "update quote",
                        Exception(f"Quote state '{quote_state}' is not allowed for associates"),
                    )

        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        query: dict[str, Any] = {}
        if params.expand:
            query["expand"] = params.expand

        if params.id:
            result = await api.post(f"{base}/{params.id}", body=body, params=query or None)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"{base}/key={params.key}", body=body, params=query or None)
            return transform_tool_output(result)
        raise SDKError("update quote", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update quote", e)


# ── Customer helpers ──────────────────────────────────────────────────────────

async def _read_quote_customer(
    params: ReadQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Customer context: /me/quotes with ownership check."""
    try:
        store_key = params.store_key
        prefix = f"/in-store/key={store_key}" if store_key else ""

        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{prefix}/quotes/{params.id}", params=query or None)
            # Ownership check: customer(id) must match
            if isinstance(result, dict):
                customer_info = result.get("customer", {})
                if customer_info.get("id") != ctx.customer_id:
                    raise SDKError("read quote", Exception("Quote not found"))
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{prefix}/quotes/key={params.key}", params=query or None)
            if isinstance(result, dict):
                customer_info = result.get("customer", {})
                if customer_info.get("id") != ctx.customer_id:
                    raise SDKError("read quote", Exception("Quote not found"))
            return transform_tool_output(result)
        # Query with customer filter
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
        result = await api.get(f"{prefix}/quotes", params=query)
        return transform_tool_output(result)
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("read quote", e)


async def _update_quote_customer(
    params: UpdateQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Customer context update — validates allowed actions."""
    try:
        store_key = params.store_key
        prefix = f"/in-store/key={store_key}" if store_key else ""

        # Validate allowed actions for customers
        allowed_customer_actions = {"changeQuoteState", "requestQuoteRenegotiation"}
        for action in params.actions:
            if action.action not in allowed_customer_actions:
                raise SDKError(
                    "update quote",
                    Exception(f"Action '{action.action}' is not allowed for customers"),
                )
            if action.action == "changeQuoteState":
                action_data = action.model_dump(by_alias=True, exclude_none=True)
                quote_state = action_data.get("quoteState")
                if quote_state not in ("Accepted", "Declined"):
                    raise SDKError(
                        "update quote",
                        Exception(f"Quote state '{quote_state}' is not allowed for customers"),
                    )

        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        query: dict[str, Any] = {}
        if params.expand:
            query["expand"] = params.expand

        if params.id:
            result = await api.post(f"{prefix}/quotes/{params.id}", body=body, params=query or None)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"{prefix}/quotes/key={params.key}", body=body, params=query or None)
            return transform_tool_output(result)
        raise SDKError("update quote", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update quote", e)


# ── Store helpers ─────────────────────────────────────────────────────────────

async def _read_quote_store(
    params: ReadQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        store_key = params.store_key or ctx.store_key
        base = f"/in-store/key={store_key}/quotes"
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
        # Query with store filter
        store_where = [f'store(key="{store_key}")']
        combined_where = (store_where + list(params.where)) if params.where else store_where
        query = {"where": combined_where}
        if params.limit is not None:
            query["limit"] = params.limit
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.expand:
            query["expand"] = params.expand
        result = await api.get(base, params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read quote", e)


async def _create_quote_store(
    params: CreateQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        store_key = params.store_key or ctx.store_key
        body: dict[str, Any] = {
            "stagedQuote": params.staged_quote.model_dump(by_alias=True, exclude_none=True),
            "stagedQuoteVersion": params.staged_quote_version,
            "stagedQuoteStateToSent": params.staged_quote_state_to_sent,
        }
        if params.key:
            body["key"] = params.key
        if params.state:
            body["state"] = params.state.model_dump(by_alias=True, exclude_none=True)
        if params.custom:
            body["custom"] = params.custom.model_dump(by_alias=True, exclude_none=True)
        query: dict[str, Any] = {}
        if params.expand:
            query["expand"] = params.expand
        result = await api.post(f"/in-store/key={store_key}/quotes", body=body, params=query or None)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create quote", e)


async def _update_quote_store(
    params: UpdateQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        store_key = params.store_key or ctx.store_key
        base = f"/in-store/key={store_key}/quotes"
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        query: dict[str, Any] = {}
        if params.expand:
            query["expand"] = params.expand
        if params.id:
            result = await api.post(f"{base}/{params.id}", body=body, params=query or None)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"{base}/key={params.key}", body=body, params=query or None)
            return transform_tool_output(result)
        raise SDKError("update quote", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update quote", e)


# ── Admin helpers ─────────────────────────────────────────────────────────────

async def _read_quote_admin(
    params: ReadQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        store_key = params.store_key
        prefix = f"/in-store/key={store_key}" if store_key else ""
        base = f"{prefix}/quotes"
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
        raise SDKError("read quote", e)


async def _create_quote_admin(
    params: CreateQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        store_key = params.store_key
        prefix = f"/in-store/key={store_key}" if store_key else ""
        body: dict[str, Any] = {
            "stagedQuote": params.staged_quote.model_dump(by_alias=True, exclude_none=True),
            "stagedQuoteVersion": params.staged_quote_version,
            "stagedQuoteStateToSent": params.staged_quote_state_to_sent,
        }
        if params.key:
            body["key"] = params.key
        if params.state:
            body["state"] = params.state.model_dump(by_alias=True, exclude_none=True)
        if params.custom:
            body["custom"] = params.custom.model_dump(by_alias=True, exclude_none=True)
        query: dict[str, Any] = {}
        if params.expand:
            query["expand"] = params.expand
        result = await api.post(f"{prefix}/quotes", body=body, params=query or None)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create quote", e)


async def _update_quote_admin(
    params: UpdateQuoteParams,
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
        query: dict[str, Any] = {}
        if params.expand:
            query["expand"] = params.expand
        if params.id:
            result = await api.post(f"{prefix}/quotes/{params.id}", body=body, params=query or None)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"{prefix}/quotes/key={params.key}", body=body, params=query or None)
            return transform_tool_output(result)
        raise SDKError("update quote", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update quote", e)


# ── Public dispatchers ────────────────────────────────────────────────────────

async def read_quote(
    params: ReadQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Mirrors contextToQuoteFunctionMapping
    if ctx.customer_id and ctx.business_unit_key:
        return await _read_quote_associate(params, api, ctx)
    if ctx.customer_id:
        return await _read_quote_customer(params, api, ctx)
    if ctx.store_key:
        return await _read_quote_store(params, api, ctx)
    if ctx.is_admin:
        return await _read_quote_admin(params, api, ctx)
    raise ContextError(
        "read_quote", "isAdmin, customerId, storeKey, or customerId+businessUnitKey"
    )


async def create_quote(
    params: CreateQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # No create for associate or customer-only — matches contextToQuoteFunctionMapping
    if ctx.store_key:
        return await _create_quote_store(params, api, ctx)
    if ctx.is_admin:
        return await _create_quote_admin(params, api, ctx)
    raise ContextError(
        "create_quote", "isAdmin or storeKey"
    )


async def update_quote(
    params: UpdateQuoteParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await _update_quote_associate(params, api, ctx)
    if ctx.customer_id:
        return await _update_quote_customer(params, api, ctx)
    if ctx.store_key:
        return await _update_quote_store(params, api, ctx)
    if ctx.is_admin:
        return await _update_quote_admin(params, api, ctx)
    raise ContextError(
        "update_quote", "isAdmin, customerId, storeKey, or customerId+businessUnitKey"
    )
