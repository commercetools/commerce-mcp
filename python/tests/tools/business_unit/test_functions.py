"""Tests for business_unit context-conditional dispatch."""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.business_unit.functions import (
    read_business_unit,
    create_business_unit,
    update_business_unit,
    _read_business_unit_admin,
    _read_business_unit_store,
    _create_business_unit_admin,
    _create_business_unit_store,
    _update_business_unit_admin,
    _update_business_unit_store,
)
from commerce_mcp.tools.business_unit.schemas import (
    ReadBusinessUnitParams,
    CreateBusinessUnitParams,
    UpdateBusinessUnitParams,
    BusinessUnitUpdateAction,
)
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def store_ctx():
    return CTContext(store_key="my-store")


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "x-1", "version": 5})
    api.post = AsyncMock(return_value={"id": "x-1", "version": 1})
    return api


def make_create_params(**kwargs) -> CreateBusinessUnitParams:
    return CreateBusinessUnitParams(
        key="my-bu",
        name="My Business Unit",
        unitType="Company",
        **kwargs,
    )


def make_update_params(**kwargs) -> UpdateBusinessUnitParams:
    return UpdateBusinessUnitParams(
        id="bu-1",
        version=3,
        actions=[BusinessUnitUpdateAction(action="changeName")],
        **kwargs,
    )


# ── Dispatch: read_business_unit ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await read_business_unit(ReadBusinessUnitParams(), mock_api, store_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=my-store/business-units" in path


@pytest.mark.asyncio
async def test_read_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await read_business_unit(ReadBusinessUnitParams(), mock_api, admin_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert path == "/business-units"


@pytest.mark.asyncio
async def test_read_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="read_business_unit"):
        await read_business_unit(ReadBusinessUnitParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


# ── Dispatch: create_business_unit ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await create_business_unit(make_create_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=my-store/business-units"


@pytest.mark.asyncio
async def test_create_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await create_business_unit(make_create_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/business-units"


@pytest.mark.asyncio
async def test_create_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_business_unit"):
        await create_business_unit(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Dispatch: update_business_unit ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await update_business_unit(make_update_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/in-store/key=my-store/business-units/" in path


@pytest.mark.asyncio
async def test_update_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await update_business_unit(make_update_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/business-units/bu-1"


@pytest.mark.asyncio
async def test_update_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="update_business_unit"):
        await update_business_unit(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Admin read implementation ─────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_admin_list_uses_business_units_endpoint(mock_api, admin_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_business_unit_admin(ReadBusinessUnitParams(), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/business-units"


@pytest.mark.asyncio
async def test_read_admin_by_id_uses_direct_path(mock_api, admin_ctx):
    await _read_business_unit_admin(ReadBusinessUnitParams(id="bu-99"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/business-units/bu-99"


@pytest.mark.asyncio
async def test_read_admin_by_key_uses_key_path(mock_api, admin_ctx):
    await _read_business_unit_admin(ReadBusinessUnitParams(key="my-bu"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/business-units/key=my-bu"


@pytest.mark.asyncio
async def test_read_admin_passes_query_params(mock_api, admin_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_business_unit_admin(
        ReadBusinessUnitParams(limit=10, offset=5, sort=["createdAt desc"]),
        mock_api,
        admin_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 10
    assert params["offset"] == 5
    assert params["sort"] == ["createdAt desc"]


@pytest.mark.asyncio
async def test_read_admin_with_where_filter(mock_api, admin_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_business_unit_admin(
        ReadBusinessUnitParams(where=["status=\"Active\""]),
        mock_api,
        admin_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["where"] == ["status=\"Active\""]


@pytest.mark.asyncio
async def test_read_admin_with_expand(mock_api, admin_ctx):
    await _read_business_unit_admin(
        ReadBusinessUnitParams(id="bu-1", expand=["associates[*].customer"]),
        mock_api,
        admin_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["expand"] == ["associates[*].customer"]


# ── Store read implementation ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_store_list_uses_in_store_path(mock_api, store_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_business_unit_store(ReadBusinessUnitParams(), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/business-units"


@pytest.mark.asyncio
async def test_read_store_by_id_uses_in_store_path(mock_api, store_ctx):
    await _read_business_unit_store(ReadBusinessUnitParams(id="bu-2"), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/business-units/bu-2"


@pytest.mark.asyncio
async def test_read_store_by_key_uses_in_store_key_path(mock_api, store_ctx):
    await _read_business_unit_store(ReadBusinessUnitParams(key="bu-key"), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/business-units/key=bu-key"


@pytest.mark.asyncio
async def test_read_store_passes_query_params(mock_api, store_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_business_unit_store(
        ReadBusinessUnitParams(limit=20, sort=["name asc"]),
        mock_api,
        store_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 20
    assert params["sort"] == ["name asc"]


# ── Admin create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_admin_posts_to_business_units(mock_api, admin_ctx):
    await _create_business_unit_admin(make_create_params(), mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/business-units"
    body = mock_api.post.call_args[1]["body"]
    assert body["key"] == "my-bu"
    assert body["name"] == "My Business Unit"
    assert body["unitType"] == "Company"


@pytest.mark.asyncio
async def test_create_admin_does_not_auto_set_stores(mock_api, admin_ctx):
    """Admin create should NOT inject stores/storeMode automatically."""
    await _create_business_unit_admin(make_create_params(), mock_api, admin_ctx)
    body = mock_api.post.call_args[1]["body"]
    # stores and storeMode should only be present if explicitly provided
    assert "stores" not in body
    assert "storeMode" not in body


# ── Store create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_store_posts_to_in_store_path(mock_api, store_ctx):
    await _create_business_unit_store(make_create_params(), mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/business-units"


@pytest.mark.asyncio
async def test_create_store_auto_sets_stores_when_missing(mock_api, store_ctx):
    """Store context should auto-inject stores=[{key: store_key}] when not provided."""
    await _create_business_unit_store(make_create_params(), mock_api, store_ctx)
    body = mock_api.post.call_args[1]["body"]
    assert "stores" in body
    assert body["stores"] == [{"key": "my-store", "typeId": "store"}]


@pytest.mark.asyncio
async def test_create_store_auto_sets_store_mode_when_missing(mock_api, store_ctx):
    """Store context should auto-inject storeMode=Explicit when not provided."""
    await _create_business_unit_store(make_create_params(), mock_api, store_ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["storeMode"] == "Explicit"


@pytest.mark.asyncio
async def test_create_store_does_not_override_explicit_stores(mock_api, store_ctx):
    """If stores is explicitly provided, it should not be overwritten."""
    from commerce_mcp.tools.business_unit.schemas import StoreKeyReference
    params = make_create_params(stores=[StoreKeyReference(key="other-store")])
    await _create_business_unit_store(params, mock_api, store_ctx)
    body = mock_api.post.call_args[1]["body"]
    # The explicitly provided stores should be kept
    assert body["stores"][0]["key"] == "other-store"


@pytest.mark.asyncio
async def test_create_store_does_not_override_explicit_store_mode(mock_api, store_ctx):
    """If storeMode is explicitly provided, it should not be overwritten."""
    params = make_create_params(store_mode="FromParent")
    await _create_business_unit_store(params, mock_api, store_ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["storeMode"] == "FromParent"


# ── Admin update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_admin_by_id_posts_to_direct_path(mock_api, admin_ctx):
    await _update_business_unit_admin(make_update_params(), mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/business-units/bu-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 3
    assert body["actions"][0]["action"] == "changeName"


@pytest.mark.asyncio
async def test_update_admin_by_key_posts_to_key_path(mock_api, admin_ctx):
    params = UpdateBusinessUnitParams(
        key="bu-key", version=2, actions=[BusinessUnitUpdateAction(action="setContactEmail")]
    )
    await _update_business_unit_admin(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/business-units/key=bu-key"


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_when_no_id_or_key(mock_api, admin_ctx):
    params = UpdateBusinessUnitParams(
        version=1, actions=[BusinessUnitUpdateAction(action="changeName")]
    )
    with pytest.raises(SDKError, match="update business unit"):
        await _update_business_unit_admin(params, mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_update_admin_auto_fetches_version_when_none(mock_api, admin_ctx):
    """When version is None, it should be fetched from the API."""
    mock_api.get.return_value = {"id": "bu-1", "version": 7}
    params = UpdateBusinessUnitParams(
        id="bu-1",
        version=None,
        actions=[BusinessUnitUpdateAction(action="changeName")],
    )
    await _update_business_unit_admin(params, mock_api, admin_ctx)
    # GET should have been called to fetch version
    mock_api.get.assert_called_once_with("/business-units/bu-1", params=None)
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 7


# ── Store update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_store_by_id_posts_to_in_store_path(mock_api, store_ctx):
    await _update_business_unit_store(make_update_params(), mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/business-units/bu-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 3


@pytest.mark.asyncio
async def test_update_store_by_key_posts_to_in_store_key_path(mock_api, store_ctx):
    params = UpdateBusinessUnitParams(
        key="bu-key", version=2, actions=[BusinessUnitUpdateAction(action="changeName")]
    )
    await _update_business_unit_store(params, mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/business-units/key=bu-key"


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_when_no_id_or_key(mock_api, store_ctx):
    params = UpdateBusinessUnitParams(
        version=1, actions=[BusinessUnitUpdateAction(action="changeName")]
    )
    with pytest.raises(SDKError, match="update business unit"):
        await _update_business_unit_store(params, mock_api, store_ctx)


@pytest.mark.asyncio
async def test_update_store_auto_fetches_version_when_none(mock_api, store_ctx):
    """When version is None, it should be fetched using the in-store path."""
    mock_api.get.return_value = {"id": "bu-1", "version": 9}
    params = UpdateBusinessUnitParams(
        id="bu-1",
        version=None,
        actions=[BusinessUnitUpdateAction(action="changeName")],
    )
    await _update_business_unit_store(params, mock_api, store_ctx)
    # GET should have been called with the in-store path
    mock_api.get.assert_called_once_with(
        "/in-store/key=my-store/business-units/bu-1", params=None
    )
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 9


# ── SDK error wrapping ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read business unit"):
        await _read_business_unit_admin(ReadBusinessUnitParams(id="bu-1"), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_read_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read business unit"):
        await _read_business_unit_store(ReadBusinessUnitParams(id="bu-1"), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_create_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create business unit"):
        await _create_business_unit_admin(make_create_params(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_create_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create business unit"):
        await _create_business_unit_store(make_create_params(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update business unit"):
        await _update_business_unit_admin(make_update_params(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update business unit"):
        await _update_business_unit_store(make_update_params(), mock_api, store_ctx)


# ── store_key takes priority over is_admin ────────────────────────────────────

@pytest.mark.asyncio
async def test_read_uses_store_path_when_both_store_key_and_admin(mock_api):
    ctx = CTContext(is_admin=True, store_key="priority-store")
    await read_business_unit(ReadBusinessUnitParams(), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=priority-store/business-units" in path


@pytest.mark.asyncio
async def test_create_uses_store_path_when_both_store_key_and_admin(mock_api):
    ctx = CTContext(is_admin=True, store_key="priority-store")
    await create_business_unit(make_create_params(), mock_api, ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=priority-store/business-units"
