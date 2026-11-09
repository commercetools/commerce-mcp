---
name: python-namespace-split
description: Enforce the namespace file structure for every Python namespace under python/commerce_mcp/tools/. Simple namespaces use the 3-file split (schemas.py + functions.py + __init__.py). Namespaces with multiple context scopes (admin/customer/store/associate) expand functions.py into a set of scope files. Use this skill whenever a new namespace is being added, an existing namespace uses the all-in-one __init__.py pattern, or someone asks to check or fix namespace structure.
---

# Python Namespace File Structure

Every namespace under `python/commerce_mcp/tools/<namespace>/` uses the **3-file minimum**:

```
python/commerce_mcp/tools/<namespace>/
├── __init__.py    ← ToolDefinition declarations + register_tool() calls ONLY
├── schemas.py     ← Pydantic v2 input models ONLY
└── functions.py   ← async handler implementations ONLY
```

For namespaces with multiple context scopes (admin, customer, store, associate), `functions.py` becomes a **thin dispatcher** and the actual logic lives in scope files:

```
python/commerce_mcp/tools/<namespace>/
├── __init__.py              ← ToolDefinition + register_tool() ONLY
├── schemas.py               ← Pydantic v2 input models ONLY
├── base_functions.py        ← shared helpers (get by id/key, query, verify ownership)
├── admin_functions.py       ← admin-scoped handlers
├── customer_functions.py    ← customer-scoped handlers (if applicable)
├── store_functions.py       ← store-scoped handlers (if applicable)
├── as_associate_functions.py← associate-scoped handlers (if applicable)
└── functions.py             ← ONLY public dispatch (imports scope files, routes by ctx)
```

**Rule:** scope files are internal — only `functions.py` imports them. No other file in the codebase imports from `admin_functions.py`, `customer_functions.py`, etc. directly.

No mixing. Each file has exactly one responsibility.

## What belongs in each file

### schemas.py — only Pydantic models
```python
from __future__ import annotations
from pydantic import BaseModel, Field

class ListXParams(BaseModel):
    id: str | None = Field(None, description="...")
    limit: int = Field(20, ge=1, le=500)
```
- No handler logic
- No imports from `..registry` or `...api`
- No ToolDefinition, no register_tool

### functions.py — handlers (simple) or dispatcher (multi-scope)

**Simple namespace** — all handler logic lives here directly:
```python
from __future__ import annotations
from typing import TYPE_CHECKING
from .schemas import ListXParams, CreateXParams
from ...shared.errors import SDKError, ContextError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext

async def list_x(params: ListXParams, api: "CommercetoolsAPI", ctx: "CTContext") -> str:
    try:
        result = await api.get("/x", params={"limit": params.limit})
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("list x", e)
```

**Multi-scope namespace** — `functions.py` is a pure dispatcher, logic is in scope files:
```python
from __future__ import annotations
from typing import TYPE_CHECKING
from .schemas import ReadXParams, CreateXParams
from ...shared.errors import ContextError
from . import admin_functions as admin
from . import customer_functions as customer
from . import store_functions as store
from . import as_associate_functions as associate

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext

async def read_x(params: ReadXParams, api: "CommercetoolsAPI", ctx: "CTContext") -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await associate.read_x(params, api, ctx)
    if ctx.customer_id:
        return await customer.read_x(params, api, ctx)
    if ctx.store_key:
        return await store.read_x(params, api, ctx)
    if ctx.is_admin:
        return await admin.read_x(params, api, ctx)
    raise ContextError("read_x", "isAdmin, customerId, storeKey, or customerId+businessUnitKey")
```

In both cases:
- No ToolDefinition, no register_tool
- No FastMCP, no Context imports
- Imports schemas from `.schemas`

### base_functions.py — shared helpers (multi-scope only)

Utility functions used by multiple scope files: fetch by id/key, query with filters, verify ownership.
```python
from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI

async def get_x_by_id(api: "CommercetoolsAPI", x_id: str, expand: list[str] | None = None) -> dict:
    ...
async def verify_x_belongs_to_customer(api: "CommercetoolsAPI", customer_id: str, x_id: str) -> bool:
    ...
```
- No schemas, no SDKError, no transform
- No CTContext — helpers are context-agnostic

### Scope files (admin_functions.py, customer_functions.py, etc.) — multi-scope only

Each scope file contains the 4 handler functions for that context (`read_x`, `create_x`, `replicate_x`, `update_x`). They import from `base_functions.py` and `schemas.py`:
```python
from .base_functions import get_x_by_id, query_x, serialize_actions
from .schemas import ReadXParams, CreateXParams
from ...shared.errors import SDKError
from ...shared.transform import transform_tool_output
```
- Never import ContextError (dispatch is handled in functions.py)
- Never import from other scope files
- Only `functions.py` imports these files

### __init__.py — only ToolDefinition + registration
```python
from __future__ import annotations
from ..registry import ToolDefinition, register_tool
from .schemas import ListXParams, CreateXParams
from .functions import list_x, create_x

_X_TOOLS = [
    ToolDefinition(
        method="list_x",
        name="List X",
        description="...",
        parameters=ListXParams,
        handler=list_x,
        actions={"x": {"read": True}},
    ),
    ToolDefinition(
        method="create_x",
        name="Create X",
        description="...",
        parameters=CreateXParams,
        handler=create_x,
        actions={"x": {"create": True}},
    ),
]
for _tool in _X_TOOLS:
    register_tool(_tool)
```
- No handler logic
- No Pydantic model definitions
- No direct API calls

## Anti-patterns to reject

| Pattern | Problem |
|---------|---------|
| Pydantic models in `__init__.py` | Blurs schema/registration boundary |
| Handler functions in `__init__.py` | Makes functions untestable without importing registration side-effects |
| `register_tool()` in `functions.py` | Mixes framework wiring into pure logic |
| `ToolDefinition` in `schemas.py` | Wrong layer — schemas don't know about registration |

## When to use each structure

| Namespace type | Structure |
|---------------|-----------|
| Admin-only, single context | 3-file minimum |
| Multiple context scopes (admin/customer/store/associate) | Scope files + dispatcher |

The carts namespace is the canonical multi-scope example. Products is the canonical simple example.

## When migrating an existing all-in-one namespace

**Simple (single context):**
1. Create `schemas.py` — move all `BaseModel` subclasses there
2. Create `functions.py` — move all `async def` handlers there, update imports
3. Rewrite `__init__.py` to only import and register
4. Update test imports to `.functions` and `.schemas`

**Multi-scope:**
1. Create `schemas.py` and `__init__.py` as above
2. Create `base_functions.py` — extract shared helpers
3. Create one scope file per context (`admin_functions.py`, etc.) — move scoped handlers there
4. Replace `functions.py` with the thin dispatcher pattern
5. Update test imports — tests still import only from `.functions`, never scope files

## Reference implementations

- Simple: `python/commerce_mcp/tools/products/`
- Multi-scope: `python/commerce_mcp/tools/carts/`
