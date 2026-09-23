---
"@commercetools/commerce-mcp": patch
---

Deprecate stateful session mode (DEVX-888). The 2026-07-28 MCP specification removes protocol sessions and the `Mcp-Session-Id` header, so `--stateless=false` has no equivalent in the new protocol.

An audit of the current implementation found nothing carried between calls except the transport instance and the fingerprint that binds a session to the token it was opened with. Per-request credentials already cover that, so no functionality is lost by moving to stateless.

Behaviour is unchanged: the remote server still defaults to stateful, and the flag still works. Starting it in stateful mode now prints a deprecation notice. Pass `--stateless=true` to adopt the future default, which is what the v2 handler will serve.
