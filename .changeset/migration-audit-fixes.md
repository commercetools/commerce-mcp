---
"@commercetools/commerce-agent": patch
"@commercetools/commerce-mcp": patch
---

Fix inconsistencies left by the SDK v2 migration.

- `context.mode` reported `'stateful'` whenever `--stateless=false` was set, but the 2026-07-28 handler has no sessions and always serves statelessly. Tools and the request log were being told a mode the server never serves. It now reports what actually happens.
- `server.json` advertised the streamable HTTP endpoint as `http://{HOST}:{PORT}/mcp` without declaring either variable, so a registry had nothing to substitute. Both are real environment variables the CLI reads, and are now declared.
- The CLI still passed `streamableHttpOptions`, which became inert when the transport moved to `createMcpHandler`, and the README's SDK examples still showed it alongside `stateless: false`. Both removed, so the documented setup matches what the options now do.

Also restores a regression test lost in the transport rewrite: the route used to catch errors and answer 500 itself, and that responsibility moved to the SDK adapter. A test now asserts a failed per-request server build still surfaces as an error rather than leaving the request unanswered.
