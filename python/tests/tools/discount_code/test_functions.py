import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.discount_code.functions import (
    create_discount_code,
    read_discount_code,
    update_discount_code,
)
from commerce_mcp.tools.discount_code.schemas import (
    CartDiscountReference,
    CreateDiscountCodeParams,
    DiscountCodeUpdateAction,
    ReadDiscountCodeParams,
    UpdateDiscountCodeParams,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "dc-1", "code": "SAVE10"})
    api.post = AsyncMock(return_value={"id": "dc-1", "version": 2})
    return api


class TestReadDiscountCode:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_discount_code(ReadDiscountCodeParams(id="dc-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/discount-codes/dc-1", params=None)
        assert json.loads(result)["id"] == "dc-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_discount_code(ReadDiscountCodeParams(key="SAVE10"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/discount-codes/key=SAVE10", params=None)

    @pytest.mark.asyncio
    async def test_list_codes(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        result = await read_discount_code(ReadDiscountCodeParams(limit=5), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 5
        assert "results" in json.loads(result)

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_discount_code"):
            await read_discount_code(ReadDiscountCodeParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("network error")
        with pytest.raises(SDKError, match="read discount code"):
            await read_discount_code(ReadDiscountCodeParams(id="dc-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_discount_code(ReadDiscountCodeParams(id="dc-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateDiscountCode:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        params = CreateDiscountCodeParams(
            code="SAVE10",
            cartDiscounts=[CartDiscountReference(id="cd-1")],
        )
        result = await create_discount_code(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["code"] == "SAVE10"
        assert body["cartDiscounts"][0]["id"] == "cd-1"
        assert json.loads(result)["id"] == "dc-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = CreateDiscountCodeParams(code="X", cartDiscounts=[CartDiscountReference(id="cd-1")])
        with pytest.raises(ContextError, match="create_discount_code"):
            await create_discount_code(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError, match="create discount code"):
            await create_discount_code(
                CreateDiscountCodeParams(code="X", cartDiscounts=[CartDiscountReference(id="cd-1")]),
                mock_api, admin_ctx,
            )


class TestUpdateDiscountCode:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateDiscountCodeParams(id="dc-1", version=1, actions=[DiscountCodeUpdateAction(action="setIsActive", isActive=False)])
        result = await update_discount_code(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/discount-codes/dc-1"
        assert json.loads(result)["version"] == 2

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateDiscountCodeParams(key="SAVE10", version=1, actions=[DiscountCodeUpdateAction(action="setIsActive", isActive=True)])
        await update_discount_code(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/discount-codes/key=SAVE10"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = UpdateDiscountCodeParams(id="dc-1", version=1, actions=[DiscountCodeUpdateAction(action="setIsActive")])
        with pytest.raises(ContextError, match="update_discount_code"):
            await update_discount_code(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateDiscountCodeParams(version=1, actions=[DiscountCodeUpdateAction(action="setIsActive")])
        with pytest.raises(SDKError):
            await update_discount_code(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("conflict")
        params = UpdateDiscountCodeParams(id="dc-1", version=1, actions=[DiscountCodeUpdateAction(action="setIsActive")])
        with pytest.raises(SDKError, match="update discount code"):
            await update_discount_code(params, mock_api, admin_ctx)
