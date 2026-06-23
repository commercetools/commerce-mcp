from __future__ import annotations

from typing import TYPE_CHECKING

from .schemas import SearchProductsParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def search_products(
    params: SearchProductsParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        body: dict = {"query": params.query}
        if params.sort is not None:
            body["sort"] = [s.model_dump(by_alias=True, exclude_none=True) for s in params.sort]
        if params.limit is not None:
            body["limit"] = params.limit
        if params.offset is not None:
            body["offset"] = params.offset
        if params.mark_matching_variants is not None:
            body["markMatchingVariants"] = params.mark_matching_variants
        if params.product_projection_parameters is not None:
            body["productProjectionParameters"] = params.product_projection_parameters
        if params.facets is not None:
            body["facets"] = params.facets
        result = await api.post("/products/search", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("search products", e)
