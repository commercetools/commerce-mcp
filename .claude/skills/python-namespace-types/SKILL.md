---
name: python-namespace-types
description: Enforce concrete type annotations on every handler function in Python namespace files. Use this skill whenever adding a new handler, reviewing an existing namespace, or checking that handler signatures have fully annotated parameters. Trigger on phrases like "check handler types", "enforce type annotations", "annotate handler", "missing types", "untyped handler", "add type hints to handler".
---

# Enforce Type Annotations on Handler Functions

Every handler function in `functions.py` (or `__init__.py` for legacy all-in-one namespaces) **must** carry concrete type annotations on all three parameters.

## Required signature shape

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext

async def my_handler(
    params: MyParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    ...
```

All three rules apply together:

| Parameter | Type | Notes |
|-----------|------|-------|
| `params` | Concrete Pydantic model (e.g. `ListProductsParams`) | Never `Any`, never untyped |
| `api` | `"CommercetoolsAPI"` | String annotation via `TYPE_CHECKING` to avoid circular import |
| `ctx` | `"CTContext"` | String annotation via `TYPE_CHECKING` |
| return | `str` | Always `str` — transform_tool_output returns str |

## Why string annotations for api and ctx

`CommercetoolsAPI` and `CTContext` live in parent packages. Importing them directly at the top of `functions.py` would create a circular dependency (`api.py` → `tools/registry.py` → `tools/products/functions.py` → `api.py`). The `TYPE_CHECKING` guard breaks the cycle: the import only runs for static type checkers, not at runtime.

## Private scope-specific implementations

Private helpers (prefixed `_`) follow the same rules:

```python
async def _read_x_admin(
    params: ReadXParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    ...
```

## Anti-patterns to reject

```python
# ❌ Untyped params
async def list_x(params, api, ctx) -> str: ...

# ❌ Any-typed api
async def list_x(params: ListXParams, api: Any, ctx: Any) -> str: ...

# ❌ Direct import (circular)
from ...api import CommercetoolsAPI
async def list_x(params: ListXParams, api: CommercetoolsAPI, ctx: CTContext) -> str: ...

# ❌ Wrong params type — handler registered with ListXParams but signature uses BaseModel
async def list_x(params: BaseModel, api: "CommercetoolsAPI", ctx: "CTContext") -> str: ...
```

## Checking an existing namespace

For each public and private handler function in `functions.py`:

1. Confirm `params` is annotated with the specific Pydantic model from `schemas.py`
2. Confirm `api` is annotated `"CommercetoolsAPI"` (string)
3. Confirm `ctx` is annotated `"CTContext"` (string)
4. Confirm `-> str` return annotation is present
5. Confirm `CommercetoolsAPI` and `CTContext` are under `TYPE_CHECKING`, not top-level

If any of the above are missing, add the annotations — do not leave them untyped.

## Reference

`python/commerce_mcp/tools/products/functions.py` is the canonical example. All three handler functions there carry full annotations.
