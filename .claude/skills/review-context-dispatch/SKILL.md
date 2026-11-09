---
name: review-context-dispatch
description: Review Python context dispatch handlers against TypeScript source to verify security faithfulness. Use this skill whenever the user wants to audit or verify that Python tool handlers correctly implement the TypeScript `contextToXFunctionMapping` security contract, check for silent admin fallthrough bugs, ensure ContextError is raised for unauthorized context combinations, or confirm that security tests exist for every dispatch boundary. Trigger on phrases like "review context dispatch", "audit security dispatch", "check Python vs TypeScript mapping", "verify context guards", "review dispatch faithfulness", or any mention of checking is_admin fallthrough or ContextError coverage.
---

# Review Python Context Dispatch Against TypeScript Source

For each namespace, verify that the Python dispatch handlers faithfully implement the TypeScript security contract and that tests cover every boundary.

## Which namespaces to review

If namespaces are specified (e.g. `orders carts`), review only those. Otherwise review all namespaces found under `python/commerce_mcp/tools/` that have a corresponding TypeScript source in `typescript/src/shared/`.

## For each namespace

### 1. Read the TypeScript source of truth

Open `typescript/src/shared/<namespace>/functions.ts` and find the `contextToXFunctionMapping` function. This function determines which API call is made for each combination of context fields (`isAdmin`, `customerId`, `storeKey`, `businessUnitKey`). It is the authoritative security contract.

### 2. Check dispatch faithfulness

For each public handler function in `python/commerce_mcp/tools/<namespace>/functions.py` (or `__init__.py`), verify:

| Check | What to look for |
|-------|-----------------|
| Every TS branch has a matching Python `if` | Check for missing context paths |
| No extra branches not in TS mapping | Check for unauthorized additions |
| Final `else` raises `ContextError` | **Critical: never calls admin** |
| Customer-only context excluded from write ops (if TS excludes it) | **Critical security bug if missing** |
| `is_admin` is the explicit last guard before `ContextError` | Must be a named check, not a fallthrough |

The single most important rule: if `contextToXFunctionMapping` returns `{}` for a context combination, the Python handler **must** raise `ContextError`. No silent fallthrough.

### 3. Check that tests exist

Open `python/tests/tools/<namespace>/test_functions.py` and verify:

| Test required | Present? |
|--------------|---------|
| One test per valid context path (admin, customer, store, associate) | ✅ / ❌ |
| Test for `CTContext()` (no context at all) → raises `ContextError` | ✅ / ❌ |
| Test for customer-only context on write ops (if TS excludes this) → raises `ContextError` | ✅ / ❌ |
| Each `ContextError` test asserts `mock_api.post/get.assert_not_called()` | ✅ / ❌ |

## Output format

For each namespace, produce a section like this:

```
## <namespace>

TypeScript mapping:  typescript/src/shared/<namespace>/functions.ts
Python dispatch:     python/commerce_mcp/tools/<namespace>/functions.py
Test file:          python/tests/tools/<namespace>/test_functions.py

### Dispatch faithfulness
- [✅/❌] customerId+businessUnitKey → associate
- [✅/❌] customerId only → customer (read only / all ops)
- [✅/❌] storeKey → store
- [✅/❌] isAdmin → admin (explicit guard, not fallthrough)
- [✅/❌] no context → ContextError

### Security issues (if any)
<list issues, or "None">

### Missing tests (if any)
<list missing test cases, or "None">
```

End with a **summary table**:

```
| namespace | dispatch correct | tests present | security issues |
|-----------|-----------------|---------------|-----------------|
| orders    | ✅               | ✅             | None            |
| carts     | ❌               | ❌             | admin fallthrough in create_cart |
```

## Common security bugs to flag

Flag these as **CRITICAL** — they silently grant elevated access:

- Final `else` branch calls admin function instead of raising `ContextError`
- Missing `if ctx.is_admin:` guard — admin branch is only reachable via fallthrough
- Write operation allows `customerId`-only context when TypeScript mapping excludes it
- Any branch that grants more access than the TypeScript mapping authorizes
