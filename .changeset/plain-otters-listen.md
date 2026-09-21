---
'@commercetools/commerce-mcp': minor
'@commercetools/commerce-agent': minor
'@commercetools/processors': minor
---

Require Node.js 20 or newer, and publish the MCP CLI as an ES module. Groundwork for the MCP SDK v2 migration (DEVX-882): the v2 packages are ESM-only and declare `engines.node >= 20`.

The executable moves from `dist/index.js` to `dist/cli.js` — a thin bin shim, so `index.js` stays importable without starting a server as a side effect. Anyone invoking the package through `npx @commercetools/commerce-mcp` or the `bin` entry is unaffected; only a direct `node .../dist/index.js` invocation needs updating.

Three changes here can break an existing setup, so check them before upgrading:

- **Node 18 is no longer supported.** Install fails on `engines.node` unless you are on Node 20 or newer.
- **CommonJS consumers cannot `require()` these packages.** The published output is ESM only; use a dynamic `import()` or move the consuming code to ESM.
- **`node .../dist/index.js` no longer starts a server.** It now only exports `main()`. Call `dist/cli.js` instead.
