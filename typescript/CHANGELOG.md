# @commercetools/commerce-agent

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
