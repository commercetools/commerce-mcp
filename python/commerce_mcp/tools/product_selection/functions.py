from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import CreateProductSelectionParams, ReadProductSelectionParams, UpdateProductSelectionParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_product_selection(
    params: ReadProductSelectionParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("read_product_selection", "isAdmin")
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/product-selections/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/product-selections/key={params.key}", params=query or None)
            return transform_tool_output(result)
        query = {}
        if params.limit is not None:
            query["limit"] = params.limit
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.where:
            query["where"] = params.where
        if params.expand:
            query["expand"] = params.expand
        result = await api.get("/product-selections", params=query or None)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("read product selection", e)


async def create_product_selection(
    params: CreateProductSelectionParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_product_selection", "isAdmin")
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/product-selections", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("create product selection", e)


async def update_product_selection(
    params: UpdateProductSelectionParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_product_selection", "isAdmin")
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/product-selections/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/product-selections/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError("update product selection", Exception("Either id or key must be provided"))
    except ContextError:
        raise
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update product selection", e)
