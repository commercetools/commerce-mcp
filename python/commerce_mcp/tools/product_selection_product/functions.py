from __future__ import annotations

from typing import TYPE_CHECKING, Any
from .schemas import ReadProductSelectionProductParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def _query_products(
    params: ReadProductSelectionProductParams,
    api: "CommercetoolsAPI",
) -> Any:
    if not params.product_selection_id and not params.product_selection_key:
        raise ValueError("Either productSelectionId or productSelectionKey must be provided")
    query: dict[str, Any] = {"limit": params.limit or 10}
    if params.where:
        query["where"] = params.where
    if params.offset is not None:
        query["offset"] = params.offset
    if params.sort:
        query["sort"] = params.sort
    if params.expand:
        query["expand"] = params.expand
    if params.product_selection_id:
        return await api.get(
            f"/product-selections/{params.product_selection_id}/products", params=query
        )
    return await api.get(
        f"/product-selections/key={params.product_selection_key}/products", params=query
    )


async def read_product_selection_product(
    params: ReadProductSelectionProductParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Mirrors contextToProductSelectionProductFunctionMapping — storeKey first, then admin.
    if ctx.store_key or ctx.is_admin:
        try:
            result = await _query_products(params, api)
            return transform_tool_output(result)
        except (ContextError, ValueError):
            raise
        except Exception as e:
            raise SDKError("read product selection product", e)
    raise ContextError("read_product_selection_product", "isAdmin or storeKey")
