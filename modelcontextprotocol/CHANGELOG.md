# @commercetools/commerce-mcp

## 4.2.0

### Minor Changes

- [#59](https://github.com/commercetools/commerce-mcp/pull/59) [`49a315f`](https://github.com/commercetools/commerce-mcp/commit/49a315fcfd5ccd3b9cdcdcbfbeaec007f6f7bc64) Thanks [@ajimae](https://github.com/ajimae)! - Require Node.js 20 or newer, and publish the MCP CLI as an ES module. Groundwork for the MCP SDK v2 migration (DEVX-882): the v2 packages are ESM-only and declare `engines.node >= 20`.

  The executable moves from `dist/index.js` to `dist/cli.js` — a thin bin shim, so `index.js` stays importable without starting a server as a side effect. Anyone invoking the package through `npx @commercetools/commerce-mcp` or the `bin` entry is unaffected; only a direct `node .../dist/index.js` invocation needs updating.

  Three changes here can break an existing setup, so check them before upgrading:

  - **Node 18 is no longer supported.** Install fails on `engines.node` unless you are on Node 20 or newer.
  - **CommonJS consumers cannot `require()` these packages.** The published output is ESM only; use a dynamic `import()` or move the consuming code to ESM.
  - **`node .../dist/index.js` no longer starts a server.** It now only exports `main()`. Call `dist/cli.js` instead.

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Serve both protocol eras from the v2 SDK handler (DEVX-886).

  `StreamableHTTPServerTransport` and its session map are replaced by `createMcpHandler` plus the SDK's Node adapter, and the CLI's stdio transport moves to `@modelcontextprotocol/server/stdio`. The handler builds a server per request from that request's credentials, which is what the previous `getServer` already did, so per-caller auth is unchanged.

  `legacy: 'stateless'` keeps existing clients working: a 2025-era `initialize` still negotiates (against `2025-11-25`), while `server/discover` answers `2026-07-28` on the modern path. Tool registration now goes through the zod → JSON Schema bridge added in DEVX-883, so `tools/list` emits real JSON Schema alongside the titles and annotations from DEVX-885, and is marked cacheable for modern clients.

  Two behaviour changes to know about:

  - **`GET /mcp` now returns 405 instead of 401.** The 2026-07-28 spec removed the GET endpoint, and a GET carries no credentials to protect. `Host`/`Origin` validation still runs first, so DNS-rebinding protection is unaffected.
  - **Protocol sessions are gone**, as flagged in DEVX-888. `Mcp-Session-Id` is no longer issued or accepted, and the session-to-opener binding it required is removed with it. Per-request credentials already provided that guarantee.

  `streamableHttpOptions` is now inert and deprecated; it is still accepted so existing callers typecheck. The stale `@modelcontextprotocol/sdk` v1 peer dependency is dropped — the v2 packages ship as regular dependencies, so consumers no longer need to install the SDK themselves.

### Patch Changes

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Refresh the `server.json` manifest and document protocol compatibility (DEVX-889).

  The manifest declared `version: "1.0.0"` while the package was at 4.x, and advertised only the stdio transport — the streamable HTTP server was not listed at all. Both are fixed, and the manifest validates against the published registry schema.

  The README gains a compatibility matrix: which spec revisions are served (`2026-07-28` and `2025-11-25`), the available transports, the Node 20 floor, and the two behavioural consequences of the 2026 revision — no protocol sessions, and stricter headers on modern requests. The section describing session-to-opener binding is corrected, since sessions no longer exist.

  Note the `$schema` date is unchanged: `2025-10-17` is still the only published registry schema, and it is independent of the MCP protocol revision.

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Fix inconsistencies left by the SDK v2 migration.

  - `context.mode` reported `'stateful'` whenever `--stateless=false` was set, but the 2026-07-28 handler has no sessions and always serves statelessly. Tools and the request log were being told a mode the server never serves. It now reports what actually happens.
  - `server.json` advertised the streamable HTTP endpoint as `http://{HOST}:{PORT}/mcp` without declaring either variable, so a registry had nothing to substitute. Both are real environment variables the CLI reads, and are now declared.
  - The CLI still passed `streamableHttpOptions`, which became inert when the transport moved to `createMcpHandler`, and the README's SDK examples still showed it alongside `stateless: false`. Both removed, so the documented setup matches what the options now do.

  Also restores a regression test lost in the transport rewrite: the route used to catch errors and answer 500 itself, and that responsibility moved to the SDK adapter. A test now asserts a failed per-request server build still surfaces as an error rather than leaving the request unanswered.

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Deprecate stateful session mode (DEVX-888). The 2026-07-28 MCP specification removes protocol sessions and the `Mcp-Session-Id` header, so `--stateless=false` has no equivalent in the new protocol.

  An audit of the current implementation found nothing carried between calls except the transport instance and the fingerprint that binds a session to the token it was opened with. Per-request credentials already cover that, so no functionality is lost by moving to stateless.

  Behaviour is unchanged: the remote server still defaults to stateful, and the flag still works. Starting it in stateful mode now prints a deprecation notice. Pass `--stateless=true` to adopt the future default, which is what the v2 handler will serve.

- Updated dependencies [[`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416), [`70f5b6e`](https://github.com/commercetools/commerce-mcp/commit/70f5b6e0e2d8c670365b8b7e8becaecb9dc2d1f7), [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416), [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416), [`49a315f`](https://github.com/commercetools/commerce-mcp/commit/49a315fcfd5ccd3b9cdcdcbfbeaec007f6f7bc64), [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416), [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416), [`43e6264`](https://github.com/commercetools/commerce-mcp/commit/43e62641daf0f114845977af13859c494c5ed140), [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416), [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416), [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416)]:
  - @commercetools/commerce-agent@4.2.0
  - @commercetools/processors@0.1.0

## 4.1.0

### Minor Changes

- [#53](https://github.com/commercetools/commerce-mcp/pull/53) [`28f7d9e`](https://github.com/commercetools/commerce-mcp/commit/28f7d9e70e1e898149f3dae74b68037c4d15a331) Thanks [@ajimae](https://github.com/ajimae)! - Validate the `Host` and `Origin` headers on the remote (streamable HTTP) server (Cure53 COM-15-006). Requests addressed to an unrecognised hostname are rejected with `403`, which is what closes the DNS rebinding path: a malicious page can rebind its hostname to `127.0.0.1` and stays same-origin as far as the browser is concerned, but the `Host` header still names the attacker's domain. Requests that carry an `Origin` header must match an allow-list too; requests without one (every non-browser MCP client) are unaffected, and no permissive CORS header is ever sent.

  Hostnames default to `localhost`, `127.0.0.1`, `[::1]` plus the resolved `--host`, so a server serving a real domain now needs `--allowedHosts=mcp.example.com` (or `ALLOWED_HOSTS`). Browser origins are opted in with `--allowedOrigins`/`ALLOWED_ORIGINS`. Both accept `*` to disable the check, and both are available as `allowedHosts`/`allowedOrigins` on `CommercetoolsCommerceAgentStreamable`.

- [#53](https://github.com/commercetools/commerce-mcp/pull/53) [`28f7d9e`](https://github.com/commercetools/commerce-mcp/commit/28f7d9e70e1e898149f3dae74b68037c4d15a331) Thanks [@ajimae](https://github.com/ajimae)! - Bind the remote (streamable HTTP) server to `127.0.0.1` by default instead of every network interface (Cure53 COM-15-005). A new `--host` option (or `HOST` environment variable) opts into a wider binding, and the server warns at startup whenever it is bound beyond loopback.

  This changes the default reachability of `--remote=true` servers: deployments that rely on the server accepting connections from other hosts — containers with published ports, Kubernetes pods, anything behind a reverse proxy on another machine — must now pass `--host=0.0.0.0` explicitly. `CommercetoolsCommerceAgentStreamable.listen()` takes an optional host as its second argument, still accepts the `(port, callback)` form, and now returns the underlying server so a bind failure can be observed. `--host=*` is normalised to `0.0.0.0` (Node cannot bind the literal `*`), and a failed bind is reported as `Unable to bind <host>:<port>` instead of exiting silently after logging a misleading "listening" line.

### Patch Changes

- [#53](https://github.com/commercetools/commerce-mcp/pull/53) [`28f7d9e`](https://github.com/commercetools/commerce-mcp/commit/28f7d9e70e1e898149f3dae74b68037c4d15a331) Thanks [@ajimae](https://github.com/ajimae)! - - Only require `--accessToken` for `--authType=auth_token` on the stdio transport. Remote (streamable HTTP) servers read the token from the `Authorization` header of each request, so a startup token is no longer enforced when `--remote=true`.

- Updated dependencies [[`28f7d9e`](https://github.com/commercetools/commerce-mcp/commit/28f7d9e70e1e898149f3dae74b68037c4d15a331), [`28f7d9e`](https://github.com/commercetools/commerce-mcp/commit/28f7d9e70e1e898149f3dae74b68037c4d15a331), [`28f7d9e`](https://github.com/commercetools/commerce-mcp/commit/28f7d9e70e1e898149f3dae74b68037c4d15a331)]:
  - @commercetools/commerce-agent@4.1.0

## 4.0.0

### Major Changes

- [#51](https://github.com/commercetools/commerce-mcp/pull/51) [`d27f7c0`](https://github.com/commercetools/commerce-mcp/commit/d27f7c0520b37c1e11234175d2366e543f96ffb3) Thanks [@ajimae](https://github.com/ajimae)! - Update packages to use the shared tools package
  [Feat][DEVX-842] Use standalone @commercetools/tools-core packages

### Patch Changes

- Updated dependencies [[`d27f7c0`](https://github.com/commercetools/commerce-mcp/commit/d27f7c0520b37c1e11234175d2366e543f96ffb3)]:
  - @commercetools/commerce-agent@4.0.0

## 3.0.1

### Patch Changes

- Updated dependencies [[`14c35c9`](https://github.com/commercetools/commerce-mcp/commit/14c35c971e4197d69d0a73bc22af884518fb5abf)]:
  - @commercetools/commerce-agent@3.1.0

## 3.0.0

### Major Changes

- [#46](https://github.com/commercetools/commerce-mcp/pull/46) [`770c99b`](https://github.com/commercetools/commerce-mcp/commit/770c99b424eb02106f68f6997d0a276ec1eac1b5) Thanks [@geethanga-ct](https://github.com/geethanga-ct)! - fix(security): require Authorization header for the streamable HTTP server (DEVX-806 / COM-15-004)

  **BREAKING:** In remote/streamable HTTP mode, `/mcp` now requires a valid
  `Authorization: Bearer <token>` on every request. Existing remote clients that
  relied on the no-header fallback will receive `401 Unauthorized` until they send
  a token.

  The remote/streamable HTTP MCP server no longer falls back to the credentials
  provided at startup when an incoming request omits the `Authorization` header.
  Previously an unauthenticated network caller could be served using the server's
  own configured token.

  ### What changed
  - Every request to `/mcp` must now include a valid
    `Authorization: Bearer <token>` header; missing or malformed headers are
    rejected with `401 Unauthorized` before any commercetools call is made.
  - The caller's bearer token is forwarded directly to the commercetools API
    (`auth_token` flow). This also fixes a latent bug where a server started with
    `client_credentials` silently ignored the per-request header token.
  - The handler no longer mutates the shared `authConfig`; each request builds an
    isolated per-request auth config.
  - Added an `enforceAuthHeader` option to `CommercetoolsCommerceAgentStreamable`
    (defaults to `true`). Embedders that perform their own authentication via an
    injected `server` factory can set it to `false` to opt out.

  ### Migration

  Clients connecting to a remote server (e.g. via `mcp-remote`) must now send an
  `Authorization: Bearer <commercetools-access-token>` header on every request.
  The startup credentials are no longer used to serve network requests.

### Patch Changes

- Updated dependencies [[`770c99b`](https://github.com/commercetools/commerce-mcp/commit/770c99b424eb02106f68f6997d0a276ec1eac1b5)]:
  - @commercetools/commerce-agent@3.0.0

## 2.0.0

### Major Changes

- [#39](https://github.com/commercetools/commerce-mcp/pull/39) [`df51410`](https://github.com/commercetools/commerce-mcp/commit/df514108420915df16886679e02f0a69d7db7db7) Thanks [@ajimae](https://github.com/ajimae)! - major package updates and bug fixes

  ### What Changed
  - Tool output now is defaulted to `json`
    _this means if `--toolOutputFormat` option is not specified then it defaults to `json`_
  - Tool output text in `json` format has been dropped
    _the root explanatory text for tool output json object has been removed_

  ```ts
  // before
  {
    "READ CART DISCOUNT RESULT": {
      limit: 10,
      offset: 0,
      count: 10,
      results: [
        {
          id: '123',
          name: 'Cart Discount 1',
          description: 'This is a cart discount',
          code: '1234567890',
        }
      ],
    },
  }

  // after
  {
    limit: 10,
    offset: 0,
    count: 10,
    results: [
      {
        id: '123',
        name: 'Cart Discount 1',
        description: 'This is a cart discount',
        code: '1234567890',
      }
    ],
  }
  ```

  The `READ CART DISCOUNT RESULT` text has been dropped
  - The `all` tool now requires setting `isAdmin` option to `true`

  ```bash
  npx -y @commercetools/commerce-mcp --tools="all" --isAdmin=true ...
  ```

### Patch Changes

- Updated dependencies [[`c29fcef`](https://github.com/commercetools/commerce-mcp/commit/c29fcef5ab61d11d18c5103ade8dd382f22f1d44), [`df51410`](https://github.com/commercetools/commerce-mcp/commit/df514108420915df16886679e02f0a69d7db7db7)]:
  - @commercetools/commerce-agent@2.0.0

## 1.0.7

### Patch Changes

- Updated dependencies [[`b9ac11e`](https://github.com/commercetools/commerce-mcp/commit/b9ac11e37e3c378b8aff8f003d43f65dae543a18)]:
  - @commercetools/commerce-agent@1.1.0

## 1.0.6

### Patch Changes

- [#22](https://github.com/commercetools/commerce-mcp/pull/22) [`7c349fb`](https://github.com/commercetools/commerce-mcp/commit/7c349fb63ae337a2d3097d1571977fbf9e2f1b29) Thanks [@Trackerchum](https://github.com/Trackerchum)! - [Fix] Fixed dependencies

- Updated dependencies [[`7c349fb`](https://github.com/commercetools/commerce-mcp/commit/7c349fb63ae337a2d3097d1571977fbf9e2f1b29)]:
  - @commercetools/commerce-agent@1.0.6

## 1.0.5

### Patch Changes

- Updated dependencies [[`37d37b4`](https://github.com/commercetools/commerce-mcp/commit/37d37b44528e7cad5832ff642495b2fac24967c8)]:
  - @commercetools/commerce-agent@1.0.5

## 1.0.4

### Patch Changes

- [#18](https://github.com/commercetools/commerce-mcp/pull/18) [`6ee546a`](https://github.com/commercetools/commerce-mcp/commit/6ee546a54b2172ae9316b077ba0fe2a90889ee96) Thanks [@ajimae](https://github.com/ajimae)! - update repository url in package.json file

- Updated dependencies [[`6ee546a`](https://github.com/commercetools/commerce-mcp/commit/6ee546a54b2172ae9316b077ba0fe2a90889ee96)]:
  - @commercetools/commerce-agent@1.0.4

## 1.0.3

### Patch Changes

- [#16](https://github.com/commercetools/commerce-mcp/pull/16) [`3999782`](https://github.com/commercetools/commerce-mcp/commit/3999782c7fc030f267d88822228d558133f29118) Thanks [@ajimae](https://github.com/ajimae)! - release packages
  update npm and node versions
- Updated dependencies [[`3999782`](https://github.com/commercetools/commerce-mcp/commit/3999782c7fc030f267d88822228d558133f29118)]:
  - @commercetools/commerce-agent@1.0.3

## 1.0.2

### Patch Changes

- [#14](https://github.com/commercetools/commerce-mcp/pull/14) [`87e679a`](https://github.com/commercetools/commerce-mcp/commit/87e679a68db92a43f92b4f75d415233ba3feb915) Thanks [@ajimae](https://github.com/ajimae)! - release packages

- Updated dependencies [[`87e679a`](https://github.com/commercetools/commerce-mcp/commit/87e679a68db92a43f92b4f75d415233ba3feb915)]:
  - @commercetools/commerce-agent@1.0.2

## 1.0.1

### Patch Changes

- [#10](https://github.com/commercetools/commerce-mcp/pull/10) [`fce61a3`](https://github.com/commercetools/commerce-mcp/commit/fce61a3514560bd7a39b5d8e6309b58633cf87b7) Thanks [@behnamt](https://github.com/behnamt)! - Fix Channel input-schema

- [#13](https://github.com/commercetools/commerce-mcp/pull/13) [`6c21409`](https://github.com/commercetools/commerce-mcp/commit/6c214095b4338f9bc5553ee22ae3cbdc0817b75a) Thanks [@ajimae](https://github.com/ajimae)! - [Chore] Clean Up Git Markers

- Updated dependencies [[`fce61a3`](https://github.com/commercetools/commerce-mcp/commit/fce61a3514560bd7a39b5d8e6309b58633cf87b7), [`6c21409`](https://github.com/commercetools/commerce-mcp/commit/6c214095b4338f9bc5553ee22ae3cbdc0817b75a)]:
  - @commercetools/commerce-agent@1.0.1

## 1.0.0

### Major Changes

- [#5](https://github.com/commercetools/commerce-mcp/pull/5) [`9440a1b`](https://github.com/commercetools/commerce-mcp/commit/9440a1b243ded7a418861269dd5ca8e81a77acc9) Thanks [@Trackerchum](https://github.com/Trackerchum)! - First stable major release

### Patch Changes

- Updated dependencies [[`9440a1b`](https://github.com/commercetools/commerce-mcp/commit/9440a1b243ded7a418861269dd5ca8e81a77acc9)]:
  - @commercetools/commerce-agent@1.0.0

## 0.0.1

### Patch Changes

- [#1](https://github.com/commercetools/commerce-mcp/pull/1) [`e6e997f`](https://github.com/commercetools/commerce-mcp/commit/e6e997f25af240aa2ab278c864d22627864a274b) Thanks [@Trackerchum](https://github.com/Trackerchum)! - - Renamed mcp-essentials to commerce-mcp, and agent-essentials with commerce-agent.
  - Changed the licence terms.
- Updated dependencies [[`e6e997f`](https://github.com/commercetools/commerce-mcp/commit/e6e997f25af240aa2ab278c864d22627864a274b)]:
  - @commercetools/commerce-agent@0.0.1
