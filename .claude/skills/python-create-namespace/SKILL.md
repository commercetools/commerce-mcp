---
name: python-create-namespace
description: Step-by-step guide for adding a new tool namespace to the Python fastMCP server under python/commerce_mcp/tools/. Use this skill whenever a new resource namespace needs to be created, ported from TypeScript, or wired into the server. This is the master guide — it coordinates the other namespace skills. Trigger on phrases like "create namespace", "add namespace", "new namespace", "add X tools to Python", "how do I add a new resource", "port X namespace", "scaffold X", or any question about the process of adding a new tool family.
---

# Adding a New Tool Namespace

This guide is the authoritative process for creating a new namespace in the Python server. Follow every step in order. Other skills are called out at the steps where they apply.

## Before you start

Clarify two things:

1. **What is the resource name?** (e.g. `discount_codes`, `shipping_methods`) — this becomes the directory name, the `Actions` field, and the namespace key in `ToolDefinition.actions`.
2. **Does a TypeScript source exist?** (`typescript/src/shared/<namespace>/`) — if yes, read it first (see Step 1B). If you're writing a net-new namespace, skip Step 1B.

---

## Step 1A — Verify the Actions field exists in config.py

Open `python/commerce_mcp/config.py` and find the `Actions` class. Confirm a field for your namespace exists. If it is missing, add it:

```python
# python/commerce_mcp/config.py
class Actions(BaseModel):
    # ... existing fields ...
    discount_code: ResourceActions | None = Field(None, alias="discount-code")
    model_config = {"populate_by_name": True}
```

Rules:
- Use `snake_case` for the Python attribute name
- Use the TypeScript alias (usually `kebab-case`) as `alias=` only when the namespace key contains a hyphen
- Match the exact namespace key used in `ToolDefinition.actions` (see Step 3)

---

## Step 1B — (TypeScript port only) Read the TypeScript source first

If porting an existing TypeScript namespace, read all five files **before writing any Python**:

- `typescript/src/shared/<namespace>/tools.ts` — tool names, descriptions, `actions` requirements
- `typescript/src/shared/<namespace>/parameters.ts` — Zod schemas → translate to Pydantic
- `typescript/src/shared/<namespace>/functions.ts` — read `contextToXFunctionMapping` carefully; this is the security contract
- `typescript/src/shared/<namespace>/base.functions.ts` — API paths used by scope implementations
- `typescript/src/shared/<namespace>/admin.functions.ts`, `customer.functions.ts`, `store.functions.ts`, `as-associate.functions.ts` — per-scope logic

> **Invoke skill: `python-schema-alignment`** for the schema translation. It covers the full Zod→Pydantic mapping table, camelCase alias rules, sub-model extraction, and a completeness checklist.

> **Invoke skill: `python-namespace-completeness`** early to enumerate all tools TypeScript exposes — so you know the full set before writing any code.

The `contextToXFunctionMapping` function is the single most important thing to get right. It determines which API endpoint is called for each combination of context fields (`isAdmin`, `customerId`, `storeKey`, `businessUnitKey`). **Copy it faithfully** — see Step 3 for the dispatch pattern.

---

## Step 2 — Create the directory and three files

Every namespace lives in:

```
python/commerce_mcp/tools/<namespace>/
├── __init__.py     ← ToolDefinition declarations + register_tool() calls only
├── schemas.py      ← Pydantic v2 input models only
└── functions.py    ← async handler implementations only
```

> **Invoke skill: `python-namespace-split`** to verify this structure is correct and understand what belongs in each file.

The products namespace is the canonical example — read it before writing your own:
- `python/commerce_mcp/tools/products/schemas.py`
- `python/commerce_mcp/tools/products/functions.py`
- `python/commerce_mcp/tools/products/__init__.py`

---

## Step 3 — Write schemas.py

Pydantic v2 input models. One model per tool.

```python
# python/commerce_mcp/tools/<namespace>/schemas.py
from __future__ import annotations
from pydantic import BaseModel, Field


class ListXParams(BaseModel):
    id: str | None = Field(None, description="Filter by ID")
    limit: int = Field(20, ge=1, le=500, description="Maximum results (1–500)")
    offset: int | None = Field(None, ge=0, description="Number of items to skip")
    where: list[str] | None = Field(None, description="Query predicates")
    expand: list[str] | None = Field(None, description="Fields to expand")


class CreateXParams(BaseModel):
    name: str = Field(description="Resource name")
    # camelCase API fields need an alias:
    external_id: str | None = Field(None, alias="externalId", description="Optional external ID")
    model_config = {"populate_by_name": True}


class XUpdateAction(BaseModel):
    action: str
    model_config = {"extra": "allow"}  # open-ended update payloads


class UpdateXParams(BaseModel):
    id: str = Field(description="Resource ID")
    version: int = Field(description="Current version for optimistic locking")
    actions: list[XUpdateAction] = Field(description="Update actions to apply")
```

Rules:
- Every field has `Field(description="...")` 
- Optional fields default to `None` 
- camelCase API fields use `alias=` + `model_config = {"populate_by_name": True}`
- Update action payloads use `model_config = {"extra": "allow"}` to accept arbitrary action fields

---

## Step 4 — Write functions.py

Async handlers with concrete type annotations and context-conditional dispatch.

> **Invoke skill: `python-namespace-types`** — every handler must follow the annotated signature pattern.

> **Invoke skill: `python-function-logic-alignment`** — for TypeScript ports, replicate the exact id/key/where dispatch order, ownership verification, and context injection from all four scope files. This skill documents the common divergences found during the cart alignment and how to avoid them.

> **Invoke skill: `review-context-dispatch`** after writing — verify the dispatch faithfully mirrors the TypeScript `contextToXFunctionMapping`.

### Signature pattern (mandatory)

```python
# python/commerce_mcp/tools/<namespace>/functions.py
from __future__ import annotations
from typing import TYPE_CHECKING
from .schemas import ListXParams, CreateXParams, UpdateXParams
from ...shared.errors import SDKError, ContextError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext
```

Every function — public and private — uses this exact signature shape:

```python
async def list_x(
    params: ListXParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    try:
        query: dict = {"limit": params.limit}
        if params.id:
            query["where"] = f'id="{params.id}"'
        result = await api.get("/x", params=query)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("list x", e)
```

### Context-conditional dispatch (when the TypeScript mapping requires it)

```python
# Private scope-specific implementations:
async def _list_x_admin(params: ListXParams, api: "CommercetoolsAPI", ctx: "CTContext") -> str:
    try:
        result = await api.get("/x", params={"limit": params.limit})
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("list x", e)

async def _list_x_store(params: ListXParams, api: "CommercetoolsAPI", ctx: "CTContext") -> str:
    try:
        result = await api.get(f"/in-store/key={ctx.store_key}/x", params={"limit": params.limit})
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("list store x", e)


# Public dispatcher — mirrors contextToXFunctionMapping exactly:
async def list_x(params: ListXParams, api: "CommercetoolsAPI", ctx: "CTContext") -> str:
    if ctx.customer_id and ctx.business_unit_key:
        return await _list_x_as_associate(params, api, ctx)
    if ctx.customer_id:
        return await _list_x_customer(params, api, ctx)
    if ctx.store_key:
        return await _list_x_store(params, api, ctx)
    if ctx.is_admin:                              # explicit guard — never omit
        return await _list_x_admin(params, api, ctx)
    raise ContextError("list_x", "isAdmin, customerId, storeKey, or customerId+businessUnitKey")
```

**Critical rules for dispatch:**
- The `raise ContextError(...)` at the end is mandatory — never use a final `else` that calls the admin variant
- If `contextToXFunctionMapping` excludes `customerId`-only for write operations, the Python dispatcher must exclude it too
- Check TypeScript source: if a context combination maps to `{}`, Python must `raise ContextError`

### Write-only operations (no context dispatch needed)

Some tools always require `is_admin` and skip dispatch entirely:

```python
async def create_x(params: CreateXParams, api: "CommercetoolsAPI", ctx: "CTContext") -> str:
    if not ctx.is_admin:
        raise ContextError("create_x", "isAdmin")
    try:
        body = params.model_dump(by_alias=True, exclude_none=True)
        result = await api.post("/x", body=body)
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("create x", e)
```

---

## Step 5 — Write __init__.py and audit completeness

Only `ToolDefinition` declarations and `register_tool()` calls. No logic, no models, no handler code.

> **Invoke skill: `python-namespace-completeness`** after writing `__init__.py` to confirm every TypeScript tool is registered with all four scope implementations and the correct `actions` dict.

```python
# python/commerce_mcp/tools/<namespace>/__init__.py
from __future__ import annotations
from ..registry import ToolDefinition, register_tool
from .schemas import ListXParams, CreateXParams, UpdateXParams
from .functions import list_x, create_x, update_x

_X_TOOLS = [
    ToolDefinition(
        method="list_x",
        name="List X",
        description="List or search X resources.",
        parameters=ListXParams,
        handler=list_x,
        actions={"x": {"read": True}},
    ),
    ToolDefinition(
        method="create_x",
        name="Create X",
        description="Create a new X resource.",
        parameters=CreateXParams,
        handler=create_x,
        actions={"x": {"create": True}},
    ),
    ToolDefinition(
        method="update_x",
        name="Update X",
        description="Apply update actions to an existing X resource.",
        parameters=UpdateXParams,
        handler=update_x,
        actions={"x": {"update": True}},
    ),
]

for _tool in _X_TOOLS:
    register_tool(_tool)
```

The `actions` key must match the field name (or alias) in the `Actions` class from Step 1A.

---

## Step 6 — Wire into the registry

Open `python/commerce_mcp/tools/registry.py` and add the namespace to `_ensure_all_namespaces_imported()`:

```python
def _ensure_all_namespaces_imported() -> None:
    from . import (  # noqa: F401
        products,
        orders,
        carts,
        x,           # ← add your namespace here
    )
```

This is the only wiring change needed. The self-registration in `__init__.py` handles everything else — `build_server()`, the integration adapters, and `api.run()` all read from the default registry automatically.

---

## Step 7 — Write and run tests

> **Invoke skill: `python-namespace-tests`** — it is the authoritative guide for what to write, how to structure the three test sections, when to use `patch()`, and what the coverage checklist requires.

The short version of what is mandatory before the namespace is considered done:

1. Create the test directory:
   ```
   python/tests/tools/<namespace>/
   ├── __init__.py          ← empty, required for pytest discovery
   └── test_functions.py
   ```

2. The test file must cover three sections for every public handler:
   - **Functional** — correct API path, param passthrough, JSON output
   - **Security** — one route test per valid context variant; one `ContextError` + `assert_not_called()` per excluded context combination; one for empty `CTContext()`
   - **SDK errors** — `SDKError` wrapping on API failure

3. Run immediately after writing — do not proceed until all tests pass:
   ```bash
   cd python
   .venv/bin/pytest tests/tools/<namespace>/ -v
   ```

4. Then run the full suite to confirm no regressions:
   ```bash
   .venv/bin/pytest tests/ -q
   ```

---

## Step 8 — Verify dispatch security

Invoke `review-context-dispatch` on the new namespace. It will cross-check the Python dispatch chain against the TypeScript `contextToXFunctionMapping` and confirm every security boundary has test coverage.

A namespace is **not complete** until:
- All namespace tests pass
- The full test suite passes
- `review-context-dispatch` reports no issues

---

## Checklist

- [ ] `Actions` field added to `config.py`
- [ ] `schemas.py` created — models only, all fields have `Field(description=...)`
- [ ] `functions.py` created — handlers only, all parameters have concrete type annotations
- [ ] `__init__.py` created — ToolDefinition declarations + register_tool() only
- [ ] Namespace added to `_ensure_all_namespaces_imported()` in `registry.py`
- [ ] `tests/tools/<namespace>/__init__.py` created (empty)
- [ ] `tests/tools/<namespace>/test_functions.py` written (3 sections per handler)
- [ ] `pytest tests/tools/<namespace>/ -v` passes with 0 failures
- [ ] `pytest tests/ -q` passes — no regressions
- [ ] `review-context-dispatch` confirms dispatch faithfulness

## Skills referenced by this guide

| Step | Skill |
|------|-------|
| Step 1B — schema translation | `python-schema-alignment` |
| Step 1B — tool enumeration | `python-namespace-completeness` |
| Step 2 — file structure | `python-namespace-split` |
| Step 4 — type annotations | `python-namespace-types` |
| Step 4 — function logic alignment | `python-function-logic-alignment` |
| Step 4 — context dispatch security | `review-context-dispatch` |
| Step 5 — completeness audit | `python-namespace-completeness` |
| Step 7 — writing and running tests | `python-namespace-tests` |
| Step 8 — dispatch security audit | `review-context-dispatch` |
| Step 1B — TypeScript translation | `python-fastmcp` |
