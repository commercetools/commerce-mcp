from __future__ import annotations

from typing import TYPE_CHECKING
from .schemas import ReadOrderParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output
from .base_functions import query_orders

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def read_order(
    params: ReadOrderParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        customer_filter = f'customerId="{ctx.customer_id}"'

        if params.id:
            result = await query_orders(
                api,
                where=[f'id="{params.id}"', customer_filter],
                limit=1,
                expand=params.expand,
                store_key=params.store_key,
            )
            results = result.get("results", [])
            if not results:
                raise Exception(
                    f"Order with ID {params.id} not found for customer {ctx.customer_id}"
                )
            return transform_tool_output(results[0])

        if params.order_number:
            result = await query_orders(
                api,
                where=[f'orderNumber="{params.order_number}"', customer_filter],
                limit=1,
                expand=params.expand,
                store_key=params.store_key,
            )
            results = result.get("results", [])
            if not results:
                raise Exception(
                    f"Order with number {params.order_number} not found for customer {ctx.customer_id}"
                )
            return transform_tool_output(results[0])

        result = await query_orders(
            api,
            where=[*(params.where or []), customer_filter],
            limit=params.limit,
            offset=params.offset,
            sort=params.sort,
            expand=params.expand,
            store_key=params.store_key,
        )
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("read customer order", e)
