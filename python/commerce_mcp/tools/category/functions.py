from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import CreateCategoryParams, ReadCategoryParams, UpdateCategoryParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_category(
    params: ReadCategoryParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # read_category has NO context guard — public read (customer and anonymous contexts allowed).
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/categories/{params.id}", params=query or None)
            return transform_tool_output(result)

        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/categories/key={params.key}", params=query or None)
            return transform_tool_output(result)

        query = {"limit": params.limit if params.limit is not None else 10}
        if params.offset is not None:
            query["offset"] = params.offset
        if params.sort:
            query["sort"] = params.sort
        if params.where:
            query["where"] = params.where
        if params.expand:
            query["expand"] = params.expand
        result = await api.get("/categories", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read category", e)


async def create_category(
    params: CreateCategoryParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_category", "isAdmin")
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/categories", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("create category", e)


async def update_category(
    params: UpdateCategoryParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_category", "isAdmin")
    try:
        body = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/categories/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/categories/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError(
            "update category",
            Exception("Either id or key must be provided"),
        )
    except ContextError:
        raise
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update category", e)
