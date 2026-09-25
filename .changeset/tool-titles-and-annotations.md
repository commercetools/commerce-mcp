---
"@commercetools/commerce-agent": minor
---

Register tools through `registerTool` and report an accurate server identity (DEVX-885).

The three remaining `server.tool(...)` calls are deprecated in the MCP SDK and positional. They now go through `registerTool` with a config object, which is also what the v2 API takes — so the transport migration no longer has to touch every call site.

Each tool now advertises a `title` and MCP `annotations`, derived from the verb it already declares: `read` is read-only and idempotent, `create` is additive, `update` is marked destructive because it overwrites existing resource state. All are open-world, since they call a remote commercetools project.

The server identity reported `version: '0.4.0'` while the package was at 4.x. It now reads the version straight from `package.json`, alongside a `description`, `title`, `websiteUrl` and usage `instructions`, so a release bump cannot leave the reported identity behind.
