---
"@commercetools/commerce-agent": patch
---

Keep recursive tool schemas instead of discarding them.

Schemas were generated with `$refStrategy: 'none'`, which inlines every subschema so a client never has to resolve a reference. A recursive schema cannot be inlined, and the generator resolved that by emitting an empty schema and logging `Recursive reference detected at ...! Defaulting to any` — ten of those on startup.

The effect was that those branches shipped as `{}`: `read_product_search` described none of its compound `query` / `postFilter` DSL (`and`, `or`, `not`, `filter`), and the nested `elementType` of `update_product_types` and `update_types` was equally absent. Callers got no guidance on the most structured part of those tools, and nothing validated what they sent.

`$refStrategy: 'root'` points those branches at their own definition — `{"$ref": "#/properties/query"}` — which is the only way a recursive schema can be expressed. It also deduplicates repeated subschemas, so the combined size of all 122 tool schemas drops by roughly a quarter.

References are local pointers into the same schema, so there is no separate `$defs` section to fetch. A test asserts every `$ref` across every tool resolves, and that generating the full tool surface produces no recursion warnings.
