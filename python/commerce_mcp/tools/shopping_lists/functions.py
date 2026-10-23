from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import ReadShoppingListParams, CreateShoppingListParams, UpdateShoppingListParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


# ── Customer helpers ──────────────────────────────────────────────────────────

async def _read_shopping_list_customer(
    params: ReadShoppingListParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Customer context: use /me/shopping-lists, injecting customer filter."""
    try:
        # Build customer filter — always include customer(id=...)
        customer_where = [f'customer(id="{ctx.customer_id}")']
        combined_where = (customer_where + list(params.where)) if params.where else customer_where

        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/me/shopping-lists/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/me/shopping-lists/key={params.key}", params=query or None)
            return transform_tool_output(result)
        query = {"where": combined_where}
        if params.limit is not None:
            query["limit"] = params.limit
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.expand:
            query["expand"] = params.expand
        result = await api.get("/me/shopping-lists", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read shopping list", e)


async def _create_shopping_list_customer(
    params: CreateShoppingListParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        # Ensure customer is set
        if "customer" not in body:
            body["customer"] = {"id": ctx.customer_id, "typeId": "customer"}
        result = await api.post("/me/shopping-lists", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create shopping list", e)


async def _update_shopping_list_customer(
    params: UpdateShoppingListParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/me/shopping-lists/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/me/shopping-lists/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update shopping list", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update shopping list", e)


# ── Store helpers ─────────────────────────────────────────────────────────────

async def _read_shopping_list_store(
    params: ReadShoppingListParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = f"/in-store/key={ctx.store_key}/shopping-lists"
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
        raise SDKError("read shopping list", e)


async def _create_shopping_list_store(
    params: CreateShoppingListParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        # Ensure store is set
        if "store" not in body:
            body["store"] = {"key": ctx.store_key, "typeId": "store"}
        result = await api.post(f"/in-store/key={ctx.store_key}/shopping-lists", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create shopping list", e)


async def _update_shopping_list_store(
    params: UpdateShoppingListParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        base = f"/in-store/key={ctx.store_key}/shopping-lists"
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
        raise SDKError("update shopping list", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update shopping list", e)


# ── Admin helpers ─────────────────────────────────────────────────────────────

async def _read_shopping_list_admin(
    params: ReadShoppingListParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        # Admin may pass storeKey param to route to store endpoint
        store_key = params.store_key
        if store_key:
            return await _read_shopping_list_store(
                ReadShoppingListParams(
                    id=params.id,
                    key=params.key,
                    limit=params.limit,
                    offset=params.offset,
                    sort=params.sort,
                    where=params.where,
                    expand=params.expand,
                ),
                api,
                type("_Ctx", (), {"store_key": store_key})(),
            )
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/shopping-lists/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/shopping-lists/key={params.key}", params=query or None)
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
        result = await api.get("/shopping-lists", params=query or None)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read shopping list", e)


async def _create_shopping_list_admin(
    params: CreateShoppingListParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        # Honour storeKey param if provided
        store_key = params.store_key
        if store_key:
            result = await api.post(f"/in-store/key={store_key}/shopping-lists", body=body)
        else:
            result = await api.post("/shopping-lists", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create shopping list", e)


async def _update_shopping_list_admin(
    params: UpdateShoppingListParams,
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
            result = await api.post(f"{prefix}/shopping-lists/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"{prefix}/shopping-lists/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update shopping list", Exception("Either id or key must be provided"))
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update shopping list", e)


# ── Public dispatchers ────────────────────────────────────────────────────────

async def read_shopping_list(
    params: ReadShoppingListParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Mirrors contextToShoppingListFunctionMapping
    if ctx.customer_id:
        return await _read_shopping_list_customer(params, api, ctx)
    if ctx.store_key:
        return await _read_shopping_list_store(params, api, ctx)
    if ctx.is_admin:
        return await _read_shopping_list_admin(params, api, ctx)
    raise ContextError(
        "read_shopping_list", "isAdmin, customerId, or storeKey"
    )


async def create_shopping_list(
    params: CreateShoppingListParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id:
        return await _create_shopping_list_customer(params, api, ctx)
    if ctx.store_key:
        return await _create_shopping_list_store(params, api, ctx)
    if ctx.is_admin:
        return await _create_shopping_list_admin(params, api, ctx)
    raise ContextError(
        "create_shopping_list", "isAdmin, customerId, or storeKey"
    )


async def update_shopping_list(
    params: UpdateShoppingListParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.customer_id:
        return await _update_shopping_list_customer(params, api, ctx)
    if ctx.store_key:
        return await _update_shopping_list_store(params, api, ctx)
    if ctx.is_admin:
        return await _update_shopping_list_admin(params, api, ctx)
    raise ContextError(
        "update_shopping_list", "isAdmin, customerId, or storeKey"
    )
