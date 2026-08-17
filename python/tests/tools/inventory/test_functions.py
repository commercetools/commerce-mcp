import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.inventory.functions import create_inventory, read_inventory, update_inventory
from commerce_mcp.tools.inventory.schemas import (
    CreateInventoryParams,
    InventoryUpdateAction,
    ReadInventoryParams,
    UpdateInventoryParams,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "inv-1", "sku": "SKU-123"})
    api.post = AsyncMock(return_value={"id": "inv-1", "version": 2})
    return api


class TestReadInventory:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_inventory(ReadInventoryParams(id="inv-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/inventory/inv-1", params=None)
        assert json.loads(result)["id"] == "inv-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_inventory(ReadInventoryParams(key="my-inv"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/inventory/key=my-inv", params=None)

    @pytest.mark.asyncio
    async def test_list_inventory(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_inventory(ReadInventoryParams(where=['sku="SKU-123"'], limit=10), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["where"] == ['sku="SKU-123"']
        assert call_params["limit"] == 10

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_inventory"):
            await read_inventory(ReadInventoryParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError, match="read inventory"):
            await read_inventory(ReadInventoryParams(id="inv-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_inventory(ReadInventoryParams(id="inv-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateInventory:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        params = CreateInventoryParams(sku="SKU-123", quantityOnStock=100)
        result = await create_inventory(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["sku"] == "SKU-123"
        assert body["quantityOnStock"] == 100
        assert json.loads(result)["id"] == "inv-1"

    @pytest.mark.asyncio
    async def test_create_excludes_none_fields(self, mock_api, admin_ctx):
        await create_inventory(CreateInventoryParams(sku="SKU-X", quantityOnStock=0), mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert "supplyChannel" not in body

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_inventory"):
            await create_inventory(CreateInventoryParams(sku="X", quantityOnStock=0), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError, match="create inventory"):
            await create_inventory(CreateInventoryParams(sku="X", quantityOnStock=0), mock_api, admin_ctx)


class TestUpdateInventory:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateInventoryParams(id="inv-1", version=1, actions=[InventoryUpdateAction(action="addQuantity", quantity=10)])
        result = await update_inventory(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/inventory/inv-1"
        assert json.loads(result)["version"] == 2

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateInventoryParams(key="my-inv", version=1, actions=[InventoryUpdateAction(action="addQuantity", quantity=5)])
        await update_inventory(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/inventory/key=my-inv"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = UpdateInventoryParams(id="inv-1", version=1, actions=[InventoryUpdateAction(action="addQuantity")])
        with pytest.raises(ContextError, match="update_inventory"):
            await update_inventory(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateInventoryParams(version=1, actions=[InventoryUpdateAction(action="addQuantity")])
        with pytest.raises(SDKError):
            await update_inventory(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("conflict")
        params = UpdateInventoryParams(id="inv-1", version=1, actions=[InventoryUpdateAction(action="addQuantity")])
        with pytest.raises(SDKError, match="update inventory"):
            await update_inventory(params, mock_api, admin_ctx)
