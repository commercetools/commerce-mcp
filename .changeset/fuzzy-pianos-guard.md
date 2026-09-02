---
'@commercetools/commerce-agent': patch
---

Harden the streamable HTTP server against cross-caller credential sharing (Cure53 COM-15-010). The shared startup `authConfig` is now a frozen copy that cannot be written to after construction, and in stateful mode a session records the bearer token it was opened with: continuing a session with a different token — or with the header dropped — is rejected with `403` instead of reusing the opener's credentials. Stateless mode and sessions opened without a token are unaffected.
