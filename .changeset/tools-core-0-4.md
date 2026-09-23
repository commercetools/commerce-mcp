---
"@commercetools/commerce-agent": patch
---

Update `@commercetools/tools-core` to 0.4.1 and derive tool titles and annotations from it.

0.4 is additive — same 205 tools, same exports, same zod 3 range, nothing removed — but it adds `titleAndAnnotations`, `deriveToolTitle`, `deriveToolAnnotations`, `toolVerb` and `toolEffect`. That is the mapping DEVX-885 hand-rolled here, so the local copy is removed and the package's version is used instead. The catalogue and the meaning of its verbs now have one owner, and the package has a drift test asserting every tool resolves.

Three visible differences from the hand-rolled version:

- Titles come from the tool name rather than its `name` field, so `read_carts` is now `Read Carts` rather than `Read cart`.
- `openWorldHint` is `false`, following the package. The previous value here was `true`.
- `idempotentHint` is no longer emitted; the package does not set it.

Tools outside the catalogue — the dynamic-loading meta-tools and any custom tool an embedder supplies — have no known verb. Those fall back to conservative annotations (assume the tool writes and destroys) and log once, rather than throwing, which is what `titleAndAnnotations` does on an unknown verb.
