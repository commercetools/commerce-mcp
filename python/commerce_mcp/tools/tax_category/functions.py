from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .schemas import ReadTaxCategoryParams, CreateTaxCategoryParams, UpdateTaxCategoryParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_tax_category(
    params: ReadTaxCategoryParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("read_tax_category", "isAdmin")
    try:
        if params.id:
            query: dict[str, Any] = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/tax-categories/{params.id}", params=query or None)
            return transform_tool_output(result)
        if params.key:
            query = {}
            if params.expand:
                query["expand"] = params.expand
            result = await api.get(f"/tax-categories/key={params.key}", params=query or None)
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
        result = await api.get("/tax-categories", params=query or None)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("read tax category", e)


async def create_tax_category(
    params: CreateTaxCategoryParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("create_tax_category", "isAdmin")
    try:
        # Transform rates to ensure includedInPrice is always defined
        raw = params.model_dump(by_alias=True, exclude_none=True)
        rates = raw.get("rates", [])
        for rate in rates:
            if "includedInPrice" not in rate:
                rate["includedInPrice"] = False
        body: dict[str, Any] = {"name": params.name, "rates": rates}
        if params.key is not None:
            body["key"] = params.key
        if params.description is not None:
            body["description"] = params.description
        if params.custom is not None:
            body["custom"] = raw.get("custom")
        result = await api.post("/tax-categories", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("create tax category", e)


async def update_tax_category(
    params: UpdateTaxCategoryParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_tax_category", "isAdmin")
    try:
        body: dict[str, Any] = {
            "version": params.version,
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        if params.id:
            result = await api.post(f"/tax-categories/{params.id}", body=body)
            return transform_tool_output(result)
        if params.key:
            result = await api.post(f"/tax-categories/key={params.key}", body=body)
            return transform_tool_output(result)
        raise SDKError(
            "update tax category", Exception("Either id or key must be provided")
        )
    except ContextError:
        raise
    except SDKError:
        raise
    except Exception as e:
        raise SDKError("update tax category", e)
