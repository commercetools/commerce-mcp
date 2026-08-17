import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.tax_category.functions import (
    create_tax_category,
    read_tax_category,
    update_tax_category,
)
from commerce_mcp.tools.tax_category.schemas import (
    CreateTaxCategoryParams,
    ReadTaxCategoryParams,
    TaxCategoryUpdateAction,
    TaxRate,
    UpdateTaxCategoryParams,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "tc-1", "key": "standard", "version": 2})
    api.post = AsyncMock(return_value={"id": "tc-1", "version": 3})
    return api


def make_create_params() -> CreateTaxCategoryParams:
    return CreateTaxCategoryParams(
        name="Standard Tax",
        rates=[
            TaxRate(name="19% DE", amount=0.19, country="DE", includedInPrice=False)
        ],
    )


def make_update_params(use_id: bool = True) -> UpdateTaxCategoryParams:
    return UpdateTaxCategoryParams(
        version=2,
        actions=[TaxCategoryUpdateAction(action="changeName", name="Updated Tax")],
        id="tc-1" if use_id else None,
        key="standard" if not use_id else None,
    )


class TestReadTaxCategory:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_tax_category(ReadTaxCategoryParams(id="tc-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/tax-categories/tc-1", params=None)
        assert json.loads(result)["id"] == "tc-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_tax_category(ReadTaxCategoryParams(key="standard"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/tax-categories/key=standard", params=None)

    @pytest.mark.asyncio
    async def test_list(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_tax_category(ReadTaxCategoryParams(limit=25, offset=5), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 25
        assert call_params["offset"] == 5

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_tax_category"):
            await read_tax_category(ReadTaxCategoryParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("network error")
        with pytest.raises(SDKError, match="read tax category"):
            await read_tax_category(ReadTaxCategoryParams(id="tc-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_tax_category(ReadTaxCategoryParams(id="tc-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateTaxCategory:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        result = await create_tax_category(make_create_params(), mock_api, admin_ctx)
        mock_api.post.assert_called_once()
        body = mock_api.post.call_args[1]["body"]
        assert body["name"] == "Standard Tax"
        assert body["rates"][0]["amount"] == 0.19
        assert json.loads(result)["id"] == "tc-1"

    @pytest.mark.asyncio
    async def test_create_sets_included_in_price_default(self, mock_api, admin_ctx):
        # When includedInPrice is not provided it should default to False
        params = CreateTaxCategoryParams(
            name="Reduced Tax",
            rates=[TaxRate(name="7% DE", amount=0.07, country="DE")],
        )
        await create_tax_category(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["rates"][0].get("includedInPrice") == False

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_tax_category"):
            await create_tax_category(make_create_params(), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("server error")
        with pytest.raises(SDKError, match="create tax category"):
            await create_tax_category(make_create_params(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await create_tax_category(make_create_params(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestUpdateTaxCategory:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        result = await update_tax_category(make_update_params(use_id=True), mock_api, admin_ctx)
        mock_api.post.assert_called_once()
        path = mock_api.post.call_args[0][0]
        assert path == "/tax-categories/tc-1"
        body = mock_api.post.call_args[1]["body"]
        assert body["version"] == 2
        assert body["actions"][0]["action"] == "changeName"
        assert json.loads(result)["version"] == 3

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        await update_tax_category(make_update_params(use_id=False), mock_api, admin_ctx)
        path = mock_api.post.call_args[0][0]
        assert path == "/tax-categories/key=standard"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="update_tax_category"):
            await update_tax_category(make_update_params(), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateTaxCategoryParams(
            version=2,
            actions=[TaxCategoryUpdateAction(action="changeName", name="X")],
        )
        with pytest.raises(SDKError, match="update tax category"):
            await update_tax_category(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("server error")
        with pytest.raises(SDKError, match="update tax category"):
            await update_tax_category(make_update_params(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await update_tax_category(make_update_params(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)
