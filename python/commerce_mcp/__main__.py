"""CLI entry point for the commerce-mcp Python server.

Usage:
  # stdio (MCP clients like Claude Desktop, Claude Code)
  commerce-mcp --transport stdio --tools all

  # Streamable HTTP
  commerce-mcp --transport http --port 8000 --tools products.read,orders.read

  # Auto-derive permissions from the OAuth token's scopes
  commerce-mcp --transport stdio --tools introspect

Environment variables (mirror TypeScript server.json):
  Required:
    AUTH_URL, API_URL, PROJECT_KEY
    CLIENT_ID + CLIENT_SECRET  OR  ACCESS_TOKEN
  Optional:
    TOOLS                  (default: all)
    IS_ADMIN               (default: false)
    CUSTOMER_ID
    STORE_KEY
    BUSINESS_UNIT_KEY
    DYNAMIC_TOOL_LOADING_THRESHOLD  (default: 30)
    LOGGING                (default: false)
"""
from __future__ import annotations

import argparse
import os
import sys

from .config import (
    AuthConfig,
    ClientCredentialsAuth,
    ExistingTokenAuth,
    Configuration,
    CTContext,
    Actions,
    ResourceActions,
)
from .server import build_server


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def _env_bool(key: str) -> bool:
    return _env(key).lower() in ("1", "true", "yes")


def _parse_tools(tools_str: str) -> Actions | None:
    """Converts a tools string like 'all', 'all.read', 'products.read,orders.create'
    into an Actions object.  Returns None (= no restriction) for 'all'.
    """
    if tools_str in ("all", "*"):
        return None  # unrestricted — everything enabled

    if tools_str == "all.read":
        ra = ResourceActions(read=True)
        fields: dict = {}
        for name, field in Actions.model_fields.items():
            fields[field.alias or name] = ra
        return Actions(**fields)

    # Comma-separated: "products.read,orders.create,cart.update"
    actions_kwargs: dict[str, ResourceActions] = {}
    for part in tools_str.split(","):
        part = part.strip()
        if "." in part:
            ns, perm = part.rsplit(".", 1)
        else:
            ns, perm = part, "read"

        existing = actions_kwargs.get(ns, ResourceActions())
        update = {perm: True}
        actions_kwargs[ns] = existing.model_copy(update=update)

    return Actions(**{k: v for k, v in actions_kwargs.items()})


def _build_auth() -> AuthConfig:
    auth_url = _env("AUTH_URL")
    api_url = _env("API_URL")
    project_key = _env("PROJECT_KEY")

    if not (auth_url and api_url and project_key):
        print(
            "ERROR: AUTH_URL, API_URL, and PROJECT_KEY are required",
            file=sys.stderr,
        )
        sys.exit(1)

    access_token = _env("ACCESS_TOKEN")
    if access_token:
        return ExistingTokenAuth(
            auth_url=auth_url,
            api_url=api_url,
            project_key=project_key,
            access_token=access_token,
            client_id=_env("CLIENT_ID") or None,
            client_secret=_env("CLIENT_SECRET") or None,
        )

    client_id = _env("CLIENT_ID")
    client_secret = _env("CLIENT_SECRET")
    if not (client_id and client_secret):
        print(
            "ERROR: Either ACCESS_TOKEN or CLIENT_ID + CLIENT_SECRET must be set",
            file=sys.stderr,
        )
        sys.exit(1)

    return ClientCredentialsAuth(
        auth_url=auth_url,
        api_url=api_url,
        project_key=project_key,
        client_id=client_id,
        client_secret=client_secret,
    )


def _build_config(tools_str: str) -> Configuration:
    actions = _parse_tools(tools_str)
    context = CTContext(
        is_admin=_env_bool("IS_ADMIN"),
        customer_id=_env("CUSTOMER_ID") or None,
        store_key=_env("STORE_KEY") or None,
        business_unit_key=_env("BUSINESS_UNIT_KEY") or None,
        logging=_env_bool("LOGGING"),
        dynamic_tool_loading_threshold=int(_env("DYNAMIC_TOOL_LOADING_THRESHOLD", "30")),
    )
    return Configuration(actions=actions, context=context)


async def _introspect_actions(auth: AuthConfig) -> Actions:
    from .api import CommercetoolsAPI
    api = await CommercetoolsAPI.create(auth)
    try:
        return await api.introspect()
    finally:
        await api.close()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Commercetools MCP server (Python/fastMCP)")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default=_env("TRANSPORT", "stdio"),
        help="MCP transport: stdio (default) or http (streamable HTTP)",
    )
    parser.add_argument(
        "--host",
        default=_env("HOST", "0.0.0.0"),
        help="Host for HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(_env("PORT", "8000")),
        help="Port for HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--tools",
        default=_env("TOOLS", "all"),
        help=(
            'Tool selection: "all", "all.read", "products.read,orders.create", '
            'or "introspect" to derive permissions from OAuth token scopes'
        ),
    )

    args = parser.parse_args(argv)
    auth = _build_auth()

    if args.tools == "introspect":
        import asyncio
        actions = asyncio.run(_introspect_actions(auth))
        config = _build_config("all").model_copy(update={"actions": actions})
    else:
        config = _build_config(args.tools)

    server = build_server(auth, config)

    if args.transport == "stdio":
        server.run(transport="stdio")
    else:
        server.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
        )


if __name__ == "__main__":
    main()
