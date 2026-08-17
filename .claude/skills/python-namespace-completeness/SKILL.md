# Skill: Python Namespace Completeness Audit

## Problem

A Python namespace may be structurally correct (proper 3-file split, correct types) but functionally incomplete: missing entire tools, missing scope implementations, or lacking registration.

**Observed gaps (carts):**
- `replicate_cart` was completely absent from Python — no schema, no handlers, no `__init__.py` registration
- Even after schema and handler work, it wasn't added to `_CART_TOOLS` in `__init__.py`

## Rule

**Every tool that TypeScript exposes must exist in Python with all four scope implementations registered.**

## How to Apply

### 1. Enumerate TypeScript tools

Check `typescript/src/shared/<N>/functions.ts` (the dispatcher) and `tools.ts` (MCP registration). Count the exported tool names. For carts: `read_cart`, `create_cart`, `replicate_cart`, `update_cart`.

### 2. Enumerate Python tools

Check `python/commerce_mcp/tools/<N>/__init__.py`. Count the `ToolDefinition` entries. Anything missing needs to be added.

### 3. For each tool, verify all four scope implementations exist

In `functions.py`, each tool should have four private handlers:
```
_<tool>_admin
_<tool>_customer
_<tool>_store
_<tool>_as_associate
```
And one public dispatcher that routes to them.

If a scope implementation is absent, add it before registering the tool.

### 4. Verify schema completeness

For each tool, `schemas.py` must have a corresponding `Params` class. If a tool like `replicateCart` is present in TypeScript but has no `ReplicateCartParams` in Python, create it first (see `python-schema-alignment` skill).

### 5. Verify `__init__.py` registration

Each tool needs a `ToolDefinition` entry in `_<NAMESPACE>_TOOLS` with:
- `method`: snake_case tool name (e.g. `"replicate_cart"`)
- `name`: human-readable name
- `description`: one-sentence description
- `parameters`: the Pydantic class
- `handler`: the public dispatch function
- `actions`: correct permission dict (e.g. `{"cart": {"create": True}}` for replicate)

### 6. Verify the import line

The `from .functions import ...` and `from .schemas import ...` lines must include the new symbols.

### 7. Map TypeScript actions to Python actions

| TypeScript operation | Python `actions` dict |
|---------------------|----------------------|
| read | `{"<resource>": {"read": True}}` |
| create / replicate | `{"<resource>": {"create": True}}` |
| update | `{"<resource>": {"update": True}}` |

## Completeness Checklist

For each TypeScript tool in the namespace:

- [ ] `Params` class exists in `schemas.py`
- [ ] `_<tool>_admin` handler exists in `functions.py`
- [ ] `_<tool>_customer` handler exists in `functions.py`
- [ ] `_<tool>_store` handler exists in `functions.py`
- [ ] `_<tool>_as_associate` handler exists in `functions.py`
- [ ] Public `<tool>` dispatcher routes to all four scopes
- [ ] `ToolDefinition` for `<tool>` exists in `__init__.py`
- [ ] Correct `actions` dict on `ToolDefinition`
- [ ] `from .schemas import` and `from .functions import` include the new symbols
- [ ] Test for `ContextError` when no context is set for this tool
- [ ] All tests pass: `python3 -m pytest tests/`
