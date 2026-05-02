---
name: python-namespace-split
description: Enforce the 3-file split pattern (schemas.py + functions.py + __init__.py) for every Python namespace under python/commerce_mcp/tools/. Use this skill whenever a new namespace is being added, an existing namespace uses the all-in-one __init__.py pattern (like carts or orders), or someone asks to check namespace structure. Trigger on phrases like "check namespace structure", "enforce namespace pattern", "namespace split", "fix namespace", "refactor carts namespace", "migrate all-in-one namespace".
---

# Enforce Python Namespace 3-File Split

Every namespace under `python/commerce_mcp/tools/<namespace>/` **must** use this structure:

```
python/commerce_mcp/tools/<namespace>/
├── __init__.py    ← ToolDefinition declarations + register_tool() calls ONLY
├── schemas.py     ← Pydantic v2 input models ONLY
└── functions.py   ← async handler implementations ONLY
```

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

### functions.py — only async handlers
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
- No ToolDefinition, no register_tool
- No FastMCP, no Context imports
- Imports schemas from `.schemas`

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

## When migrating an existing all-in-one namespace

1. Create `schemas.py` — move all `BaseModel` subclasses there
2. Create `functions.py` — move all `async def` handlers there, update imports
3. Rewrite `__init__.py` to only import and register
4. Update `tests/tools/<namespace>/test_functions.py` imports to `from commerce_mcp.tools.<namespace>.functions import ...` and `from commerce_mcp.tools.<namespace>.schemas import ...`

## Reference implementation

`python/commerce_mcp/tools/products/` is the canonical example. Read it before writing any namespace.
