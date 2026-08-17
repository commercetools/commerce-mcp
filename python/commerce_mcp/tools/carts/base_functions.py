from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI


def serialize_actions(actions: list) -> list[dict]:
    return [a.model_dump(by_alias=True, exclude_none=True) for a in actions]


async def get_cart_by_id(
    api: "CommercetoolsAPI",
    cart_id: str,
    expand: list[str] | None = None,
) -> dict:
    query: dict[str, Any] = {}
    if expand:
        query["expand"] = expand
    return await api.get(f"/carts/{cart_id}", params=query or None)


async def get_cart_by_key(
    api: "CommercetoolsAPI",
    cart_key: str,
    expand: list[str] | None = None,
) -> dict:
    query: dict[str, Any] = {}
    if expand:
        query["expand"] = expand
    return await api.get(f"/carts/key={cart_key}", params=query or None)


async def query_carts(
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
    path = f"/in-store/key={store_key}/carts" if store_key else "/carts"
    return await api.get(path, params=query)


async def verify_cart_belongs_to_customer(
    api: "CommercetoolsAPI",
    customer_id: str,
    cart_id: str | None = None,
    cart_key: str | None = None,
) -> bool:
    if cart_id:
        cart = await api.get(f"/carts/{cart_id}")
    elif cart_key:
        cart = await api.get(f"/carts/key={cart_key}")
    else:
        raise Exception("Either cart_id or cart_key must be provided")
    return cart.get("customerId") == customer_id


async def verify_cart_belongs_to_store(
    api: "CommercetoolsAPI",
    store_key: str,
    cart_id: str | None = None,
    cart_key: str | None = None,
) -> bool:
    if cart_id:
        cart = await api.get(f"/carts/{cart_id}")
    elif cart_key:
        cart = await api.get(f"/carts/key={cart_key}")
    else:
        raise Exception("Either cart_id or cart_key must be provided")
    return (cart.get("store") or {}).get("key") == store_key
