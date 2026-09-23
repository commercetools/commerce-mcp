---
"@commercetools/commerce-agent": patch
---

Use the SDK's `validateHostHeader` for DNS-rebinding protection (DEVX-887).

Our hand-rolled `Host` parser is replaced by the validator shipped in `@modelcontextprotocol/server`, which has the same port-agnostic hostname-allowlist semantics, including bracketed IPv6. The `*` wildcard, the `--allowedHosts` surface and the existing 403 messages are unchanged, so the PLASE-3987 regression tests pass untouched.

`Origin` checking deliberately keeps our own comparison. The SDK's `validateOriginHeader` matches on hostname only, so a configured `https://app.example.com` would start accepting `http://app.example.com` and any port. Our `--allowedOrigins` values are full origins and are still compared as full origins.
