import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.bulk.functions import bulk_create, bulk_update
from commerce_mcp.tools.bulk.schemas import BulkCreateItem, BulkCreateParams, BulkUpdateItem, BulkUpdateParams


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.post = AsyncMock(return_value={"id": "result-1", "version": 1})
    return api


class TestBulkCreate:
    @pytest.mark.asyncio
    async def test_bulk_create_calls_individual_creates(self, mock_api, admin_ctx):
        async def fake_create_fn(params, api, ctx):
            return '{"id": "zone-1"}'

        with patch("commerce_mcp.tools.bulk.functions._get_create_fn", return_value=fake_create_fn):
            params = BulkCreateParams(items=[
                BulkCreateItem(entityType="zones", data={"name": {"en": "EU Zone"}}),
            ])
            result = await bulk_create(params, mock_api, admin_ctx)
            output = json.loads(result)
            assert output["success"] is True
            assert len(output["results"]) == 1
            assert output["results"][0]["id"] == "zone-1"

    @pytest.mark.asyncio
    async def test_bulk_create_captures_errors_per_item(self, mock_api, admin_ctx):
        mock_create_fn = AsyncMock(side_effect=Exception("create failed"))
        with patch("commerce_mcp.tools.bulk.functions._get_create_fn", return_value=mock_create_fn):
            params = BulkCreateParams(items=[
                BulkCreateItem(entityType="zones", data={"name": {"en": "EU Zone"}}),
            ])
            result = await bulk_create(params, mock_api, admin_ctx)
            output = json.loads(result)
            assert output["success"] is True
            assert "error" in output["results"][0]

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = BulkCreateParams(items=[
            BulkCreateItem(entityType="zones", data={}),
        ])
        with pytest.raises(ContextError, match="bulk_create"):
            await bulk_create(params, mock_api, CTContext())

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        async def fake_create_fn(params, api, ctx):
            return '{"id": "zone-1"}'

        with patch("commerce_mcp.tools.bulk.functions._get_create_fn", return_value=fake_create_fn):
            params = BulkCreateParams(items=[
                BulkCreateItem(entityType="zones", data={}),
            ])
            result = await bulk_create(params, mock_api, admin_ctx)
            assert isinstance(result, str)
            json.loads(result)


class TestBulkUpdate:
    @pytest.mark.asyncio
    async def test_bulk_update_calls_individual_updates(self, mock_api, admin_ctx):
        mock_update_fn = AsyncMock(return_value='{"id": "zone-1", "version": 2}')
        with patch("commerce_mcp.tools.bulk.functions._get_update_fn", return_value=mock_update_fn):
            params = BulkUpdateParams(items=[
                BulkUpdateItem(
                    entityType="zones",
                    data={"id": "zone-1", "version": 1, "actions": [{"action": "changeName"}]},
                ),
            ])
            result = await bulk_update(params, mock_api, admin_ctx)
            output = json.loads(result)
            assert output["success"] is True
            assert len(output["results"]) == 1
            assert output["results"][0]["id"] == "zone-1"

    @pytest.mark.asyncio
    async def test_bulk_update_captures_errors_per_item(self, mock_api, admin_ctx):
        mock_update_fn = AsyncMock(side_effect=Exception("update failed"))
        with patch("commerce_mcp.tools.bulk.functions._get_update_fn", return_value=mock_update_fn):
            params = BulkUpdateParams(items=[
                BulkUpdateItem(
                    entityType="zones",
                    data={"id": "zone-1", "version": 1, "actions": []},
                ),
            ])
            result = await bulk_update(params, mock_api, admin_ctx)
            output = json.loads(result)
            assert output["success"] is True
            assert "error" in output["results"][0]

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = BulkUpdateParams(items=[
            BulkUpdateItem(entityType="zones", data={}),
        ])
        with pytest.raises(ContextError, match="bulk_update"):
            await bulk_update(params, mock_api, CTContext())

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        async def fake_update_fn(params, api, ctx):
            return '{"id": "zone-1"}'

        with patch("commerce_mcp.tools.bulk.functions._get_update_fn", return_value=fake_update_fn):
            params = BulkUpdateParams(items=[
                BulkUpdateItem(entityType="zones", data={"id": "zone-1", "version": 1, "actions": []}),
            ])
            result = await bulk_update(params, mock_api, admin_ctx)
            assert isinstance(result, str)
            json.loads(result)
