"""Shared pytest fixtures — mirrors TypeScript test/setup.ts + beforeEach patterns."""
from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock

from commerce_mcp.config import (
    AuthConfig,
    ClientCredentialsAuth,
    Configuration,
    CTContext,
    Actions,
    ResourceActions,
)
from commerce_mcp.api import CommercetoolsAPI


# ── Auth fixtures ──────────────────────────────────────────────────────────────

@pytest.fixture
def client_credentials_auth() -> ClientCredentialsAuth:
    return ClientCredentialsAuth(
        auth_url="https://auth.commercetools.com",
        api_url="https://api.commercetools.com",
        project_key="test-project",
        client_id="test-client-id",
        client_secret="test-client-secret",
    )


# ── Context fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def admin_context() -> CTContext:
    return CTContext(is_admin=True)


@pytest.fixture
def customer_context() -> CTContext:
    return CTContext(customer_id="customer-123")


@pytest.fixture
def store_context() -> CTContext:
    return CTContext(store_key="my-store")


@pytest.fixture
def bu_context() -> CTContext:
    return CTContext(customer_id="customer-123", business_unit_key="bu-key")


# ── Configuration fixtures ─────────────────────────────────────────────────────

@pytest.fixture
def all_actions() -> Actions:
    ra = ResourceActions(read=True, create=True, update=True)
    return Actions(
        products=ra,
        order=ra,
        cart=ra,
        customer=ra,
    )


@pytest.fixture
def read_only_actions() -> Actions:
    ra = ResourceActions(read=True)
    return Actions(products=ra, order=ra, cart=ra)


@pytest.fixture
def admin_config(all_actions, admin_context) -> Configuration:
    return Configuration(actions=all_actions, context=admin_context)


@pytest.fixture
def customer_config(all_actions, customer_context) -> Configuration:
    return Configuration(actions=all_actions, context=customer_context)


# ── API mock ───────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_api() -> MagicMock:
    api = MagicMock(spec=CommercetoolsAPI)
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "prod-123"}]})
    api.post = AsyncMock(return_value={"id": "prod-123", "version": 1})
    api.run = AsyncMock(return_value='{"id": "prod-123"}')
    api.close = AsyncMock()
    return api
