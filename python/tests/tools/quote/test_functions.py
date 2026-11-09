"""Tests for quote context-conditional dispatch."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.quote.functions import (
    read_quote,
    create_quote,
    update_quote,
    _read_quote_associate,
    _read_quote_customer,
    _read_quote_store,
    _read_quote_admin,
    _create_quote_store,
    _create_quote_admin,
    _update_quote_associate,
    _update_quote_customer,
    _update_quote_store,
    _update_quote_admin,
)
from commerce_mcp.tools.quote.schemas import (
    ReadQuoteParams,
    CreateQuoteParams,
    UpdateQuoteParams,
    QuoteUpdateAction,
    StagedQuoteReference,
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
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "q-1"}]})
    api.post = AsyncMock(return_value={"id": "q-1", "version": 2})
    return api


def make_create_params(**kwargs) -> CreateQuoteParams:
    return CreateQuoteParams(
        stagedQuote=StagedQuoteReference(id="sq-1"),
        stagedQuoteVersion=1,
        **kwargs,
    )


def make_update_params(**kwargs) -> UpdateQuoteParams:
    return UpdateQuoteParams(
        id="q-1",
        version=1,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Accepted")],
        **kwargs,
    )


# ── Context dispatch: read_quote ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_dispatches_to_associate_when_customer_and_bu(mock_api, bu_ctx):
    await read_quote(ReadQuoteParams(), mock_api, bu_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert "in-business-unit/key=bu-key" in path
    assert path.endswith("/quotes")


@pytest.mark.asyncio
async def test_read_dispatches_to_customer_when_customer_only(mock_api, customer_ctx):
    await read_quote(ReadQuoteParams(), mock_api, customer_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "/quotes" in path


@pytest.mark.asyncio
async def test_read_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await read_quote(ReadQuoteParams(), mock_api, store_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=my-store/quotes" in path


@pytest.mark.asyncio
async def test_read_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await read_quote(ReadQuoteParams(), mock_api, admin_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert path == "/quotes"


@pytest.mark.asyncio
async def test_read_associate_takes_priority_over_customer_only(mock_api, bu_ctx):
    await read_quote(ReadQuoteParams(), mock_api, bu_ctx)
    path = mock_api.get.call_args[0][0]
    assert "as-associate" in path


@pytest.mark.asyncio
async def test_read_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="read_quote"):
        await read_quote(ReadQuoteParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


# ── Context dispatch: create_quote ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await create_quote(make_create_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=my-store/quotes"


@pytest.mark.asyncio
async def test_create_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await create_quote(make_create_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/quotes"


@pytest.mark.asyncio
async def test_create_raises_context_error_for_associate(mock_api, bu_ctx):
    # Associate context (customer + BU) cannot create quotes
    with pytest.raises(ContextError, match="create_quote"):
        await create_quote(make_create_params(), mock_api, bu_ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_create_raises_context_error_for_customer_only(mock_api, customer_ctx):
    # Customer-only context cannot create quotes
    with pytest.raises(ContextError, match="create_quote"):
        await create_quote(make_create_params(), mock_api, customer_ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_create_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_quote"):
        await create_quote(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Context dispatch: update_quote ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_dispatches_to_associate_when_customer_and_bu(mock_api, bu_ctx):
    await update_quote(make_update_params(), mock_api, bu_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert "in-business-unit/key=bu-key" in path


@pytest.mark.asyncio
async def test_update_dispatches_to_customer_when_customer_only(mock_api, customer_ctx):
    await update_quote(make_update_params(), mock_api, customer_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/quotes/q-1" in path


@pytest.mark.asyncio
async def test_update_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await update_quote(make_update_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/in-store/key=my-store/quotes/" in path


@pytest.mark.asyncio
async def test_update_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await update_quote(make_update_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/quotes/q-1" in path


@pytest.mark.asyncio
async def test_update_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="update_quote"):
        await update_quote(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Associate read implementation ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_associate_list_uses_as_associate_path(mock_api, bu_ctx):
    await _read_quote_associate(ReadQuoteParams(), mock_api, bu_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/as-associate/cust-1/in-business-unit/key=bu-key/quotes"


@pytest.mark.asyncio
async def test_read_associate_by_id_uses_direct_path(mock_api, bu_ctx):
    mock_api.get.return_value = {"id": "q-1"}
    await _read_quote_associate(ReadQuoteParams(id="q-1"), mock_api, bu_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/as-associate/cust-1/in-business-unit/key=bu-key/quotes/q-1"


@pytest.mark.asyncio
async def test_read_associate_by_key_uses_key_path(mock_api, bu_ctx):
    mock_api.get.return_value = {"id": "q-1"}
    await _read_quote_associate(ReadQuoteParams(key="q-key"), mock_api, bu_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/as-associate/cust-1/in-business-unit/key=bu-key/quotes/key=q-key"


@pytest.mark.asyncio
async def test_read_associate_passes_query_params(mock_api, bu_ctx):
    await _read_quote_associate(
        ReadQuoteParams(limit=5, offset=10, sort=["createdAt desc"]),
        mock_api,
        bu_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 5
    assert params["offset"] == 10
    assert params["sort"] == ["createdAt desc"]


# ── Customer read implementation ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_customer_list_injects_customer_where_filter(mock_api, customer_ctx):
    # Customer context uses ownership filter on /quotes
    mock_api.get.return_value = {"count": 0, "results": []}
    await _read_quote_customer(ReadQuoteParams(), mock_api, customer_ctx)
    params = mock_api.get.call_args[1]["params"]
    where = params.get("where", [])
    assert any("cust-1" in c for c in where)


@pytest.mark.asyncio
async def test_read_customer_by_id_performs_ownership_check(mock_api, customer_ctx):
    # When the returned quote does not belong to the customer, SDKError is raised
    mock_api.get.return_value = {"id": "q-1", "customer": {"id": "other-cust"}}
    with pytest.raises(SDKError, match="Failed to read quote"):
        await _read_quote_customer(ReadQuoteParams(id="q-1"), mock_api, customer_ctx)


@pytest.mark.asyncio
async def test_read_customer_by_id_succeeds_when_owner_matches(mock_api, customer_ctx):
    mock_api.get.return_value = {"id": "q-1", "customer": {"id": "cust-1"}}
    result = await _read_quote_customer(ReadQuoteParams(id="q-1"), mock_api, customer_ctx)
    assert result is not None


@pytest.mark.asyncio
async def test_read_customer_by_key_performs_ownership_check(mock_api, customer_ctx):
    mock_api.get.return_value = {"id": "q-1", "customer": {"id": "other-cust"}}
    with pytest.raises(SDKError, match="Failed to read quote"):
        await _read_quote_customer(ReadQuoteParams(key="q-key"), mock_api, customer_ctx)


@pytest.mark.asyncio
async def test_read_customer_merges_extra_where(mock_api, customer_ctx):
    mock_api.get.return_value = {"count": 0, "results": []}
    await _read_quote_customer(
        ReadQuoteParams(where=['quoteState="Accepted"']),
        mock_api,
        customer_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    where = params["where"]
    assert any("cust-1" in c for c in where)
    assert any("Accepted" in c for c in where)


# ── Store read implementation ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_store_list_uses_in_store_path(mock_api, store_ctx):
    await _read_quote_store(ReadQuoteParams(), mock_api, store_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/in-store/key=my-store/quotes"


@pytest.mark.asyncio
async def test_read_store_by_id_uses_in_store_id_path(mock_api, store_ctx):
    mock_api.get.return_value = {"id": "q-1"}
    await _read_quote_store(ReadQuoteParams(id="q-1"), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/quotes/q-1"


@pytest.mark.asyncio
async def test_read_store_by_key_uses_in_store_key_path(mock_api, store_ctx):
    mock_api.get.return_value = {"id": "q-1"}
    await _read_quote_store(ReadQuoteParams(key="q-key"), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/quotes/key=q-key"


@pytest.mark.asyncio
async def test_read_store_injects_store_where_filter(mock_api, store_ctx):
    await _read_quote_store(ReadQuoteParams(), mock_api, store_ctx)
    params = mock_api.get.call_args[1]["params"]
    where = params.get("where", [])
    assert any("my-store" in c for c in where)


@pytest.mark.asyncio
async def test_read_store_passes_limit_and_sort(mock_api, store_ctx):
    await _read_quote_store(
        ReadQuoteParams(limit=15, sort=["createdAt asc"]),
        mock_api,
        store_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 15
    assert params["sort"] == ["createdAt asc"]


# ── Admin read implementation ─────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_admin_list_uses_quotes_endpoint(mock_api, admin_ctx):
    await _read_quote_admin(ReadQuoteParams(), mock_api, admin_ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/quotes"


@pytest.mark.asyncio
async def test_read_admin_by_id_uses_direct_path(mock_api, admin_ctx):
    mock_api.get.return_value = {"id": "q-99"}
    await _read_quote_admin(ReadQuoteParams(id="q-99"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/quotes/q-99"


@pytest.mark.asyncio
async def test_read_admin_by_key_uses_key_path(mock_api, admin_ctx):
    mock_api.get.return_value = {"id": "q-99"}
    await _read_quote_admin(ReadQuoteParams(key="my-key"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/quotes/key=my-key"


@pytest.mark.asyncio
async def test_read_admin_with_store_key_param_uses_in_store_prefix(mock_api, admin_ctx):
    await _read_quote_admin(ReadQuoteParams(store_key="eu-store"), mock_api, admin_ctx)
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=eu-store/quotes" in path


@pytest.mark.asyncio
async def test_read_admin_passes_limit_offset_sort(mock_api, admin_ctx):
    await _read_quote_admin(
        ReadQuoteParams(limit=20, offset=40, sort=["createdAt desc"]),
        mock_api,
        admin_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 20
    assert params["offset"] == 40
    assert params["sort"] == ["createdAt desc"]


# ── Store create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_store_posts_to_in_store_quotes_path(mock_api, store_ctx):
    await _create_quote_store(make_create_params(), mock_api, store_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=my-store/quotes"
    body = mock_api.post.call_args[1]["body"]
    assert body["stagedQuote"]["id"] == "sq-1"
    assert body["stagedQuoteVersion"] == 1


@pytest.mark.asyncio
async def test_create_store_includes_key_when_provided(mock_api, store_ctx):
    await _create_quote_store(make_create_params(key="q-custom"), mock_api, store_ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["key"] == "q-custom"


@pytest.mark.asyncio
async def test_create_store_uses_store_key_from_params_when_provided(mock_api, store_ctx):
    await _create_quote_store(
        make_create_params(store_key="override-store"),
        mock_api,
        store_ctx,
    )
    path = mock_api.post.call_args[0][0]
    assert "/in-store/key=override-store/quotes" in path


# ── Admin create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_admin_posts_to_quotes_endpoint(mock_api, admin_ctx):
    await _create_quote_admin(make_create_params(), mock_api, admin_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/quotes"
    body = mock_api.post.call_args[1]["body"]
    assert body["stagedQuote"]["id"] == "sq-1"
    assert body["stagedQuoteVersion"] == 1


@pytest.mark.asyncio
async def test_create_admin_with_store_key_param_uses_in_store_path(mock_api, admin_ctx):
    await _create_quote_admin(
        make_create_params(store_key="eu-store"),
        mock_api,
        admin_ctx,
    )
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=eu-store/quotes"


# ── Associate update implementation ───────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_associate_by_id_posts_to_as_associate_path(mock_api, bu_ctx):
    await _update_quote_associate(make_update_params(), mock_api, bu_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/as-associate/cust-1/in-business-unit/key=bu-key/quotes/q-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1


@pytest.mark.asyncio
async def test_update_associate_by_key_uses_key_path(mock_api, bu_ctx):
    params = UpdateQuoteParams(
        key="q-key",
        version=2,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Accepted")],
    )
    await _update_quote_associate(params, mock_api, bu_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/as-associate/cust-1/in-business-unit/key=bu-key/quotes/key=q-key"


@pytest.mark.asyncio
async def test_update_associate_rejects_disallowed_action(mock_api, bu_ctx):
    params = UpdateQuoteParams(
        id="q-1",
        version=1,
        actions=[QuoteUpdateAction(action="setCustomField")],
    )
    with pytest.raises(SDKError, match="update quote"):
        await _update_quote_associate(params, mock_api, bu_ctx)


@pytest.mark.asyncio
async def test_update_associate_rejects_invalid_quote_state(mock_api, bu_ctx):
    params = UpdateQuoteParams(
        id="q-1",
        version=1,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Pending")],
    )
    with pytest.raises(SDKError, match="update quote"):
        await _update_quote_associate(params, mock_api, bu_ctx)


@pytest.mark.asyncio
async def test_update_associate_allows_accepted_state(mock_api, bu_ctx):
    params = UpdateQuoteParams(
        id="q-1",
        version=1,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Accepted")],
    )
    result = await _update_quote_associate(params, mock_api, bu_ctx)
    assert result is not None


@pytest.mark.asyncio
async def test_update_associate_allows_declined_state(mock_api, bu_ctx):
    params = UpdateQuoteParams(
        id="q-1",
        version=1,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Declined")],
    )
    result = await _update_quote_associate(params, mock_api, bu_ctx)
    assert result is not None


@pytest.mark.asyncio
async def test_update_associate_raises_sdk_error_when_no_id_or_key(mock_api, bu_ctx):
    params = UpdateQuoteParams(
        version=1,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Accepted")],
    )
    with pytest.raises(SDKError, match="update quote"):
        await _update_quote_associate(params, mock_api, bu_ctx)


# ── Customer update implementation ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_customer_by_id_posts_to_quotes_path(mock_api, customer_ctx):
    await _update_quote_customer(make_update_params(), mock_api, customer_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/quotes/q-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1


@pytest.mark.asyncio
async def test_update_customer_by_key_uses_key_path(mock_api, customer_ctx):
    params = UpdateQuoteParams(
        key="q-key",
        version=2,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Accepted")],
    )
    await _update_quote_customer(params, mock_api, customer_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/quotes/key=q-key"


@pytest.mark.asyncio
async def test_update_customer_rejects_disallowed_action(mock_api, customer_ctx):
    params = UpdateQuoteParams(
        id="q-1",
        version=1,
        actions=[QuoteUpdateAction(action="setCustomField")],
    )
    with pytest.raises(SDKError, match="update quote"):
        await _update_quote_customer(params, mock_api, customer_ctx)


@pytest.mark.asyncio
async def test_update_customer_rejects_invalid_quote_state(mock_api, customer_ctx):
    params = UpdateQuoteParams(
        id="q-1",
        version=1,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Pending")],
    )
    with pytest.raises(SDKError, match="update quote"):
        await _update_quote_customer(params, mock_api, customer_ctx)


@pytest.mark.asyncio
async def test_update_customer_allows_accepted_state(mock_api, customer_ctx):
    params = UpdateQuoteParams(
        id="q-1",
        version=1,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Accepted")],
    )
    result = await _update_quote_customer(params, mock_api, customer_ctx)
    assert result is not None


@pytest.mark.asyncio
async def test_update_customer_with_store_key_param_uses_in_store_prefix(mock_api, customer_ctx):
    params = UpdateQuoteParams(
        id="q-1",
        version=1,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Accepted")],
        store_key="eu-store",
    )
    await _update_quote_customer(params, mock_api, customer_ctx)
    path = mock_api.post.call_args[0][0]
    assert "/in-store/key=eu-store/quotes/q-1" in path


@pytest.mark.asyncio
async def test_update_customer_raises_sdk_error_when_no_id_or_key(mock_api, customer_ctx):
    params = UpdateQuoteParams(
        version=1,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Accepted")],
    )
    with pytest.raises(SDKError, match="update quote"):
        await _update_quote_customer(params, mock_api, customer_ctx)


# ── Store update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_store_by_id_posts_to_in_store_path(mock_api, store_ctx):
    await _update_quote_store(make_update_params(), mock_api, store_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=my-store/quotes/q-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1


@pytest.mark.asyncio
async def test_update_store_by_key_uses_key_path(mock_api, store_ctx):
    params = UpdateQuoteParams(
        key="q-key",
        version=2,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Accepted")],
    )
    await _update_quote_store(params, mock_api, store_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=my-store/quotes/key=q-key"


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_when_no_id_or_key(mock_api, store_ctx):
    params = UpdateQuoteParams(
        version=1,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Accepted")],
    )
    with pytest.raises(SDKError, match="update quote"):
        await _update_quote_store(params, mock_api, store_ctx)


# ── Admin update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_admin_by_id_posts_to_direct_path(mock_api, admin_ctx):
    await _update_quote_admin(make_update_params(), mock_api, admin_ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/quotes/q-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1
    assert body["actions"][0]["action"] == "changeQuoteState"


@pytest.mark.asyncio
async def test_update_admin_by_key_uses_key_path(mock_api, admin_ctx):
    params = UpdateQuoteParams(
        key="q-key",
        version=3,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Declined")],
    )
    await _update_quote_admin(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/quotes/key=q-key"


@pytest.mark.asyncio
async def test_update_admin_with_store_key_param_uses_prefix(mock_api, admin_ctx):
    await _update_quote_admin(
        make_update_params(store_key="eu-store"),
        mock_api,
        admin_ctx,
    )
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/quotes/q-1"


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_when_no_id_or_key(mock_api, admin_ctx):
    params = UpdateQuoteParams(
        version=1,
        actions=[QuoteUpdateAction(action="changeQuoteState", quoteState="Accepted")],
    )
    with pytest.raises(SDKError, match="update quote"):
        await _update_quote_admin(params, mock_api, admin_ctx)


# ── SDK error wrapping ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_associate_raises_sdk_error_on_api_failure(mock_api, bu_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read quote"):
        await _read_quote_associate(ReadQuoteParams(), mock_api, bu_ctx)


@pytest.mark.asyncio
async def test_read_customer_raises_sdk_error_on_api_failure(mock_api, customer_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read quote"):
        await _read_quote_customer(ReadQuoteParams(), mock_api, customer_ctx)


@pytest.mark.asyncio
async def test_read_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read quote"):
        await _read_quote_store(ReadQuoteParams(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_read_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read quote"):
        await _read_quote_admin(ReadQuoteParams(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_create_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create quote"):
        await _create_quote_store(make_create_params(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_create_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create quote"):
        await _create_quote_admin(make_create_params(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_update_associate_raises_sdk_error_on_api_failure(mock_api, bu_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update quote"):
        await _update_quote_associate(make_update_params(), mock_api, bu_ctx)


@pytest.mark.asyncio
async def test_update_customer_raises_sdk_error_on_api_failure(mock_api, customer_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update quote"):
        await _update_quote_customer(make_update_params(), mock_api, customer_ctx)


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update quote"):
        await _update_quote_store(make_update_params(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update quote"):
        await _update_quote_admin(make_update_params(), mock_api, admin_ctx)


# ── Security: no admin fallthrough ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_does_not_fallthrough_to_admin(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError):
        await read_quote(ReadQuoteParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


@pytest.mark.asyncio
async def test_create_does_not_fallthrough_to_admin(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError):
        await create_quote(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_does_not_fallthrough_to_admin(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError):
        await update_quote(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()
