"""Tests for quote_request context-conditional dispatch."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.quote_request.functions import (
    read_quote_request,
    create_quote_request,
    update_quote_request,
    _read_quote_request_associate,
    _read_quote_request_customer,
    _read_quote_request_store,
    _read_quote_request_admin,
    _create_quote_request_associate,
    _create_quote_request_store,
    _create_quote_request_admin,
    _update_quote_request_associate,
    _update_quote_request_customer,
    _update_quote_request_store,
    _update_quote_request_admin,
)
from commerce_mcp.tools.quote_request.schemas import (
    ReadQuoteRequestParams,
    CreateQuoteRequestParams,
    UpdateQuoteRequestParams,
    QuoteRequestUpdateAction,
    CartReference,
)
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def customer_ctx():
    return CTContext(customer_id="cust-1")


@pytest.fixture
def store_ctx():
    return CTContext(store_key="my-store")


@pytest.fixture
def bu_ctx():
    return CTContext(customer_id="cust-1", business_unit_key="bu-key")


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "qr-1"}]})
    api.post = AsyncMock(return_value={"id": "qr-1", "version": 2})
    return api


def make_create_params(**kwargs) -> CreateQuoteRequestParams:
    return CreateQuoteRequestParams(
        cart=CartReference(id="cart-1"),
        cartVersion=1,
        **kwargs,
    )


def make_update_params(**kwargs) -> UpdateQuoteRequestParams:
    return UpdateQuoteRequestParams(
        id="qr-1",
        version=1,
        actions=[QuoteRequestUpdateAction(action="cancelQuoteRequest")],
        **kwargs,
    )


# ── Context dispatch: read_quote_request ──────────────────────────────────────

@pytest.mark.asyncio
async def test_read_dispatches_to_associate_when_customer_and_bu(mock_api, bu_ctx):
    await read_quote_request(ReadQuoteRequestParams(), mock_api, bu_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert "in-business-unit/key=bu-key" in path
    assert path.endswith("/quote-requests")


@pytest.mark.asyncio
async def test_read_dispatches_to_customer_when_customer_only(mock_api, customer_ctx):
    await read_quote_request(ReadQuoteRequestParams(), mock_api, customer_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "/me/quote-requests" in path


@pytest.mark.asyncio
async def test_read_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await read_quote_request(ReadQuoteRequestParams(), mock_api, store_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=my-store/quote-requests" in path


@pytest.mark.asyncio
async def test_read_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await read_quote_request(ReadQuoteRequestParams(), mock_api, admin_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "/quote-requests" in path


@pytest.mark.asyncio
async def test_read_associate_takes_priority_over_customer_only(mock_api, bu_ctx):
    # bu_ctx has both customer_id and business_unit_key -> associate path
    await read_quote_request(ReadQuoteRequestParams(), mock_api, bu_ctx)
    path = mock_api.get.call_args[0][0]
    assert "as-associate" in path


@pytest.mark.asyncio
async def test_read_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="read_quote_request"):
        await read_quote_request(ReadQuoteRequestParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


# ── Context dispatch: create_quote_request ────────────────────────────────────

@pytest.mark.asyncio
async def test_create_dispatches_to_associate_when_customer_and_bu(mock_api, bu_ctx):
    await create_quote_request(make_create_params(), mock_api, bu_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert "in-business-unit/key=bu-key" in path


@pytest.mark.asyncio
async def test_create_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await create_quote_request(make_create_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=my-store/quote-requests"


@pytest.mark.asyncio
async def test_create_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await create_quote_request(make_create_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/quote-requests"


@pytest.mark.asyncio
async def test_create_raises_context_error_for_customer_only(mock_api, customer_ctx):
    # Customer-only cannot create quote requests (no business unit)
    with pytest.raises(ContextError, match="create_quote_request"):
        await create_quote_request(make_create_params(), mock_api, customer_ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_create_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_quote_request"):
        await create_quote_request(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Context dispatch: update_quote_request ────────────────────────────────────

@pytest.mark.asyncio
async def test_update_dispatches_to_associate_when_customer_and_bu(mock_api, bu_ctx):
    await update_quote_request(make_update_params(), mock_api, bu_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert "in-business-unit/key=bu-key" in path


@pytest.mark.asyncio
async def test_update_dispatches_to_customer_when_customer_only(mock_api, customer_ctx):
    await update_quote_request(make_update_params(), mock_api, customer_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/me/quote-requests/" in path


@pytest.mark.asyncio
async def test_update_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await update_quote_request(make_update_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/in-store/key=my-store/quote-requests/" in path


@pytest.mark.asyncio
async def test_update_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await update_quote_request(make_update_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/quote-requests/qr-1" in path


@pytest.mark.asyncio
async def test_update_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="update_quote_request"):
        await update_quote_request(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Associate read implementation ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_associate_list_uses_as_associate_path(mock_api, bu_ctx):
    await _read_quote_request_associate(ReadQuoteRequestParams(), mock_api, bu_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/as-associate/cust-1/in-business-unit/key=bu-key/quote-requests"


@pytest.mark.asyncio
async def test_read_associate_by_id_uses_direct_path(mock_api, bu_ctx):
    mock_api.get.return_value = {"id": "qr-1"}
    await _read_quote_request_associate(ReadQuoteRequestParams(id="qr-1"), mock_api, bu_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/as-associate/cust-1/in-business-unit/key=bu-key/quote-requests/qr-1"


@pytest.mark.asyncio
async def test_read_associate_by_key_uses_key_path(mock_api, bu_ctx):
    mock_api.get.return_value = {"id": "qr-1"}
    await _read_quote_request_associate(ReadQuoteRequestParams(key="qr-key"), mock_api, bu_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/as-associate/cust-1/in-business-unit/key=bu-key/quote-requests/key=qr-key"


@pytest.mark.asyncio
async def test_read_associate_passes_query_params(mock_api, bu_ctx):
    await _read_quote_request_associate(
        ReadQuoteRequestParams(limit=10, offset=5, sort=["createdAt desc"]),
        mock_api,
        bu_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 10
    assert params["offset"] == 5
    assert params["sort"] == ["createdAt desc"]


# ── Customer read implementation ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_customer_list_uses_me_endpoint(mock_api, customer_ctx):
    await _read_quote_request_customer(ReadQuoteRequestParams(), mock_api, customer_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/me/quote-requests"


@pytest.mark.asyncio
async def test_read_customer_injects_customer_where_filter(mock_api, customer_ctx):
    await _read_quote_request_customer(ReadQuoteRequestParams(), mock_api, customer_ctx)
    params = mock_api.get.call_args[1]["params"]
    where = params.get("where", [])
    assert any("cust-1" in c for c in where)


@pytest.mark.asyncio
async def test_read_customer_by_id_uses_me_id_path(mock_api, customer_ctx):
    mock_api.get.return_value = {"id": "qr-1"}
    await _read_quote_request_customer(ReadQuoteRequestParams(id="qr-1"), mock_api, customer_ctx)
    assert mock_api.get.call_args[0][0] == "/me/quote-requests/qr-1"


@pytest.mark.asyncio
async def test_read_customer_by_key_uses_me_key_path(mock_api, customer_ctx):
    mock_api.get.return_value = {"id": "qr-1"}
    await _read_quote_request_customer(ReadQuoteRequestParams(key="qr-key"), mock_api, customer_ctx)
    assert mock_api.get.call_args[0][0] == "/me/quote-requests/key=qr-key"


@pytest.mark.asyncio
async def test_read_customer_merges_extra_where(mock_api, customer_ctx):
    await _read_quote_request_customer(
        ReadQuoteRequestParams(where=['quoteRequestState="Submitted"']),
        mock_api,
        customer_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    where = params["where"]
    assert any("cust-1" in c for c in where)
    assert any("Submitted" in c for c in where)


# ── Store read implementation ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_store_list_uses_in_store_path(mock_api, store_ctx):
    await _read_quote_request_store(ReadQuoteRequestParams(), mock_api, store_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/in-store/key=my-store/quote-requests"


@pytest.mark.asyncio
async def test_read_store_by_id_uses_in_store_id_path(mock_api, store_ctx):
    mock_api.get.return_value = {"id": "qr-1"}
    await _read_quote_request_store(ReadQuoteRequestParams(id="qr-1"), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/quote-requests/qr-1"


@pytest.mark.asyncio
async def test_read_store_by_key_uses_in_store_key_path(mock_api, store_ctx):
    mock_api.get.return_value = {"id": "qr-1"}
    await _read_quote_request_store(ReadQuoteRequestParams(key="qr-key"), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/quote-requests/key=qr-key"


@pytest.mark.asyncio
async def test_read_store_with_customer_id_param_applies_where_filter(mock_api, store_ctx):
    await _read_quote_request_store(
        ReadQuoteRequestParams(customer_id="cust-99"),
        mock_api,
        store_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    where = params.get("where", [])
    assert any("cust-99" in c for c in where)


# ── Admin read implementation ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_admin_list_uses_quote_requests_endpoint(mock_api, admin_ctx):
    await _read_quote_request_admin(ReadQuoteRequestParams(), mock_api, admin_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/quote-requests"


@pytest.mark.asyncio
async def test_read_admin_by_id_uses_direct_path(mock_api, admin_ctx):
    mock_api.get.return_value = {"id": "qr-99"}
    await _read_quote_request_admin(ReadQuoteRequestParams(id="qr-99"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/quote-requests/qr-99"


@pytest.mark.asyncio
async def test_read_admin_by_key_uses_key_path(mock_api, admin_ctx):
    mock_api.get.return_value = {"id": "qr-99"}
    await _read_quote_request_admin(ReadQuoteRequestParams(key="my-key"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/quote-requests/key=my-key"


@pytest.mark.asyncio
async def test_read_admin_with_store_key_param_uses_in_store_prefix(mock_api, admin_ctx):
    await _read_quote_request_admin(
        ReadQuoteRequestParams(store_key="eu-store"),
        mock_api,
        admin_ctx,
    )
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=eu-store/quote-requests" in path


@pytest.mark.asyncio
async def test_read_admin_with_customer_id_applies_where_filter(mock_api, admin_ctx):
    await _read_quote_request_admin(
        ReadQuoteRequestParams(customer_id="cust-42"),
        mock_api,
        admin_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    where = params.get("where", [])
    assert any("cust-42" in c for c in where)


# ── Associate create implementation ───────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_associate_posts_to_as_associate_path(mock_api, bu_ctx):
    await _create_quote_request_associate(make_create_params(), mock_api, bu_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/as-associate/cust-1/in-business-unit/key=bu-key/quote-requests"
    body = mock_api.post.call_args[1]["body"]
    assert body["cart"]["id"] == "cart-1"
    assert body["cartVersion"] == 1


@pytest.mark.asyncio
async def test_create_associate_includes_comment_when_provided(mock_api, bu_ctx):
    await _create_quote_request_associate(
        make_create_params(comment="Please expedite"),
        mock_api,
        bu_ctx,
    )
    body = mock_api.post.call_args[1]["body"]
    assert body["comment"] == "Please expedite"


@pytest.mark.asyncio
async def test_create_associate_includes_key_when_provided(mock_api, bu_ctx):
    await _create_quote_request_associate(
        make_create_params(key="qr-custom-key"),
        mock_api,
        bu_ctx,
    )
    body = mock_api.post.call_args[1]["body"]
    assert body["key"] == "qr-custom-key"


# ── Store create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_store_posts_to_in_store_path(mock_api, store_ctx):
    await _create_quote_request_store(make_create_params(), mock_api, store_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=my-store/quote-requests"
    body = mock_api.post.call_args[1]["body"]
    assert body["cart"]["id"] == "cart-1"
    assert body["cartVersion"] == 1


# ── Admin create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_admin_posts_to_quote_requests(mock_api, admin_ctx):
    await _create_quote_request_admin(make_create_params(), mock_api, admin_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/quote-requests"
    body = mock_api.post.call_args[1]["body"]
    assert body["cart"]["id"] == "cart-1"


@pytest.mark.asyncio
async def test_create_admin_with_store_key_param_uses_in_store_path(mock_api, admin_ctx):
    await _create_quote_request_admin(
        make_create_params(store_key="eu-store"),
        mock_api,
        admin_ctx,
    )
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=eu-store/quote-requests"


# ── Associate update implementation ───────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_associate_by_id_posts_to_as_associate_path(mock_api, bu_ctx):
    await _update_quote_request_associate(make_update_params(), mock_api, bu_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/as-associate/cust-1/in-business-unit/key=bu-key/quote-requests/qr-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1
    assert body["actions"][0]["action"] == "cancelQuoteRequest"


@pytest.mark.asyncio
async def test_update_associate_by_key_uses_key_path(mock_api, bu_ctx):
    params = UpdateQuoteRequestParams(
        key="qr-key",
        version=2,
        actions=[QuoteRequestUpdateAction(action="cancelQuoteRequest")],
    )
    await _update_quote_request_associate(params, mock_api, bu_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/as-associate/cust-1/in-business-unit/key=bu-key/quote-requests/key=qr-key"


@pytest.mark.asyncio
async def test_update_associate_raises_sdk_error_when_no_id_or_key(mock_api, bu_ctx):
    params = UpdateQuoteRequestParams(
        version=1,
        actions=[QuoteRequestUpdateAction(action="cancelQuoteRequest")],
    )
    with pytest.raises(SDKError, match="update quote request"):
        await _update_quote_request_associate(params, mock_api, bu_ctx)


# ── Customer update implementation ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_customer_by_id_posts_to_me_path(mock_api, customer_ctx):
    await _update_quote_request_customer(make_update_params(), mock_api, customer_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/me/quote-requests/qr-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1


@pytest.mark.asyncio
async def test_update_customer_by_key_uses_me_key_path(mock_api, customer_ctx):
    params = UpdateQuoteRequestParams(
        key="qr-key",
        version=2,
        actions=[QuoteRequestUpdateAction(action="cancelQuoteRequest")],
    )
    await _update_quote_request_customer(params, mock_api, customer_ctx)
    assert mock_api.post.call_args[0][0] == "/me/quote-requests/key=qr-key"


@pytest.mark.asyncio
async def test_update_customer_raises_sdk_error_when_no_id_or_key(mock_api, customer_ctx):
    params = UpdateQuoteRequestParams(
        version=1,
        actions=[QuoteRequestUpdateAction(action="cancelQuoteRequest")],
    )
    with pytest.raises(SDKError, match="update quote request"):
        await _update_quote_request_customer(params, mock_api, customer_ctx)


# ── Store update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_store_by_id_posts_to_in_store_path(mock_api, store_ctx):
    await _update_quote_request_store(make_update_params(), mock_api, store_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=my-store/quote-requests/qr-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1


@pytest.mark.asyncio
async def test_update_store_by_key_uses_key_path(mock_api, store_ctx):
    params = UpdateQuoteRequestParams(
        key="qr-key",
        version=2,
        actions=[QuoteRequestUpdateAction(action="cancelQuoteRequest")],
    )
    await _update_quote_request_store(params, mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/quote-requests/key=qr-key"


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_when_no_id_or_key(mock_api, store_ctx):
    params = UpdateQuoteRequestParams(
        version=1,
        actions=[QuoteRequestUpdateAction(action="cancelQuoteRequest")],
    )
    with pytest.raises(SDKError, match="update quote request"):
        await _update_quote_request_store(params, mock_api, store_ctx)


# ── Admin update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_admin_by_id_posts_to_direct_path(mock_api, admin_ctx):
    await _update_quote_request_admin(make_update_params(), mock_api, admin_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/quote-requests/qr-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1
    assert body["actions"][0]["action"] == "cancelQuoteRequest"


@pytest.mark.asyncio
async def test_update_admin_by_key_uses_key_path(mock_api, admin_ctx):
    params = UpdateQuoteRequestParams(
        key="qr-key",
        version=3,
        actions=[QuoteRequestUpdateAction(action="cancelQuoteRequest")],
    )
    await _update_quote_request_admin(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/quote-requests/key=qr-key"


@pytest.mark.asyncio
async def test_update_admin_with_store_key_param_uses_prefix(mock_api, admin_ctx):
    await _update_quote_request_admin(
        make_update_params(store_key="eu-store"),
        mock_api,
        admin_ctx,
    )
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/quote-requests/qr-1"


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_when_no_id_or_key(mock_api, admin_ctx):
    params = UpdateQuoteRequestParams(
        version=1,
        actions=[QuoteRequestUpdateAction(action="cancelQuoteRequest")],
    )
    with pytest.raises(SDKError, match="update quote request"):
        await _update_quote_request_admin(params, mock_api, admin_ctx)


# ── SDK error wrapping ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_associate_raises_sdk_error_on_api_failure(mock_api, bu_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read quote request"):
        await _read_quote_request_associate(ReadQuoteRequestParams(), mock_api, bu_ctx)


@pytest.mark.asyncio
async def test_read_customer_raises_sdk_error_on_api_failure(mock_api, customer_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read quote request"):
        await _read_quote_request_customer(ReadQuoteRequestParams(), mock_api, customer_ctx)


@pytest.mark.asyncio
async def test_read_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read quote request"):
        await _read_quote_request_store(ReadQuoteRequestParams(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_read_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read quote request"):
        await _read_quote_request_admin(ReadQuoteRequestParams(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_create_associate_raises_sdk_error_on_api_failure(mock_api, bu_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create quote request"):
        await _create_quote_request_associate(make_create_params(), mock_api, bu_ctx)


@pytest.mark.asyncio
async def test_create_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create quote request"):
        await _create_quote_request_store(make_create_params(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_create_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create quote request"):
        await _create_quote_request_admin(make_create_params(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_update_associate_raises_sdk_error_on_api_failure(mock_api, bu_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update quote request"):
        await _update_quote_request_associate(make_update_params(), mock_api, bu_ctx)


@pytest.mark.asyncio
async def test_update_customer_raises_sdk_error_on_api_failure(mock_api, customer_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update quote request"):
        await _update_quote_request_customer(make_update_params(), mock_api, customer_ctx)


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update quote request"):
        await _update_quote_request_store(make_update_params(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update quote request"):
        await _update_quote_request_admin(make_update_params(), mock_api, admin_ctx)


# ── Security: no admin fallthrough ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_does_not_fallthrough_to_admin(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError):
        await read_quote_request(ReadQuoteRequestParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


@pytest.mark.asyncio
async def test_create_does_not_fallthrough_to_admin(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError):
        await create_quote_request(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_does_not_fallthrough_to_admin(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError):
        await update_quote_request(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()
