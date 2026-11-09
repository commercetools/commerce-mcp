from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI


def serialize_actions(actions: list) -> list[dict]:
    return [a.model_dump(by_alias=True, exclude_none=True) for a in actions]


async def get_order_by_id(
    api: "CommercetoolsAPI",
    order_id: str,
    expand: list[str] | None = None,
    store_key: str | None = None,
) -> dict:
    query: dict[str, Any] = {}
    if expand:
        query["expand"] = expand
    prefix = f"/in-store/key={store_key}" if store_key else ""
    return await api.get(f"{prefix}/orders/{order_id}", params=query or None)


async def get_order_by_order_number(
    api: "CommercetoolsAPI",
    order_number: str,
    expand: list[str] | None = None,
    store_key: str | None = None,
) -> dict:
    query: dict[str, Any] = {}
    if expand:
        query["expand"] = expand
    prefix = f"/in-store/key={store_key}" if store_key else ""
    return await api.get(
        f"{prefix}/orders/order-number={order_number}", params=query or None
    )


async def query_orders(
    api: "CommercetoolsAPI",
    where: list[str] | None = None,
    limit: int | None = None,
    offset: int | None = None,
    sort: list[str] | None = None,
    expand: list[str] | None = None,
    store_key: str | None = None,
) -> dict:
    query: dict[str, Any] = {"limit": limit or 10}
    if where:
        query["where"] = where
    if offset is not None:
        query["offset"] = offset
    if sort:
        query["sort"] = sort
    if expand:
        query["expand"] = expand
    prefix = f"/in-store/key={store_key}" if store_key else ""
    return await api.get(f"{prefix}/orders", params=query)
