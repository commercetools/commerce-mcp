---
"@commercetools/commerce-mcp": patch
---

Refresh the `server.json` manifest and document protocol compatibility (DEVX-889).

The manifest declared `version: "1.0.0"` while the package was at 4.x, and advertised only the stdio transport — the streamable HTTP server was not listed at all. Both are fixed, and the manifest validates against the published registry schema.

The README gains a compatibility matrix: which spec revisions are served (`2026-07-28` and `2025-11-25`), the available transports, the Node 20 floor, and the two behavioural consequences of the 2026 revision — no protocol sessions, and stricter headers on modern requests. The section describing session-to-opener binding is corrected, since sessions no longer exist.

Note the `$schema` date is unchanged: `2025-10-17` is still the only published registry schema, and it is independent of the MCP protocol revision.
