---
'@commercetools/commerce-mcp': major
'@commercetools/commerce-agent': major
'@commercetools/processors': major
---

Require Node.js 20 or newer, and publish the MCP CLI as an ES module. Groundwork for the MCP SDK v2 migration (DEVX-882): the v2 packages are ESM-only and declare `engines.node >= 20`.

The executable moves from `dist/index.js` to `dist/cli.js` — a thin bin shim, so `index.js` stays importable without starting a server as a side effect. Anyone invoking the package through `npx @commercetools/commerce-mcp` or the `bin` entry is unaffected; only a direct `node .../dist/index.js` invocation needs updating.
