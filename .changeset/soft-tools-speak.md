---
'@commercetools/commerce-agent': minor
---

Return structured tool output (DEVX-884). Tool results now carry `structuredContent` alongside the existing text block, so clients no longer have to parse our stringified JSON back out of a text content block. The text content is unchanged, so existing clients are unaffected.

Array and scalar payloads travel in the text block only: the protocol models structured output as a JSON object, and wrapping those in an invented envelope would be a guess about shape.

Also flags failed `execute_tool` calls with `isError: true`. Tools that throw were already flagged by the SDK, but `execute_tool` caught the error and returned a plain text result, leaving a failure indistinguishable from a success whose text happens to mention an error.
