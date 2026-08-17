"""Tests for staged_quote context-conditional dispatch."""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.staged_quote.functions import (
    read_staged_quote,
    create_staged_quote,
    update_staged_quote,
    _read_staged_quote_admin,
    _read_staged_quote_store,
    _create_staged_quote_admin,
    _create_staged_quote_store,
    _update_staged_quote_admin,
    _update_staged_quote_store,
)
from commerce_mcp.tools.staged_quote.schemas import (
    ReadStagedQuoteParams,
    CreateStagedQuoteParams,
    UpdateStagedQuoteParams,
    QuoteRequestReference,
    StagedQuoteUpdateAction,
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
    api.get = AsyncMock(return_value={"id": "x-1"})
    api.post = AsyncMock(return_value={"id": "x-1", "version": 1})
    return api


def make_create_params() -> CreateStagedQuoteParams:
    return CreateStagedQuoteParams(
        quoteRequest=QuoteRequestReference(id="qr-1"),
        quoteRequestVersion=1,
    )


def make_update_params(**kwargs) -> UpdateStagedQuoteParams:
    return UpdateStagedQuoteParams(
        id="sq-1",
        version=2,
        actions=[StagedQuoteUpdateAction(action="changeStagedQuoteState")],
        **kwargs,
    )


# ── Dispatch: read_staged_quote ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_dispatches_to_store_when_store_key(mock_api, store_ctx):
    result = await read_staged_quote(ReadStagedQuoteParams(), mock_api, store_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=my-store/staged-quotes" in path


@pytest.mark.asyncio
async def test_read_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    result = await read_staged_quote(ReadStagedQuoteParams(), mock_api, admin_ctx)
    mock_api.get.assert_called_once()
    path = mock_api.get.call_args[0][0]
    assert path == "/staged-quotes"


@pytest.mark.asyncio
async def test_read_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="read_staged_quote"):
        await read_staged_quote(ReadStagedQuoteParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


# ── Dispatch: create_staged_quote ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await create_staged_quote(make_create_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=my-store/staged-quotes"


@pytest.mark.asyncio
async def test_create_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await create_staged_quote(make_create_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/staged-quotes"


@pytest.mark.asyncio
async def test_create_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_staged_quote"):
        await create_staged_quote(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Dispatch: update_staged_quote ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_dispatches_to_store_when_store_key(mock_api, store_ctx):
    await update_staged_quote(make_update_params(), mock_api, store_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert "/in-store/key=my-store/staged-quotes/" in path


@pytest.mark.asyncio
async def test_update_dispatches_to_admin_when_is_admin(mock_api, admin_ctx):
    await update_staged_quote(make_update_params(), mock_api, admin_ctx)
    mock_api.post.assert_called_once()
    path = mock_api.post.call_args[0][0]
    assert path == "/staged-quotes/sq-1"


@pytest.mark.asyncio
async def test_update_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="update_staged_quote"):
        await update_staged_quote(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Admin read implementation ─────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_admin_list_uses_staged_quotes_endpoint(mock_api, admin_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_staged_quote_admin(ReadStagedQuoteParams(), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/staged-quotes"


@pytest.mark.asyncio
async def test_read_admin_by_id_uses_direct_path(mock_api, admin_ctx):
    await _read_staged_quote_admin(ReadStagedQuoteParams(id="sq-99"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/staged-quotes/sq-99"


@pytest.mark.asyncio
async def test_read_admin_by_key_uses_key_path(mock_api, admin_ctx):
    await _read_staged_quote_admin(ReadStagedQuoteParams(key="my-key"), mock_api, admin_ctx)
    assert mock_api.get.call_args[0][0] == "/staged-quotes/key=my-key"


@pytest.mark.asyncio
async def test_read_admin_passes_query_params(mock_api, admin_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_staged_quote_admin(
        ReadStagedQuoteParams(limit=5, offset=10, sort=["createdAt desc"]),
        mock_api,
        admin_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 5
    assert params["offset"] == 10
    assert params["sort"] == ["createdAt desc"]


@pytest.mark.asyncio
async def test_read_admin_with_expand(mock_api, admin_ctx):
    await _read_staged_quote_admin(
        ReadStagedQuoteParams(id="sq-1", expand=["quoteRequest"]),
        mock_api,
        admin_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["expand"] == ["quoteRequest"]


# ── Store read implementation ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_store_list_uses_in_store_path(mock_api, store_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_staged_quote_store(ReadStagedQuoteParams(), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/staged-quotes"


@pytest.mark.asyncio
async def test_read_store_by_id_uses_in_store_path(mock_api, store_ctx):
    await _read_staged_quote_store(ReadStagedQuoteParams(id="sq-2"), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/staged-quotes/sq-2"


@pytest.mark.asyncio
async def test_read_store_by_key_uses_in_store_path(mock_api, store_ctx):
    await _read_staged_quote_store(ReadStagedQuoteParams(key="sq-key"), mock_api, store_ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=my-store/staged-quotes/key=sq-key"


@pytest.mark.asyncio
async def test_read_store_passes_query_params(mock_api, store_ctx):
    mock_api.get.return_value = {"results": [], "count": 0}
    await _read_staged_quote_store(
        ReadStagedQuoteParams(where=["stagedQuoteState=\"Sent\""], limit=20),
        mock_api,
        store_ctx,
    )
    params = mock_api.get.call_args[1]["params"]
    assert params["where"] == ["stagedQuoteState=\"Sent\""]
    assert params["limit"] == 20


# ── Admin create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_admin_posts_to_staged_quotes(mock_api, admin_ctx):
    await _create_staged_quote_admin(make_create_params(), mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/staged-quotes"
    body = mock_api.post.call_args[1]["body"]
    assert body["quoteRequest"]["id"] == "qr-1"
    assert body["quoteRequestVersion"] == 1


# ── Store create implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_store_posts_to_in_store_path(mock_api, store_ctx):
    await _create_staged_quote_store(make_create_params(), mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/staged-quotes"
    body = mock_api.post.call_args[1]["body"]
    assert body["quoteRequest"]["id"] == "qr-1"
    assert body["quoteRequestVersion"] == 1


# ── Admin update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_admin_by_id_posts_to_direct_path(mock_api, admin_ctx):
    await _update_staged_quote_admin(make_update_params(), mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/staged-quotes/sq-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 2
    assert body["actions"][0]["action"] == "changeStagedQuoteState"


@pytest.mark.asyncio
async def test_update_admin_by_key_posts_to_key_path(mock_api, admin_ctx):
    params = UpdateStagedQuoteParams(
        key="my-key", version=3, actions=[StagedQuoteUpdateAction(action="setCustomField")]
    )
    await _update_staged_quote_admin(params, mock_api, admin_ctx)
    assert mock_api.post.call_args[0][0] == "/staged-quotes/key=my-key"


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_when_no_id_or_key(mock_api, admin_ctx):
    params = UpdateStagedQuoteParams(
        version=1, actions=[StagedQuoteUpdateAction(action="changeStagedQuoteState")]
    )
    with pytest.raises(SDKError, match="update staged quote"):
        await _update_staged_quote_admin(params, mock_api, admin_ctx)


# ── Store update implementation ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_store_by_id_posts_to_in_store_path(mock_api, store_ctx):
    await _update_staged_quote_store(make_update_params(), mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/staged-quotes/sq-1"
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 2


@pytest.mark.asyncio
async def test_update_store_by_key_posts_to_in_store_key_path(mock_api, store_ctx):
    params = UpdateStagedQuoteParams(
        key="sq-key", version=1, actions=[StagedQuoteUpdateAction(action="changeStagedQuoteState")]
    )
    await _update_staged_quote_store(params, mock_api, store_ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=my-store/staged-quotes/key=sq-key"


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_when_no_id_or_key(mock_api, store_ctx):
    params = UpdateStagedQuoteParams(
        version=1, actions=[StagedQuoteUpdateAction(action="changeStagedQuoteState")]
    )
    with pytest.raises(SDKError, match="update staged quote"):
        await _update_staged_quote_store(params, mock_api, store_ctx)


# ── SDK error wrapping ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read staged quote"):
        await _read_staged_quote_admin(ReadStagedQuoteParams(id="sq-1"), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_read_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.get.side_effect = Exception("network failure")
    with pytest.raises(SDKError, match="Failed to read staged quote"):
        await _read_staged_quote_store(ReadStagedQuoteParams(id="sq-1"), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_create_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create staged quote"):
        await _create_staged_quote_admin(make_create_params(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_create_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to create staged quote"):
        await _create_staged_quote_store(make_create_params(), mock_api, store_ctx)


@pytest.mark.asyncio
async def test_update_admin_raises_sdk_error_on_api_failure(mock_api, admin_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update staged quote"):
        await _update_staged_quote_admin(make_update_params(), mock_api, admin_ctx)


@pytest.mark.asyncio
async def test_update_store_raises_sdk_error_on_api_failure(mock_api, store_ctx):
    mock_api.post.side_effect = Exception("500 error")
    with pytest.raises(SDKError, match="Failed to update staged quote"):
        await _update_staged_quote_store(make_update_params(), mock_api, store_ctx)


# ── store_key takes priority over is_admin ────────────────────────────────────

@pytest.mark.asyncio
async def test_read_uses_store_path_when_both_store_key_and_admin(mock_api):
    ctx = CTContext(is_admin=True, store_key="priority-store")
    await read_staged_quote(ReadStagedQuoteParams(), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert "/in-store/key=priority-store/staged-quotes" in path


@pytest.mark.asyncio
async def test_create_uses_store_path_when_both_store_key_and_admin(mock_api):
    ctx = CTContext(is_admin=True, store_key="priority-store")
    await create_staged_quote(make_create_params(), mock_api, ctx)
    path = mock_api.post.call_args[0][0]
    assert path == "/in-store/key=priority-store/staged-quotes"
