import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import ContextError, SDKError
from commerce_mcp.tools.reviews.functions import create_review, read_review, update_review
from commerce_mcp.tools.reviews.schemas import (
    CreateReviewParams,
    ReadReviewParams,
    ReviewUpdateAction,
    UpdateReviewParams,
)


@pytest.fixture
def admin_ctx() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"id": "rev-1", "rating": 80})
    api.post = AsyncMock(return_value={"id": "rev-1", "version": 2})
    return api


class TestReadReview:
    @pytest.mark.asyncio
    async def test_read_by_id(self, mock_api, admin_ctx):
        result = await read_review(ReadReviewParams(id="rev-1"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/reviews/rev-1", params=None)
        assert json.loads(result)["id"] == "rev-1"

    @pytest.mark.asyncio
    async def test_read_by_key(self, mock_api, admin_ctx):
        await read_review(ReadReviewParams(key="my-review"), mock_api, admin_ctx)
        mock_api.get.assert_called_once_with("/reviews/key=my-review", params=None)

    @pytest.mark.asyncio
    async def test_list_reviews(self, mock_api, admin_ctx):
        mock_api.get.return_value = {"results": [], "total": 0}
        await read_review(ReadReviewParams(where=["rating > 50"]), mock_api, admin_ctx)
        call_params = mock_api.get.call_args[1]["params"]
        assert call_params["where"] == ["rating > 50"]

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="read_review"):
            await read_review(ReadReviewParams(), mock_api, CTContext())
        mock_api.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.get.side_effect = Exception("error")
        with pytest.raises(SDKError, match="read review"):
            await read_review(ReadReviewParams(id="rev-1"), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await read_review(ReadReviewParams(id="rev-1"), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)


class TestCreateReview:
    @pytest.mark.asyncio
    async def test_create(self, mock_api, admin_ctx):
        params = CreateReviewParams(rating=90, title="Great product")
        result = await create_review(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["rating"] == 90
        assert body["title"] == "Great product"
        assert json.loads(result)["id"] == "rev-1"

    @pytest.mark.asyncio
    async def test_create_excludes_none_fields(self, mock_api, admin_ctx):
        await create_review(CreateReviewParams(rating=50), mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert "title" not in body
        assert "text" not in body

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        with pytest.raises(ContextError, match="create_review"):
            await create_review(CreateReviewParams(rating=50), mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError, match="create review"):
            await create_review(CreateReviewParams(rating=50), mock_api, admin_ctx)


class TestUpdateReview:
    @pytest.mark.asyncio
    async def test_update_by_id(self, mock_api, admin_ctx):
        params = UpdateReviewParams(id="rev-1", version=1, actions=[ReviewUpdateAction(action="setRating", rating=100)])
        result = await update_review(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/reviews/rev-1"
        assert json.loads(result)["version"] == 2

    @pytest.mark.asyncio
    async def test_update_by_key(self, mock_api, admin_ctx):
        params = UpdateReviewParams(key="my-review", version=1, actions=[ReviewUpdateAction(action="setTitle", title="New")])
        await update_review(params, mock_api, admin_ctx)
        assert mock_api.post.call_args[0][0] == "/reviews/key=my-review"

    @pytest.mark.asyncio
    async def test_raises_context_error_without_admin(self, mock_api):
        params = UpdateReviewParams(id="rev-1", version=1, actions=[ReviewUpdateAction(action="setRating")])
        with pytest.raises(ContextError, match="update_review"):
            await update_review(params, mock_api, CTContext())
        mock_api.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_raises_sdk_error_without_id_or_key(self, mock_api, admin_ctx):
        params = UpdateReviewParams(version=1, actions=[ReviewUpdateAction(action="setRating")])
        with pytest.raises(SDKError):
            await update_review(params, mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("conflict")
        params = UpdateReviewParams(id="rev-1", version=1, actions=[ReviewUpdateAction(action="setRating")])
        with pytest.raises(SDKError, match="update review"):
            await update_review(params, mock_api, admin_ctx)
