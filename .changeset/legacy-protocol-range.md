---
"@commercetools/commerce-agent": patch
---

Keep serving every 2025-era protocol revision, not just the newest.

The v2 migration set `supportedProtocolVersions` to `['2026-07-28', '2025-11-25']`. That looks equivalent to the SDK default but is not: the legacy handshake counter-offers the newest listed 2025 revision, so a client asking for `2025-06-18` was answered with `2025-11-25`, and a client that does not recognise that revision disconnects rather than downgrading.

`mcp-remote` — the bridge Claude Desktop and similar clients use to reach a remote MCP server — does exactly that, failing with `Server's protocol version is not supported: 2025-11-25`. The v1 server accepted five 2025-era revisions; the migration narrowed that to one.

The list now spreads the SDK's own `SUPPORTED_PROTOCOL_VERSIONS` alongside the 2026 revision, so `2025-11-25`, `2025-06-18`, `2025-03-26`, `2024-11-05` and `2024-10-07` each negotiate as themselves again, and the range stays current with the SDK.
