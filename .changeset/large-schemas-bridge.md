---
'@commercetools/commerce-agent': patch
---

Add a zod → JSON Schema bridge for tool parameters (DEVX-883). MCP SDK v2 registers tools from a validator that can emit JSON Schema (zod 4, ArkType, Valibot) or from raw JSON Schema via `fromJsonSchema`, while our tool parameters come from `@commercetools/tools-core` on zod 3. Converting to JSON Schema keeps us on zod 3 and makes the wire format the one the protocol actually speaks.

`toJsonSchema()` and `toolInputJsonSchema()` drop `$schema` (MCP's default dialect is JSON Schema 2020-12, so declaring an older one per tool would be wrong), drop `additionalProperties` (zod strips unknown keys; rendering that as `additionalProperties: false` would turn a stray model-supplied argument into a validation failure), and inline nested schemas so clients never resolve `$ref`. Not yet wired into registration — that lands with the v2 server migration.
