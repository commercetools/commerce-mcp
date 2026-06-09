---
"@commercetools/commerce-agent": minor
"@commercetools/commerce-mcp": minor
---

fix(security): require Authorization header for the streamable HTTP server (DEVX-806 / COM-15-004)

The remote/streamable HTTP MCP server no longer falls back to the credentials
provided at startup when an incoming request omits the `Authorization` header.
Previously an unauthenticated network caller could be served using the server's
own configured token.

### What changed

- Every request to `/mcp` must now include a valid
  `Authorization: Bearer <token>` header; missing or malformed headers are
  rejected with `401 Unauthorized` before any commercetools call is made.
- The caller's bearer token is forwarded directly to the commercetools API
  (`auth_token` flow). This also fixes a latent bug where a server started with
  `client_credentials` silently ignored the per-request header token.
- The handler no longer mutates the shared `authConfig`; each request builds an
  isolated per-request auth config.
- Added an `enforceAuthHeader` option (defaults to `true`) to opt out of the
  check. It is available as the `CommercetoolsCommerceAgentStreamable`
  constructor option, the `--enforceAuthHeader` CLI argument, and the
  `ENFORCE_AUTH_HEADER` environment variable. When disabled in remote mode the
  server logs a startup warning, since unauthenticated requests then fall back
  to the startup credentials. Only use it behind your own authentication layer.

### Migration

Clients connecting to a remote server (e.g. via `mcp-remote`) must now send an
`Authorization: Bearer <commercetools-access-token>` header on every request.
The startup credentials are no longer used to serve network requests.

Existing deployments that cannot add the header immediately can set
`ENFORCE_AUTH_HEADER=false` (or `--enforceAuthHeader=false`) to temporarily
restore the previous behavior while migrating. This is a transitional escape
hatch and is not recommended for network-exposed servers.
