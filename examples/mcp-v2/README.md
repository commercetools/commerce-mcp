# MCP SDK v2 server — runnable example

A minimal `commerce-mcp`-shaped server built on `@modelcontextprotocol/server@2`,
serving both the [2026-07-28 spec](https://modelcontextprotocol.io/specification/2026-07-28)
and today's clients from a single `/mcp` endpoint.

It mirrors how the real server is wired — our own Express app, a per-request
server instance carrying the caller's credentials, a mandatory bearer token —
so it doubles as the reference for the migration work tracked under DEVX-880.

Deliberately **outside the pnpm workspace**, with its own `package.json`: the
v2 packages are ESM-only and Node 20+, so keeping them here means the example
can use them while the published packages are still on SDK v1.

```bash
npm install
npm run probe    # protocol matrix, 11 checks, exits non-zero on failure
npm run serve    # the server on 127.0.0.1:8899, for the manual checks below
```

The probe drives the MCP handler directly with web-standard `Request`
objects, so it needs no HTTP client. The three guarantees that live in Express
middleware rather than in the handler need a real socket, so they are manual —
run `npm run serve`, then:

```bash
# bearer token required
curl -so /dev/null -w '%{http_code}\n' -XPOST 127.0.0.1:8899/mcp \
  -H 'content-type: application/json' -d '{}'                        # 401

# DNS rebinding: a foreign Host is refused, our own is served
curl -so /dev/null -w '%{http_code}\n' -XPOST 127.0.0.1:8899/mcp \
  -H 'host: xxx.attacker.com' -H 'authorization: Bearer t' \
  -H 'content-type: application/json' -d '{}'                        # 403
curl -so /dev/null -w '%{http_code}\n' -XPOST 127.0.0.1:8899/mcp \
  -H 'authorization: Bearer t' \
  -H 'content-type: application/json' -d '{}'                        # 400 (past the guards)
```

What this told us about the migration: [`FINDINGS.md`](./FINDINGS.md).
