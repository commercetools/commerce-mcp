---
"@commercetools/commerce-agent": patch
---

Stop warning about the dynamic-loading tools on every start.

`list_available_tools`, `inject_tools` and `execute_tool` are registered by this package, not drawn from the `@commercetools/tools-core` catalogue, so they have no catalogue verb and always take the conservative annotation fallback. Logging that each time the server starts reported an expected condition as a problem — three lines on every launch once dynamic tool loading engages.

The fallback still applies to them, unchanged: they are annotated as writing and destroying, so a client asks before calling. Only the log is suppressed, and only for tools this package registers itself. A tool that reaches the fallback without being one of ours — an embedder's custom tool, or a catalogue tool whose verb stopped resolving — still logs, because that is worth knowing about.

The list is derived from the tool definitions rather than written out again, so adding one cannot leave it behind.
