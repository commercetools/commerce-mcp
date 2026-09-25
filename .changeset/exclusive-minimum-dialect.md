---
"@commercetools/commerce-agent": patch
---

Emit exclusive numeric bounds in the dialect MCP actually speaks.

Tool schemas were generated with zod-to-json-schema's `jsonSchema2019-09` target, chosen because its name is closest to MCP's 2020-12 default dialect. That target is the wrong one: for `.positive()` and `.gt()` it emits the draft-4 spelling `{minimum: n, exclusiveMinimum: true}`, and every draft-6-or-later validator rejects a boolean there.

The effect was that a client which validates schemas — MCP Inspector among them — failed to connect with `exclusiveMinimum value must be ["number"]`. Four tools carried it: `create_cart_discounts`, `update_cart_discounts`, `create_orders` and `update_inventory`.

Switching to the `jsonSchema7` target emits the numeric `{exclusiveMinimum: n}` that 2020-12 also expects, and matches 2020-12 on every other keyword our tools use. A test now compiles all 122 tool schemas through the SDK's own validator, which is where the failure surfaced.
