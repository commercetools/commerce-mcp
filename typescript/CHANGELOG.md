# @commercetools/commerce-agent

## 4.2.0

### Minor Changes

- [#59](https://github.com/commercetools/commerce-mcp/pull/59) [`49a315f`](https://github.com/commercetools/commerce-mcp/commit/49a315fcfd5ccd3b9cdcdcbfbeaec007f6f7bc64) Thanks [@ajimae](https://github.com/ajimae)! - Require Node.js 20 or newer, and publish the MCP CLI as an ES module. Groundwork for the MCP SDK v2 migration (DEVX-882): the v2 packages are ESM-only and declare `engines.node >= 20`.

  The executable moves from `dist/index.js` to `dist/cli.js` — a thin bin shim, so `index.js` stays importable without starting a server as a side effect. Anyone invoking the package through `npx @commercetools/commerce-mcp` or the `bin` entry is unaffected; only a direct `node .../dist/index.js` invocation needs updating.

  Three changes here can break an existing setup, so check them before upgrading:

  - **Node 18 is no longer supported.** Install fails on `engines.node` unless you are on Node 20 or newer.
  - **CommonJS consumers cannot `require()` these packages.** The published output is ESM only; use a dynamic `import()` or move the consuming code to ESM.
  - **`node .../dist/index.js` no longer starts a server.** It now only exports `main()`. Call `dist/cli.js` instead.

- [#61](https://github.com/commercetools/commerce-mcp/pull/61) [`43e6264`](https://github.com/commercetools/commerce-mcp/commit/43e62641daf0f114845977af13859c494c5ed140) Thanks [@ajimae](https://github.com/ajimae)! - Return structured tool output (DEVX-884). Tool results now carry `structuredContent` alongside the existing text block, so clients no longer have to parse our stringified JSON back out of a text content block. The text content is unchanged, so existing clients are unaffected.

  Array and scalar payloads travel in the text block only: the protocol models structured output as a JSON object, and wrapping those in an invented envelope would be a guess about shape.

  Also flags failed `execute_tool` calls with `isError: true`. Tools that throw were already flagged by the SDK, but `execute_tool` caught the error and returned a plain text result, leaving a failure indistinguishable from a success whose text happens to mention an error.

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Register tools through `registerTool` and report an accurate server identity (DEVX-885).

  The three remaining `server.tool(...)` calls are deprecated in the MCP SDK and positional. They now go through `registerTool` with a config object, which is also what the v2 API takes — so the transport migration no longer has to touch every call site.

  Each tool now advertises a `title` and MCP `annotations`, derived from the verb it already declares: `read` is read-only and idempotent, `create` is additive, `update` is marked destructive because it overwrites existing resource state. All are open-world, since they call a remote commercetools project.

  The server identity reported `version: '0.4.0'` while the package was at 4.x. It now reads the version straight from `package.json`, alongside a `description`, `title`, `websiteUrl` and usage `instructions`, so a release bump cannot leave the reported identity behind.

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Serve both protocol eras from the v2 SDK handler (DEVX-886).

  `StreamableHTTPServerTransport` and its session map are replaced by `createMcpHandler` plus the SDK's Node adapter, and the CLI's stdio transport moves to `@modelcontextprotocol/server/stdio`. The handler builds a server per request from that request's credentials, which is what the previous `getServer` already did, so per-caller auth is unchanged.

  `legacy: 'stateless'` keeps existing clients working: a 2025-era `initialize` still negotiates (against `2025-11-25`), while `server/discover` answers `2026-07-28` on the modern path. Tool registration now goes through the zod → JSON Schema bridge added in DEVX-883, so `tools/list` emits real JSON Schema alongside the titles and annotations from DEVX-885, and is marked cacheable for modern clients.

  Two behaviour changes to know about:

  - **`GET /mcp` now returns 405 instead of 401.** The 2026-07-28 spec removed the GET endpoint, and a GET carries no credentials to protect. `Host`/`Origin` validation still runs first, so DNS-rebinding protection is unaffected.
  - **Protocol sessions are gone**, as flagged in DEVX-888. `Mcp-Session-Id` is no longer issued or accepted, and the session-to-opener binding it required is removed with it. Per-request credentials already provided that guarantee.

  `streamableHttpOptions` is now inert and deprecated; it is still accepted so existing callers typecheck. The stale `@modelcontextprotocol/sdk` v1 peer dependency is dropped — the v2 packages ship as regular dependencies, so consumers no longer need to install the SDK themselves.

### Patch Changes

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Emit exclusive numeric bounds in the dialect MCP actually speaks.

  Tool schemas were generated with zod-to-json-schema's `jsonSchema2019-09` target, chosen because its name is closest to MCP's 2020-12 default dialect. That target is the wrong one: for `.positive()` and `.gt()` it emits the draft-4 spelling `{minimum: n, exclusiveMinimum: true}`, and every draft-6-or-later validator rejects a boolean there.

  The effect was that a client which validates schemas — MCP Inspector among them — failed to connect with `exclusiveMinimum value must be ["number"]`. Four tools carried it: `create_cart_discounts`, `update_cart_discounts`, `create_orders` and `update_inventory`.

  Switching to the `jsonSchema7` target emits the numeric `{exclusiveMinimum: n}` that 2020-12 also expects, and matches 2020-12 on every other keyword our tools use. A test now compiles all 122 tool schemas through the SDK's own validator, which is where the failure surfaced.

- [#60](https://github.com/commercetools/commerce-mcp/pull/60) [`70f5b6e`](https://github.com/commercetools/commerce-mcp/commit/70f5b6e0e2d8c670365b8b7e8becaecb9dc2d1f7) Thanks [@ajimae](https://github.com/ajimae)! - Add a zod → JSON Schema bridge for tool parameters (DEVX-883). MCP SDK v2 registers tools from a validator that can emit JSON Schema (zod 4, ArkType, Valibot) or from raw JSON Schema via `fromJsonSchema`, while our tool parameters come from `@commercetools/tools-core` on zod 3. Converting to JSON Schema keeps us on zod 3 and makes the wire format the one the protocol actually speaks.

  `toJsonSchema()` and `toolInputJsonSchema()` drop `$schema` (MCP's default dialect is JSON Schema 2020-12, so declaring an older one per tool would be wrong), drop `additionalProperties` (zod strips unknown keys; rendering that as `additionalProperties: false` would turn a stray model-supplied argument into a validation failure), and inline nested schemas so clients never resolve `$ref`. Not yet wired into registration — that lands with the v2 server migration.

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Keep serving every 2025-era protocol revision, not just the newest.

  The v2 migration set `supportedProtocolVersions` to `['2026-07-28', '2025-11-25']`. That looks equivalent to the SDK default but is not: the legacy handshake counter-offers the newest listed 2025 revision, so a client asking for `2025-06-18` was answered with `2025-11-25`, and a client that does not recognise that revision disconnects rather than downgrading.

  `mcp-remote` — the bridge Claude Desktop and similar clients use to reach a remote MCP server — does exactly that, failing with `Server's protocol version is not supported: 2025-11-25`. The v1 server accepted five 2025-era revisions; the migration narrowed that to one.

  The list now spreads the SDK's own `SUPPORTED_PROTOCOL_VERSIONS` alongside the 2026 revision, so `2025-11-25`, `2025-06-18`, `2025-03-26`, `2024-11-05` and `2024-10-07` each negotiate as themselves again, and the range stays current with the SDK.

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Fix inconsistencies left by the SDK v2 migration.

  - `context.mode` reported `'stateful'` whenever `--stateless=false` was set, but the 2026-07-28 handler has no sessions and always serves statelessly. Tools and the request log were being told a mode the server never serves. It now reports what actually happens.
  - `server.json` advertised the streamable HTTP endpoint as `http://{HOST}:{PORT}/mcp` without declaring either variable, so a registry had nothing to substitute. Both are real environment variables the CLI reads, and are now declared.
  - The CLI still passed `streamableHttpOptions`, which became inert when the transport moved to `createMcpHandler`, and the README's SDK examples still showed it alongside `stateless: false`. Both removed, so the documented setup matches what the options now do.

  Also restores a regression test lost in the transport rewrite: the route used to catch errors and answer 500 itself, and that responsibility moved to the SDK adapter. A test now asserts a failed per-request server build still surfaces as an error rather than leaving the request unanswered.

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Keep recursive tool schemas instead of discarding them.

  Schemas were generated with `$refStrategy: 'none'`, which inlines every subschema so a client never has to resolve a reference. A recursive schema cannot be inlined, and the generator resolved that by emitting an empty schema and logging `Recursive reference detected at ...! Defaulting to any` — ten of those on startup.

  The effect was that those branches shipped as `{}`: `read_product_search` described none of its compound `query` / `postFilter` DSL (`and`, `or`, `not`, `filter`), and the nested `elementType` of `update_product_types` and `update_types` was equally absent. Callers got no guidance on the most structured part of those tools, and nothing validated what they sent.

  `$refStrategy: 'root'` points those branches at their own definition — `{"$ref": "#/properties/query"}` — which is the only way a recursive schema can be expressed. It also deduplicates repeated subschemas, so the combined size of all 122 tool schemas drops by roughly a quarter.

  References are local pointers into the same schema, so there is no separate `$defs` section to fetch. A test asserts every `$ref` across every tool resolves, and that generating the full tool surface produces no recursion warnings.

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Use the SDK's `validateHostHeader` for DNS-rebinding protection (DEVX-887).

  Our hand-rolled `Host` parser is replaced by the validator shipped in `@modelcontextprotocol/server`, which has the same port-agnostic hostname-allowlist semantics, including bracketed IPv6. The `*` wildcard, the `--allowedHosts` surface and the existing 403 messages are unchanged, so the PLASE-3987 regression tests pass untouched.

  `Origin` checking deliberately keeps our own comparison. The SDK's `validateOriginHeader` matches on hostname only, so a configured `https://app.example.com` would start accepting `http://app.example.com` and any port. Our `--allowedOrigins` values are full origins and are still compared as full origins.

- [#65](https://github.com/commercetools/commerce-mcp/pull/65) [`317c98d`](https://github.com/commercetools/commerce-mcp/commit/317c98d8ebdc5782d3979277cf05c446d7d69416) Thanks [@ajimae](https://github.com/ajimae)! - Update `@commercetools/tools-core` to 0.4.1 and derive tool titles and annotations from it.

  0.4 is additive — same 205 tools, same exports, same zod 3 range, nothing removed — but it adds `titleAndAnnotations`, `deriveToolTitle`, `deriveToolAnnotations`, `toolVerb` and `toolEffect`. That is the mapping DEVX-885 hand-rolled here, so the local copy is removed and the package's version is used instead. The catalogue and the meaning of its verbs now have one owner, and the package has a drift test asserting every tool resolves.

  Two visible differences from the hand-rolled version:

  - Titles come from the tool name rather than its `name` field, so `read_carts` is now `Read Carts` rather than `Read cart`.
  - `idempotentHint` is no longer emitted; the package does not set it.

  `openWorldHint` stays `true`, overriding the package's `false`: every tool reaches a live commercetools project over the network, so another client can change what a call sees between one request and the next.

  Tools outside the catalogue — the dynamic-loading meta-tools and any custom tool an embedder supplies — have no known verb. Those fall back to conservative annotations (assume the tool writes and destroys) and log once, rather than throwing, which is what `titleAndAnnotations` does on an unknown verb.

## 4.1.0

### Minor Changes

- [#53](https://github.com/commercetools/commerce-mcp/pull/53) [`28f7d9e`](https://github.com/commercetools/commerce-mcp/commit/28f7d9e70e1e898149f3dae74b68037c4d15a331) Thanks [@ajimae](https://github.com/ajimae)! - Validate the `Host` and `Origin` headers on the remote (streamable HTTP) server (Cure53 COM-15-006). Requests addressed to an unrecognised hostname are rejected with `403`, which is what closes the DNS rebinding path: a malicious page can rebind its hostname to `127.0.0.1` and stays same-origin as far as the browser is concerned, but the `Host` header still names the attacker's domain. Requests that carry an `Origin` header must match an allow-list too; requests without one (every non-browser MCP client) are unaffected, and no permissive CORS header is ever sent.

  Hostnames default to `localhost`, `127.0.0.1`, `[::1]` plus the resolved `--host`, so a server serving a real domain now needs `--allowedHosts=mcp.example.com` (or `ALLOWED_HOSTS`). Browser origins are opted in with `--allowedOrigins`/`ALLOWED_ORIGINS`. Both accept `*` to disable the check, and both are available as `allowedHosts`/`allowedOrigins` on `CommercetoolsCommerceAgentStreamable`.

- [#53](https://github.com/commercetools/commerce-mcp/pull/53) [`28f7d9e`](https://github.com/commercetools/commerce-mcp/commit/28f7d9e70e1e898149f3dae74b68037c4d15a331) Thanks [@ajimae](https://github.com/ajimae)! - Bind the remote (streamable HTTP) server to `127.0.0.1` by default instead of every network interface (Cure53 COM-15-005). A new `--host` option (or `HOST` environment variable) opts into a wider binding, and the server warns at startup whenever it is bound beyond loopback.

  This changes the default reachability of `--remote=true` servers: deployments that rely on the server accepting connections from other hosts — containers with published ports, Kubernetes pods, anything behind a reverse proxy on another machine — must now pass `--host=0.0.0.0` explicitly. `CommercetoolsCommerceAgentStreamable.listen()` takes an optional host as its second argument, still accepts the `(port, callback)` form, and now returns the underlying server so a bind failure can be observed. `--host=*` is normalised to `0.0.0.0` (Node cannot bind the literal `*`), and a failed bind is reported as `Unable to bind <host>:<port>` instead of exiting silently after logging a misleading "listening" line.

### Patch Changes

- [#53](https://github.com/commercetools/commerce-mcp/pull/53) [`28f7d9e`](https://github.com/commercetools/commerce-mcp/commit/28f7d9e70e1e898149f3dae74b68037c4d15a331) Thanks [@ajimae](https://github.com/ajimae)! - Harden the streamable HTTP server against cross-caller credential sharing (Cure53 COM-15-010). The shared startup `authConfig` is now a frozen copy that cannot be written to after construction, and in stateful mode a session records the bearer token it was opened with: continuing a session with a different token — or with the header dropped — is rejected with `403` instead of reusing the opener's credentials. Stateless mode and sessions opened without a token are unaffected.

## 4.0.0

### Major Changes

- [#51](https://github.com/commercetools/commerce-mcp/pull/51) [`d27f7c0`](https://github.com/commercetools/commerce-mcp/commit/d27f7c0520b37c1e11234175d2366e543f96ffb3) Thanks [@ajimae](https://github.com/ajimae)! - Update packages to use the shared tools package
  [Feat][DEVX-842] Use standalone @commercetools/tools-core packages

## 3.1.0

### Minor Changes

- [#42](https://github.com/commercetools/commerce-mcp/pull/42) [`14c35c9`](https://github.com/commercetools/commerce-mcp/commit/14c35c971e4197d69d0a73bc22af884518fb5abf) Thanks [@behnamt](https://github.com/behnamt)! - Add missing tools
  - approval-flow
  - approval-rule
  - associate-role
  - order-edit
  - product-selection-assignment
  - recurrence-policy
  - state

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

- [#32](https://github.com/commercetools/commerce-mcp/pull/32) [`c29fcef`](https://github.com/commercetools/commerce-mcp/commit/c29fcef5ab61d11d18c5103ade8dd382f22f1d44) Thanks [@geethanga-ct](https://github.com/geethanga-ct)! - fix(security): prevent credential leak in auth error message

## 1.1.0

### Minor Changes

- [#8](https://github.com/commercetools/commerce-mcp/pull/8) [`b9ac11e`](https://github.com/commercetools/commerce-mcp/commit/b9ac11e37e3c378b8aff8f003d43f65dae543a18) Thanks [@Trackerchum](https://github.com/Trackerchum)! - Added customizable field filtering and redaction at a resource level.

## 1.0.6

### Patch Changes

- [#22](https://github.com/commercetools/commerce-mcp/pull/22) [`7c349fb`](https://github.com/commercetools/commerce-mcp/commit/7c349fb63ae337a2d3097d1571977fbf9e2f1b29) Thanks [@Trackerchum](https://github.com/Trackerchum)! - [Fix] Fixed dependencies

## 1.0.5

### Patch Changes

- [#20](https://github.com/commercetools/commerce-mcp/pull/20) [`37d37b4`](https://github.com/commercetools/commerce-mcp/commit/37d37b44528e7cad5832ff642495b2fac24967c8) Thanks [@ajimae](https://github.com/ajimae)! - Update release workflow to create .npmrc file

## 1.0.4

### Patch Changes

- [#18](https://github.com/commercetools/commerce-mcp/pull/18) [`6ee546a`](https://github.com/commercetools/commerce-mcp/commit/6ee546a54b2172ae9316b077ba0fe2a90889ee96) Thanks [@ajimae](https://github.com/ajimae)! - update repository url in package.json file

## 1.0.3

### Patch Changes

- [#16](https://github.com/commercetools/commerce-mcp/pull/16) [`3999782`](https://github.com/commercetools/commerce-mcp/commit/3999782c7fc030f267d88822228d558133f29118) Thanks [@ajimae](https://github.com/ajimae)! - release packages
  update npm and node versions

## 1.0.2

### Patch Changes

- [#14](https://github.com/commercetools/commerce-mcp/pull/14) [`87e679a`](https://github.com/commercetools/commerce-mcp/commit/87e679a68db92a43f92b4f75d415233ba3feb915) Thanks [@ajimae](https://github.com/ajimae)! - release packages

## 1.0.1

### Patch Changes

- [#10](https://github.com/commercetools/commerce-mcp/pull/10) [`fce61a3`](https://github.com/commercetools/commerce-mcp/commit/fce61a3514560bd7a39b5d8e6309b58633cf87b7) Thanks [@behnamt](https://github.com/behnamt)! - Fix Channel input-schema

- [#13](https://github.com/commercetools/commerce-mcp/pull/13) [`6c21409`](https://github.com/commercetools/commerce-mcp/commit/6c214095b4338f9bc5553ee22ae3cbdc0817b75a) Thanks [@ajimae](https://github.com/ajimae)! - [Chore] Clean Up Git Markers

## 1.0.0

### Major Changes

- [#5](https://github.com/commercetools/commerce-mcp/pull/5) [`9440a1b`](https://github.com/commercetools/commerce-mcp/commit/9440a1b243ded7a418861269dd5ca8e81a77acc9) Thanks [@Trackerchum](https://github.com/Trackerchum)! - First stable major release

## 0.0.1

### Patch Changes

- [#1](https://github.com/commercetools/commerce-mcp/pull/1) [`e6e997f`](https://github.com/commercetools/commerce-mcp/commit/e6e997f25af240aa2ab278c864d22627864a274b) Thanks [@Trackerchum](https://github.com/Trackerchum)! - - Renamed mcp-essentials to commerce-mcp, and agent-essentials with commerce-agent.
  - Changed the licence terms.
