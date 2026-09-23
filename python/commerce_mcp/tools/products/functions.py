from __future__ import annotations

from typing import TYPE_CHECKING, Any
from ..products.schemas import ListProductsParams, CreateProductParams, UpdateProductParams
from ...shared.errors import SDKError, ContextError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def list_products(
    params: ListProductsParams,
    api: "CommercetoolsAPI",
    context: "CTContext",
) -> str:
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/products/{params.id}", params=query or None)
            return transform_tool_output(result)

        query = {"limit": params.limit or 10}
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.where:
            query["where"] = params.where
        if params.expand:
            query["expand"] = params.expand

        result = await api.get("/products", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("list products", e)


async def create_product(
    params: CreateProductParams,
    api: "CommercetoolsAPI",
    context: "CTContext",
) -> str:
    if not context.is_admin:
        raise ContextError("create_product", "isAdmin")
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/products", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create product", e)


async def update_product(
    params: UpdateProductParams,
    api: "CommercetoolsAPI",
    context: "CTContext",
) -> str:
    if not context.is_admin:
        raise ContextError("update_product", "isAdmin")
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        result = await api.post(f"/products/{params.id}", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("update product", e)
