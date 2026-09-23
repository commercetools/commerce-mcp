---
"@commercetools/commerce-agent": minor
"@commercetools/commerce-mcp": minor
---

Serve both protocol eras from the v2 SDK handler (DEVX-886).

`StreamableHTTPServerTransport` and its session map are replaced by `createMcpHandler` plus the SDK's Node adapter, and the CLI's stdio transport moves to `@modelcontextprotocol/server/stdio`. The handler builds a server per request from that request's credentials, which is what the previous `getServer` already did, so per-caller auth is unchanged.

`legacy: 'stateless'` keeps existing clients working: a 2025-era `initialize` still negotiates (against `2025-11-25`), while `server/discover` answers `2026-07-28` on the modern path. Tool registration now goes through the zod → JSON Schema bridge added in DEVX-883, so `tools/list` emits real JSON Schema alongside the titles and annotations from DEVX-885, and is marked cacheable for modern clients.

Two behaviour changes to know about:

- **`GET /mcp` now returns 405 instead of 401.** The 2026-07-28 spec removed the GET endpoint, and a GET carries no credentials to protect. `Host`/`Origin` validation still runs first, so DNS-rebinding protection is unaffected.
- **Protocol sessions are gone**, as flagged in DEVX-888. `Mcp-Session-Id` is no longer issued or accepted, and the session-to-opener binding it required is removed with it. Per-request credentials already provided that guarantee.

`streamableHttpOptions` is now inert and deprecated; it is still accepted so existing callers typecheck. The stale `@modelcontextprotocol/sdk` v1 peer dependency is dropped — the v2 packages ship as regular dependencies, so consumers no longer need to install the SDK themselves.
