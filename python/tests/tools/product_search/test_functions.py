import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import SDKError
from commerce_mcp.tools.product_search.functions import search_products
from commerce_mcp.tools.product_search.schemas import SearchProductsParams, SortItem


@pytest.fixture
def admin_ctx():
    return CTContext(is_admin=True)


@pytest.fixture
def customer_ctx():
    return CTContext(customer_id="customer-1")


@pytest.fixture
def mock_api():
    api = MagicMock()
    api.post = AsyncMock(return_value={"total": 10, "results": [{"id": "prod-1"}]})
    return api


def make_search_params():
    return SearchProductsParams(query={"fullText": {"field": "name", "language": "en", "value": "shirt"}})


class TestSearchProducts:
    @pytest.mark.asyncio
    async def test_search_posts_to_correct_endpoint(self, mock_api, admin_ctx):
        result = await search_products(make_search_params(), mock_api, admin_ctx)
        call_args = mock_api.post.call_args
        assert call_args[0][0] == "/products/search"
        body = call_args[1]["body"]
        assert "query" in body

    @pytest.mark.asyncio
    async def test_search_passes_query(self, mock_api, admin_ctx):
        params = SearchProductsParams(query={"fullText": {"field": "name", "language": "en", "value": "shirt"}})
        await search_products(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["query"]["fullText"]["value"] == "shirt"

    @pytest.mark.asyncio
    async def test_search_with_pagination(self, mock_api, admin_ctx):
        params = SearchProductsParams(query={}, limit=10, offset=20)
        await search_products(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["limit"] == 10
        assert body["offset"] == 20

    @pytest.mark.asyncio
    async def test_search_with_sort(self, mock_api, admin_ctx):
        params = SearchProductsParams(
            query={},
            sort=[SortItem(field="name", order="asc")],
        )
        await search_products(params, mock_api, admin_ctx)
        body = mock_api.post.call_args[1]["body"]
        assert body["sort"][0]["field"] == "name"
        assert body["sort"][0]["order"] == "asc"

    @pytest.mark.asyncio
    async def test_search_available_to_admin(self, mock_api, admin_ctx):
        result = await search_products(make_search_params(), mock_api, admin_ctx)
        assert json.loads(result)["total"] == 10

    @pytest.mark.asyncio
    async def test_search_available_to_customer(self, mock_api, customer_ctx):
        result = await search_products(make_search_params(), mock_api, customer_ctx)
        assert json.loads(result)["total"] == 10

    @pytest.mark.asyncio
    async def test_search_available_without_context(self, mock_api):
        result = await search_products(make_search_params(), mock_api, CTContext())
        assert json.loads(result)["total"] == 10

    @pytest.mark.asyncio
    async def test_wraps_api_error(self, mock_api, admin_ctx):
        mock_api.post.side_effect = Exception("error")
        with pytest.raises(SDKError):
            await search_products(make_search_params(), mock_api, admin_ctx)

    @pytest.mark.asyncio
    async def test_output_is_json_string(self, mock_api, admin_ctx):
        result = await search_products(make_search_params(), mock_api, admin_ctx)
        assert isinstance(result, str)
        json.loads(result)
