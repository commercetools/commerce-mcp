---
'@commercetools/commerce-agent': minor
'@commercetools/commerce-mcp': minor
---

Bind the remote (streamable HTTP) server to `127.0.0.1` by default instead of every network interface (Cure53 COM-15-005). A new `--host` option (or `HOST` environment variable) opts into a wider binding, and the server warns at startup whenever it is bound beyond loopback.

This changes the default reachability of `--remote=true` servers: deployments that rely on the server accepting connections from other hosts — containers with published ports, Kubernetes pods, anything behind a reverse proxy on another machine — must now pass `--host=0.0.0.0` explicitly. `CommercetoolsCommerceAgentStreamable.listen()` takes an optional host as its second argument and still accepts the `(port, callback)` form.
