from __future__ import annotations

import asyncio
from typing import Any, Callable, Awaitable
from .config import AuthConfig, ClientCredentialsAuth, ExistingTokenAuth, CTContext, Actions, ResourceActions


class CommercetoolsAPI:
    """Async Commercetools API client.

    Wraps httpx to handle auth, token management, and tool dispatch.
    Mirrors the TypeScript CommercetoolsAPI class.
    """

    def __init__(
        self,
        auth: AuthConfig,
        context: CTContext | None = None,
    ) -> None:
        self._auth = auth
        self._context = context or CTContext()
        self._access_token: str | None = None
        self._client: Any = None  # httpx.AsyncClient, imported lazily

    @classmethod
    async def create(
        cls,
        auth: AuthConfig,
        context: CTContext | None = None,
    ) -> "CommercetoolsAPI":
        instance = cls(auth, context)
        await instance._initialize()
        return instance

    async def _initialize(self) -> None:
        import httpx  # lazy import — not bundled with integrations that skip HTTP

        self._client = httpx.AsyncClient(
            headers={"User-Agent": "commerce-mcp-python/0.1.0"},
        )

        if isinstance(self._auth, ClientCredentialsAuth):
            await self._fetch_token()

    async def _fetch_token(self) -> None:
        import httpx

        auth = self._auth
        assert isinstance(auth, ClientCredentialsAuth)
        response = await self._client.post(
            f"{auth.auth_url}/oauth/token",
            data={
                "grant_type": "client_credentials",
                "scope": f"manage_project:{auth.project_key}",
            },
            auth=(auth.client_id, auth.client_secret),
        )
        response.raise_for_status()
        self._access_token = response.json()["access_token"]

    @property
    def _token(self) -> str:
        if isinstance(self._auth, ExistingTokenAuth):
            return self._auth.access_token
        if self._access_token is None:
            raise RuntimeError("CommercetoolsAPI not initialised — call await create()")
        return self._access_token

    @property
    def _base_url(self) -> str:
        return f"{self._auth.api_url}/{self._auth.project_key}"

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = await self._client.get(
            f"{self._base_url}{path}",
            params=params,
            headers={"Authorization": f"Bearer {self._token}"},
        )
        response.raise_for_status()
        return response.json()

    async def post(self, path: str, body: dict[str, Any]) -> Any:
        response = await self._client.post(
            f"{self._base_url}{path}",
            json=body,
            headers={"Authorization": f"Bearer {self._token}"},
        )
        response.raise_for_status()
        return response.json()

    async def run(
        self,
        method: str,
        params: Any,
        context: CTContext | None = None,
        handler: Callable[..., Awaitable[Any]] | None = None,
        registry: Any = None,
    ) -> Any:
        """Dispatches a tool call to either a custom handler or the function registry.

        Pass a Registry instance to use an isolated tool set instead of the global default.
        """
        ctx = context or self._context

        if handler is not None:
            return await handler(params, self, ctx)

        if registry is not None:
            handlers = registry.get_handlers()
        else:
            from .tools.registry import get_function_registry
            handlers = get_function_registry()

        fn = handlers.get(method)
        if fn is None:
            raise KeyError(f"No handler registered for tool '{method}'")
        return await fn(params, self, ctx)

    async def introspect(self) -> Actions:
        """Calls the auth introspect endpoint to derive Actions from token scopes."""
        auth = self._auth
        if not isinstance(auth, ClientCredentialsAuth):
            # Without credentials we cannot introspect — return full access
            return _full_actions()

        import httpx
        response = await self._client.post(
            f"{auth.auth_url}/oauth/introspect",
            data={"token": self._token},
            auth=(auth.client_id, auth.client_secret),
        )
        if not response.is_success:
            return _full_actions()

        body = response.json()
        scopes: list[str] = body.get("scope", "").split()
        return _scopes_to_actions(scopes, auth.project_key)

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()


# ── Scope → Actions mapping ────────────────────────────────────────────────────

def _full_actions() -> Actions:
    ra = ResourceActions(read=True, create=True, update=True)
    fields: dict[str, Any] = {}
    for name, field in Actions.model_fields.items():
        alias = field.alias or name
        fields[alias] = ra
    return Actions(**fields)


def _scopes_to_actions(scopes: list[str], project_key: str) -> Actions:
    """Maps Commercetools OAuth scopes to the Actions permission matrix.

    Scope format: manage_products:<projectKey> → products.{read,create,update}
                  view_products:<projectKey>   → products.read
    """
    _MANAGE_TO_NAMESPACE = {
        "manage_products": "products",
        "manage_orders": "order",
        "manage_customers": "customer",
        "manage_my_orders": "order",
        "manage_shopping_lists": "shopping-lists",
        "manage_payments": "payments",
        "manage_project": None,  # full access
    }
    _VIEW_TO_NAMESPACE = {
        "view_products": "products",
        "view_orders": "order",
        "view_customers": "customer",
        "view_shopping_lists": "shopping-lists",
        "view_payments": "payments",
    }

    namespace_perms: dict[str, ResourceActions] = {}
    full_access = False

    for scope in scopes:
        parts = scope.split(":")
        name = parts[0]
        pk = parts[1] if len(parts) > 1 else None

        if pk and pk != project_key:
            continue

        if name == "manage_project":
            full_access = True
            break

        if name in _MANAGE_TO_NAMESPACE:
            ns = _MANAGE_TO_NAMESPACE[name]
            if ns:
                namespace_perms[ns] = ResourceActions(read=True, create=True, update=True)
        elif name in _VIEW_TO_NAMESPACE:
            ns = _VIEW_TO_NAMESPACE[name]
            existing = namespace_perms.get(ns, ResourceActions())
            namespace_perms[ns] = existing.model_copy(update={"read": True})

    if full_access:
        return _full_actions()

    fields: dict[str, Any] = {}
    for field_name, field in Actions.model_fields.items():
        alias = field.alias or field_name
        fields[alias] = namespace_perms.get(alias)
    return Actions(**fields)
