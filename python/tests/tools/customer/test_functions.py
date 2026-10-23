"""Tests for customer context-conditional dispatch."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.tools.customer.functions import read_customer, create_customer, update_customer
from commerce_mcp.tools.customer.schemas import (
    ReadCustomerParams,
    CreateCustomerParams,
    UpdateCustomerParams,
    CustomerUpdateAction,
)
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import SDKError, ContextError


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "cust-1", "version": 1, "email": "test@example.com"})
    api.post = AsyncMock(return_value={"customer": {"id": "cust-1", "version": 1}, "cart": None})
    return api


def make_create_params(**kwargs) -> CreateCustomerParams:
    return CreateCustomerParams(email="test@example.com", password="secret123", **kwargs)


def make_update_params(**kwargs) -> UpdateCustomerParams:
    return UpdateCustomerParams(
        id="cust-1",
        version=1,
        actions=[CustomerUpdateAction(action="setFirstName", firstName="Alice")],
        **kwargs,
    )


# ── Customer context: read own profile ────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_customer_self_uses_customer_id_path(mock_api):
    ctx = CTContext(customer_id="cust-1")
    await read_customer(ReadCustomerParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/customers/cust-1"


@pytest.mark.asyncio
async def test_read_customer_self_with_expand(mock_api):
    ctx = CTContext(customer_id="cust-1")
    await read_customer(ReadCustomerParams(expand=["customerGroup"]), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/customers/cust-1"
    params = mock_api.get.call_args[1]["params"]
    assert params is not None
    assert "expand" in params


@pytest.mark.asyncio
async def test_create_customer_raises_context_error_for_customer_context(mock_api):
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(ContextError, match="create_customer"):
        await create_customer(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_customer_raises_context_error_for_customer_context(mock_api):
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(ContextError, match="update_customer"):
        await update_customer(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── Store context: all three tools ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_customer_store_list_uses_in_store_path(mock_api):
    mock_api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "cust-1"}]})
    ctx = CTContext(store_key="eu-store")
    await read_customer(ReadCustomerParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/customers"


@pytest.mark.asyncio
async def test_read_customer_store_by_id_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await read_customer(ReadCustomerParams(id="cust-1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/customers/cust-1"


@pytest.mark.asyncio
async def test_read_customer_store_list_with_where_and_sort(mock_api):
    mock_api.get = AsyncMock(return_value={"count": 0, "results": []})
    ctx = CTContext(store_key="eu-store")
    await read_customer(
        ReadCustomerParams(where=['email="a@b.com"'], sort=["lastName asc"], limit=5, offset=0),
        mock_api,
        ctx,
    )
    path = mock_api.get.call_args[0][0]
    assert path == "/in-store/key=eu-store/customers"
    p = mock_api.get.call_args[1]["params"]
    assert p["limit"] == 5
    assert p["offset"] == 0
    assert p["sort"] == ["lastName asc"]


@pytest.mark.asyncio
async def test_create_customer_store_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await create_customer(make_create_params(), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/customers"


@pytest.mark.asyncio
async def test_create_customer_store_strips_store_key_from_body(mock_api):
    ctx = CTContext(store_key="eu-store")
    # storeKey is in params but should be stripped from the POST body (it's in the URL)
    await create_customer(make_create_params(store_key="eu-store"), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert "storeKey" not in body


@pytest.mark.asyncio
async def test_update_customer_store_uses_in_store_path(mock_api):
    ctx = CTContext(store_key="eu-store")
    await update_customer(make_update_params(), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/customers/cust-1"


@pytest.mark.asyncio
async def test_update_customer_store_body_has_version_and_actions(mock_api):
    ctx = CTContext(store_key="eu-store")
    await update_customer(make_update_params(), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1
    assert isinstance(body["actions"], list)
    assert body["actions"][0]["action"] == "setFirstName"


# ── Admin context: all three tools ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_customer_admin_list_uses_customers_path(mock_api):
    mock_api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "cust-1"}]})
    ctx = CTContext(is_admin=True)
    await read_customer(ReadCustomerParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/customers"


@pytest.mark.asyncio
async def test_read_customer_admin_by_id_uses_customers_id_path(mock_api):
    ctx = CTContext(is_admin=True)
    await read_customer(ReadCustomerParams(id="cust-1"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/customers/cust-1"


@pytest.mark.asyncio
async def test_read_customer_admin_by_id_with_store_key_override(mock_api):
    ctx = CTContext(is_admin=True)
    await read_customer(ReadCustomerParams(id="cust-1", store_key="eu-store"), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/in-store/key=eu-store/customers/cust-1"


@pytest.mark.asyncio
async def test_read_customer_admin_list_with_where(mock_api):
    mock_api.get = AsyncMock(return_value={"count": 0, "results": []})
    ctx = CTContext(is_admin=True)
    await read_customer(ReadCustomerParams(where=['email="x@y.com"']), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert path == "/customers"
    p = mock_api.get.call_args[1]["params"]
    assert p["where"] == ['email="x@y.com"']


@pytest.mark.asyncio
async def test_create_customer_admin_uses_customers_path(mock_api):
    ctx = CTContext(is_admin=True)
    await create_customer(make_create_params(), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/customers"


@pytest.mark.asyncio
async def test_create_customer_admin_with_store_key_uses_in_store_path(mock_api):
    ctx = CTContext(is_admin=True)
    await create_customer(make_create_params(store_key="eu-store"), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/in-store/key=eu-store/customers"


@pytest.mark.asyncio
async def test_create_customer_admin_store_key_stripped_from_body(mock_api):
    ctx = CTContext(is_admin=True)
    await create_customer(make_create_params(store_key="eu-store"), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert "storeKey" not in body


@pytest.mark.asyncio
async def test_create_customer_admin_body_has_email_and_password(mock_api):
    ctx = CTContext(is_admin=True)
    await create_customer(make_create_params(), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["email"] == "test@example.com"
    assert body["password"] == "secret123"


@pytest.mark.asyncio
async def test_update_customer_admin_uses_customers_id_path(mock_api):
    ctx = CTContext(is_admin=True)
    await update_customer(make_update_params(), mock_api, ctx)
    assert mock_api.post.call_args[0][0] == "/customers/cust-1"


@pytest.mark.asyncio
async def test_update_customer_admin_body_has_version_and_actions(mock_api):
    ctx = CTContext(is_admin=True)
    await update_customer(make_update_params(), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 1
    assert isinstance(body["actions"], list)
    assert body["actions"][0]["action"] == "setFirstName"


# ── Empty context: all three tools raise ContextError ─────────────────────────

@pytest.mark.asyncio
async def test_read_customer_raises_context_error_with_empty_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="read_customer"):
        await read_customer(ReadCustomerParams(), mock_api, ctx)
    mock_api.get.assert_not_called()


@pytest.mark.asyncio
async def test_create_customer_raises_context_error_with_empty_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="create_customer"):
        await create_customer(make_create_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


@pytest.mark.asyncio
async def test_update_customer_raises_context_error_with_empty_context(mock_api):
    ctx = CTContext()
    with pytest.raises(ContextError, match="update_customer"):
        await update_customer(make_update_params(), mock_api, ctx)
    mock_api.post.assert_not_called()


# ── SDKError on API failure ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_read_customer_self_raises_sdk_error_on_failure(mock_api):
    mock_api.get.side_effect = Exception("500 Server Error")
    ctx = CTContext(customer_id="cust-1")
    with pytest.raises(SDKError, match="Failed to read customer"):
        await read_customer(ReadCustomerParams(), mock_api, ctx)


@pytest.mark.asyncio
async def test_read_customer_store_raises_sdk_error_on_failure(mock_api):
    mock_api.get.side_effect = Exception("500 Server Error")
    ctx = CTContext(store_key="eu-store")
    with pytest.raises(SDKError, match="Failed to read customer"):
        await read_customer(ReadCustomerParams(), mock_api, ctx)


@pytest.mark.asyncio
async def test_read_customer_admin_raises_sdk_error_on_failure(mock_api):
    mock_api.get.side_effect = Exception("500 Server Error")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to read customer"):
        await read_customer(ReadCustomerParams(), mock_api, ctx)


@pytest.mark.asyncio
async def test_create_customer_store_raises_sdk_error_on_failure(mock_api):
    mock_api.post.side_effect = Exception("500 Server Error")
    ctx = CTContext(store_key="eu-store")
    with pytest.raises(SDKError, match="Failed to create customer"):
        await create_customer(make_create_params(), mock_api, ctx)


@pytest.mark.asyncio
async def test_create_customer_admin_raises_sdk_error_on_failure(mock_api):
    mock_api.post.side_effect = Exception("500 Server Error")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to create customer"):
        await create_customer(make_create_params(), mock_api, ctx)


@pytest.mark.asyncio
async def test_update_customer_store_raises_sdk_error_on_failure(mock_api):
    mock_api.post.side_effect = Exception("500 Server Error")
    ctx = CTContext(store_key="eu-store")
    with pytest.raises(SDKError, match="Failed to update customer"):
        await update_customer(make_update_params(), mock_api, ctx)


@pytest.mark.asyncio
async def test_update_customer_admin_raises_sdk_error_on_failure(mock_api):
    mock_api.post.side_effect = Exception("500 Server Error")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to update customer"):
        await update_customer(make_update_params(), mock_api, ctx)
