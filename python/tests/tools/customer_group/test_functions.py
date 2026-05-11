import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.customer_group.functions import (
    create_customer_group,
    read_customer_group,
    update_customer_group,
)
from commerce_mcp.tools.customer_group.schemas import (
    CreateCustomerGroupParams,
    CustomerGroupUpdateAction,
    ReadCustomerGroupParams,
    UpdateCustomerGroupParams,
)


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "cg-1", "key": "vip", "name": "VIP"})
    api.post = AsyncMock(return_value={"id": "cg-1", "version": 1})
    return api


class TestReadCustomerGroup:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_customer_group(ReadCustomerGroupParams(id="cg-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/customer-groups/cg-1", params=None)
        assert json.loads(result)["id"] == "cg-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_customer_group(ReadCustomerGroupParams(key="vip"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/customer-groups/key=vip", params=None)

    @pytest.mark.asyncio
    async def test_list_customer_groups(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_customer_group(ReadCustomerGroupParams(limit=10), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["limit"] == 10

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_customer_group"):
            await read_customer_group(ReadCustomerGroupParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await read_customer_group(ReadCustomerGroupParams(id="cg-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_customer_group(ReadCustomerGroupParams(id="cg-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateCustomerGroup:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        params = CreateCustomerGroupParams(groupName="VIP")
        result = await create_customer_group(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["groupName"] == "VIP"
        assert json.loads(result)["id"] == "cg-1"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_customer_group"):
            await create_customer_group(CreateCustomerGroupParams(groupName="VIP"), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await create_customer_group(CreateCustomerGroupParams(groupName="VIP"), mock_api, admin_ctx)


class TestUpdateCustomerGroup:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateCustomerGroupParams(
            id="cg-1",
            version=1,
            actions=[CustomerGroupUpdateAction(action="changeName")],
        )
        result = await update_customer_group(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/customer-groups/cg-1",
            body={"version": 1, "actions": [{"action": "changeName"}]},
        )
        assert json.loads(result)["id"] == "cg-1"

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateCustomerGroupParams(
            key="vip",
            version=1,
            actions=[CustomerGroupUpdateAction(action="changeName")],
        )
        await update_customer_group(params, mock_api, admin_ctx)
        mock_api.post.assert_called_once_with(
            "/customer-groups/key=vip",
            body={"version": 1, "actions": [{"action": "changeName"}]},
        )

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateCustomerGroupParams(
            version=1,
            actions=[CustomerGroupUpdateAction(action="changeName")],
        )
        with pytest.raises(SDKError):
            await update_customer_group(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = UpdateCustomerGroupParams(
            id="cg-1",
            version=1,
            actions=[CustomerGroupUpdateAction(action="changeName")],
        )
        with pytest.raises(ContextError, match="update_customer_group"):
            await update_customer_group(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        params = UpdateCustomerGroupParams(
            id="cg-1",
            version=1,
            actions=[CustomerGroupUpdateAction(action="changeName")],
        )
        with pytest.raises(SDKError):
            await update_customer_group(params, mock_api, admin_ctx)
