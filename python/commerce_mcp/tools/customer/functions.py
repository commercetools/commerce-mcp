from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadCustomerParams, CreateCustomerParams, UpdateCustomerParams
from ...shared.errors import SDKError, ContextError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


# ── Customer (own profile) ────────────────────────────────────────────────────

async def _read_customer_self(
    params: ReadCustomerParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Customer reads their own profile. GET /customers/{customerId}"""
    try:
        query: dict[str, Any] = {}
        if params.expand:
            query["expand"] = params.expand
        result = await api.get(f"/customers/{ctx.customer_id}", params=query or None)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read customer profile", e)


# ── Store scope ───────────────────────────────────────────────────────────────

async def _read_customer_store(
    params: ReadCustomerParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Store reads a customer by ID or lists customers in the store.
    GET /in-store/key={storeKey}/customers/{id}
    GET /in-store/key={storeKey}/customers
    """
    try:
        base = f"/in-store/key={ctx.store_key}/customers"
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"{base}/{params.id}", params=query or None)
        else:
            query = {"limit": params.limit or 10}
            if params.offset is not None:
                query["offset"] = params.offset
            if params.sort:
                query["sort"] = params.sort
            if params.where:
                query["where"] = params.where
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(base, params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read customer in store", e)


async def _create_customer_store(
    params: CreateCustomerParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Store creates a customer. POST /in-store/key={storeKey}/customers"""
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        # Remove storeKey from body — it's in the URL path
        body.pop("storeKey", None)
        result = await api.post(f"/in-store/key={ctx.store_key}/customers", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create customer in store", e)


async def _update_customer_store(
    params: UpdateCustomerParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Store updates a customer. POST /in-store/key={storeKey}/customers/{id}"""
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        result = await api.post(
            f"/in-store/key={ctx.store_key}/customers/{params.id}",
            body=body,
        )
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update customer in store", e)


# ── Admin scope ───────────────────────────────────────────────────────────────

async def _read_customer_admin(
    params: ReadCustomerParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Admin reads a customer by ID (or with store key override) or lists all customers.
    GET /customers/{id}
    GET /in-store/key={storeKey}/customers/{id}  (when params.store_key provided)
    GET /customers
    """
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            if params.store_key:
                result = await api.get(
                    f"/in-store/key={params.store_key}/customers/{params.id}",
                    params=query or None,
                )
            else:
                result = await api.get(f"/customers/{params.id}", params=query or None)
        else:
            query = {"limit": params.limit or 10}
            if params.offset is not None:
                query["offset"] = params.offset
            if params.sort:
                query["sort"] = params.sort
            if params.where:
                query["where"] = params.where
            if params.expand:
                query["expand"] = params.expand
            result = await api.get("/customers", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read customer", e)


async def _create_customer_admin(
    params: CreateCustomerParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Admin creates a customer (optionally in a store).
    POST /in-store/key={storeKey}/customers  (when params.store_key provided)
    POST /customers
    """
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        store_key = body.pop("storeKey", None)
        if store_key:
            result = await api.post(f"/in-store/key={store_key}/customers", body=body)
        else:
            result = await api.post("/customers", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create customer", e)


async def _update_customer_admin(
    params: UpdateCustomerParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Admin updates a customer. POST /customers/{id}"""
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        result = await api.post(f"/customers/{params.id}", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update customer", e)


# ── Public dispatchers ────────────────────────────────────────────────────────

async def read_customer(
    params: ReadCustomerParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id:
        return await _read_customer_self(params, api, ctx)
    if ctx.store_key:
        return await _read_customer_store(params, api, ctx)
    if ctx.is_admin:
        return await _read_customer_admin(params, api, ctx)
    raise ContextError("read_customer", "isAdmin, customerId, or storeKey")


async def create_customer(
    params: CreateCustomerParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _create_customer_store(params, api, ctx)
    if ctx.is_admin:
        return await _create_customer_admin(params, api, ctx)
    raise ContextError("create_customer", "isAdmin or storeKey")


async def update_customer(
    params: UpdateCustomerParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.store_key:
        return await _update_customer_store(params, api, ctx)
    if ctx.is_admin:
        return await _update_customer_admin(params, api, ctx)
    raise ContextError("update_customer", "isAdmin or storeKey")
