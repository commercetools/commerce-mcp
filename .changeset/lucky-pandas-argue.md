---
'@commercetools/commerce-mcp': patch
---

- Only require `--accessToken` for `--authType=auth_token` on the stdio transport. Remote (streamable HTTP) servers read the token from the `Authorization` header of each request, so a startup token is no longer enforced when `--remote=true`.
