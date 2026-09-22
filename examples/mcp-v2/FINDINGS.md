# SDK v2 dual-era findings (DEVX-881)

**Verdict: go.** `@modelcontextprotocol/server@2` serves the 2026-07-28 spec and
today's clients from one endpoint, so the migration can land incrementally
without a flag day for existing users.

Reproduce with `npm install && npm run probe` in this directory (11 automated
protocol checks). The last three rows below exercise Express middleware rather
than the handler, so they need a real socket and are manual `curl` checks —
see [`README.md`](./README.md). All 14 were observed passing.

## Acceptance matrix

| Check | Result |
| --- | --- |
| `server/discover` advertises `2026-07-28` | `["2026-07-28"]` |
| `tools/list` carries `title`, JSON Schema, `annotations` | `read_carts`, `readOnlyHint=true` |
| `tools/list` is a `CacheableResult` (SEP-2549) | `ttlMs=60000`, `cacheScope=public` |
| Results carry `resultType` (SEP-2322) | `complete` |
| `tools/call` returns `structuredContent` | `{"results":[],"total":0,"limit":3,"offset":0}` |
| Per-request auth reaches the tool | token visible in handler |
| Unknown protocol version | `-32022 UnsupportedProtocolVersion` |
| Missing `Mcp-Method` header | `-32020 HeaderMismatch` |
| **Legacy `initialize`** | negotiates `2025-11-25` |
| **Legacy `tools/call`** with no `_meta` envelope | served |
| `GET /mcp` | `405` |
| Missing bearer token *(manual)* | `401` |
| Foreign `Host`, DNS rebinding *(manual)* | `403` |
| Own `Host` *(manual)* | served |

## What this tells us about the implementation

**The modern era is opt-in.** `LATEST_PROTOCOL_VERSION` in v2 is still
`2025-11-25` and `SUPPORTED_PROTOCOL_VERSIONS` is the legacy list. You get
2026-07-28 only by passing `supportedProtocolVersions: ['2026-07-28', …]`;
internally the SDK splits eras at `FIRST_MODERN_PROTOCOL_VERSION = '2026-07-28'`.
Without the option, `server/discover` is not even registered.

**`fromJsonSchema` removes the zod-4 blocker (DEVX-883).** Tools register from
raw JSON Schema and arguments validate, so `@commercetools/tools-core`'s zod-3
schemas need converting, not upgrading.

**`createMcpHandler`'s per-request factory maps onto our `getServer`.** The
factory receives `ctx.authInfo`, which the handler treats as strict
pass-through — it never reads headers or verifies tokens itself. Our bearer
handling, and the per-caller `authConfig` from PLASE-3988, carry over unchanged.

**Route every method to the handler, not just POST.** With only `app.post`
registered, `GET /mcp` returned Express's `404` instead of the spec's `405`.
`app.all('/mcp', …)` fixes it.

**Modern requests are strict.** Two rejections to expect in client integrations:
the `_meta` envelope needs `protocolVersion` *and* `clientCapabilities`
(`-32602`), and POSTs need `Mcp-Method` / `Mcp-Name` headers matching the body
(`-32020`). Both are the client's job, but our tests need to send them.

**`@modelcontextprotocol/express` already covers PLASE-3986/3987.**
`createMcpExpressApp({host, allowedHosts})` applies DNS-rebinding protection for
loopback hosts automatically, and `hostHeaderValidation()` / `originValidation()`
are exported — so DEVX-887 is a deletion, not a rewrite.

## Do not hand-roll the Express bridge

The first cut of this example converted the Node request to a web `Request`,
called `handler.fetch`, then wrote the body back with `res.send()`. SAST
flagged it — correctly: that shape runs client input through our own response
write, and it also meant hand-managing header forwarding and SSE backpressure.

`@modelcontextprotocol/node` already ships the bridge:

```js
import {toNodeHandler} from '@modelcontextprotocol/node';

const mcp = toNodeHandler(handler, {onerror});
app.all('/mcp', (req, res) => {
  req.auth = {token, clientId, scopes};   // the adapter's hand-off to authInfo
  return mcp(req, res, req.body);          // SDK owns the response write
});
```

It converts the request, calls the handler, honours SSE write backpressure,
forwards `req.auth` as the handler's pass-through `authInfo`, and ignores
Express's `next`. **DEVX-886 should use this rather than porting our current
manual transport plumbing.** `createMcpExpressApp({jsonLimit})` bounds the
request body.

## Costs confirmed

- **ESM + Node 20** (DEVX-882) is unavoidable: the v2 packages are
  `"type": "module"` with `engines.node >= 20`.
- **Legacy serving is free**: `legacy: 'stateless'` is the default. GET/DELETE
  (the 2025 session operations) answer `405`, which is why DEVX-888 must decide
  the fate of `--stateless=false` before we cut over.
