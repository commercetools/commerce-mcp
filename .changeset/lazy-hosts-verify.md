---
'@commercetools/commerce-agent': minor
'@commercetools/commerce-mcp': minor
---

Validate the `Host` and `Origin` headers on the remote (streamable HTTP) server (Cure53 COM-15-006). Requests addressed to an unrecognised hostname are rejected with `403`, which is what closes the DNS rebinding path: a malicious page can rebind its hostname to `127.0.0.1` and stays same-origin as far as the browser is concerned, but the `Host` header still names the attacker's domain. Requests that carry an `Origin` header must match an allow-list too; requests without one (every non-browser MCP client) are unaffected, and no permissive CORS header is ever sent.

Hostnames default to `localhost`, `127.0.0.1`, `[::1]` plus the resolved `--host`, so a server serving a real domain now needs `--allowedHosts=mcp.example.com` (or `ALLOWED_HOSTS`). Browser origins are opted in with `--allowedOrigins`/`ALLOWED_ORIGINS`. Both accept `*` to disable the check, and both are available as `allowedHosts`/`allowedOrigins` on `CommercetoolsCommerceAgentStreamable`.
