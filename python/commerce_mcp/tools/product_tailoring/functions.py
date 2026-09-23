from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import (
    ReadProductTailoringParams,
    CreateProductTailoringParams,
    UpdateProductTailoringParams,
)
from ...shared.errors import SDKError, ContextError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


# ── Admin scope ───────────────────────────────────────────────────────────────

async def _read_product_tailoring_admin(
    params: ReadProductTailoringParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Admin reads product tailoring entries.

    GET /product-tailoring/{id}
    GET /product-tailoring/key={key}
    GET /in-store/key={storeKey}/products/{productId}/product-tailoring
    GET /in-store/key={storeKey}/products/key={productKey}/product-tailoring
    GET /product-tailoring  (list)
    """
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/product-tailoring/{params.id}", params=query or None)
        elif params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/product-tailoring/key={params.key}", params=query or None)
        elif params.product_id and params.store_key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(
                f"/in-store/key={params.store_key}/products/{params.product_id}/product-tailoring",
                params=query or None,
            )
        elif params.product_key and params.store_key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(
                f"/in-store/key={params.store_key}/products/key={params.product_key}/product-tailoring",
                params=query or None,
            )
        else:
            query = {"limit": params.limit or 20}
            if params.offset is not None:
                query["offset"] = params.offset
            if params.sort:
                query["sort"] = params.sort
            if params.where:
                query["where"] = params.where
            if params.expand:
                query["expand"] = params.expand
            result = await api.get("/product-tailoring", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read product tailoring", e)


async def _create_product_tailoring_admin(
    params: CreateProductTailoringParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Admin creates a product tailoring entry.

    POST /in-store/key={storeKey}/product-tailoring
    POST /product-tailoring
    """
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)

        # Resolve product reference
        product_id = body.pop("productId", None)
        product_key = body.pop("productKey", None)
        store_key = body.pop("storeKey", None)

        if product_id and "product" not in body:
            body["product"] = {"typeId": "product", "id": product_id}
        elif product_key and "product" not in body:
            body["product"] = {"typeId": "product", "key": product_key}

        if store_key and "store" not in body:
            body["store"] = {"typeId": "store", "key": store_key}

        effective_store_key = store_key or (body.get("store") or {}).get("key")

        if effective_store_key:
            result = await api.post(
                f"/in-store/key={effective_store_key}/product-tailoring",
                body=body,
            )
        else:
            result = await api.post("/product-tailoring", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create product tailoring", e)


async def _update_product_tailoring_admin(
    params: UpdateProductTailoringParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Admin updates a product tailoring entry.

    POST /product-tailoring/{id}
    POST /product-tailoring/key={key}
    """
    try:
        actions = [
            a.model_dump(by_alias=True, exclude_none=True)
            for a in params.actions
            if a.action != "delete"
        ]
        body: dict[str, Any] = {"version": params.version, "actions": actions}

        if params.id:
            result = await api.post(f"/product-tailoring/{params.id}", body=body)
        elif params.key:
            result = await api.post(f"/product-tailoring/key={params.key}", body=body)
        else:
            raise ValueError(
                "Either id or key must be provided to update product tailoring"
            )
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update product tailoring", e)


# ── Store scope ───────────────────────────────────────────────────────────────

async def _read_product_tailoring_store(
    params: ReadProductTailoringParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Store reads product tailoring entries. Uses ctx.store_key for scoping.

    GET /product-tailoring/{id}
    GET /product-tailoring/key={key}
    GET /in-store/key={storeKey}/products/{productId}/product-tailoring
    GET /in-store/key={storeKey}/products/key={productKey}/product-tailoring
    GET /in-store/key={storeKey}/product-tailoring  (list)
    """
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/product-tailoring/{params.id}", params=query or None)
        elif params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/product-tailoring/key={params.key}", params=query or None)
        elif params.product_id:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(
                f"/in-store/key={ctx.store_key}/products/{params.product_id}/product-tailoring",
                params=query or None,
            )
        elif params.product_key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(
                f"/in-store/key={ctx.store_key}/products/key={params.product_key}/product-tailoring",
                params=query or None,
            )
        else:
            query = {"limit": params.limit or 20}
            if params.offset is not None:
                query["offset"] = params.offset
            if params.sort:
                query["sort"] = params.sort
            if params.where:
                query["where"] = params.where
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(
                f"/in-store/key={ctx.store_key}/product-tailoring",
                params=query,
            )
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read product tailoring", e)


async def _create_product_tailoring_store(
    params: CreateProductTailoringParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Store creates a product tailoring entry.

    POST /in-store/key={storeKey}/product-tailoring
    """
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)

        # Resolve product reference
        product_id = body.pop("productId", None)
        product_key = body.pop("productKey", None)
        body.pop("storeKey", None)

        if product_id and "product" not in body:
            body["product"] = {"typeId": "product", "id": product_id}
        elif product_key and "product" not in body:
            body["product"] = {"typeId": "product", "key": product_key}

        # Always use ctx.store_key for store context
        body["store"] = {"typeId": "store", "key": ctx.store_key}

        result = await api.post(
            f"/in-store/key={ctx.store_key}/product-tailoring",
            body=body,
        )
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create product tailoring", e)


async def _update_product_tailoring_store(
    params: UpdateProductTailoringParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Store updates a product tailoring entry.

    POST /product-tailoring/{id}
    POST /product-tailoring/key={key}
    """
    try:
        actions = [
            a.model_dump(by_alias=True, exclude_none=True)
            for a in params.actions
            if a.action != "delete"
        ]
        body: dict[str, Any] = {"version": params.version, "actions": actions}

        if params.id:
            result = await api.post(f"/product-tailoring/{params.id}", body=body)
        elif params.key:
            result = await api.post(f"/product-tailoring/key={params.key}", body=body)
        else:
            raise ValueError(
                "Either id or key must be provided to update product tailoring"
            )
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update product tailoring", e)


# ── Customer scope ────────────────────────────────────────────────────────────

async def _read_product_tailoring_customer(
    params: ReadProductTailoringParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    """Customer reads product tailoring entries (read-only, same paths as admin).

    GET /product-tailoring/{id}
    GET /product-tailoring/key={key}
    GET /in-store/key={storeKey}/products/{productId}/product-tailoring
    GET /in-store/key={storeKey}/products/key={productKey}/product-tailoring
    GET /product-tailoring  (list)
    """
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/product-tailoring/{params.id}", params=query or None)
        elif params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/product-tailoring/key={params.key}", params=query or None)
        elif params.product_id and params.store_key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(
                f"/in-store/key={params.store_key}/products/{params.product_id}/product-tailoring",
                params=query or None,
            )
        elif params.product_key and params.store_key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(
                f"/in-store/key={params.store_key}/products/key={params.product_key}/product-tailoring",
                params=query or None,
            )
        else:
            query = {"limit": params.limit or 20}
            if params.offset is not None:
                query["offset"] = params.offset
            if params.sort:
                query["sort"] = params.sort
            if params.where:
                query["where"] = params.where
            if params.expand:
                query["expand"] = params.expand
            result = await api.get("/product-tailoring", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read product tailoring", e)


# ── Public dispatchers ────────────────────────────────────────────────────────

async def read_product_tailoring(
    params: ReadProductTailoringParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.is_admin:
        return await _read_product_tailoring_admin(params, api, ctx)
    if ctx.store_key:
        return await _read_product_tailoring_store(params, api, ctx)
    if ctx.customer_id:
        return await _read_product_tailoring_customer(params, api, ctx)
    raise ContextError("read_product_tailoring", "isAdmin, storeKey, or customerId")


async def create_product_tailoring(
    params: CreateProductTailoringParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.is_admin:
        return await _create_product_tailoring_admin(params, api, ctx)
    if ctx.store_key:
        return await _create_product_tailoring_store(params, api, ctx)
    raise ContextError("create_product_tailoring", "isAdmin or storeKey")


async def update_product_tailoring(
    params: UpdateProductTailoringParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if ctx.is_admin:
        return await _update_product_tailoring_admin(params, api, ctx)
    if ctx.store_key:
        return await _update_product_tailoring_store(params, api, ctx)
    raise ContextError("update_product_tailoring", "isAdmin or storeKey")
