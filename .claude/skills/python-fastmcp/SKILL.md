---
name: python-fastmcp
description: Scaffold or extend the Python fastMCP server under `python/` for the Commercetools MCP project. Use this skill whenever the user wants to add a new namespace to the Python server, convert TypeScript tool definitions to Python, implement a new Python tool handler, create Pydantic schemas from Zod definitions, or wire up a new namespace into the registry and server. Trigger on phrases like "add Python support for X", "scaffold X namespace", "implement X in Python", "port X tools to Python", or "create Python handler for X".
---

# Scaffold Python fastMCP Server

Given a TypeScript namespace (e.g. `typescript/src/shared/products/`) or a list of namespaces, produce the full Python equivalent and wire it into the server.

## What to produce for each namespace

For each namespace, create or update these files:

```
python/commerce_mcp/tools/<namespace>/
├── __init__.py       ← ToolDefinition declarations + register_tool() calls
├── schemas.py        ← Pydantic v2 models (translated from Zod)
└── functions.py      ← async handler functions with context-conditional dispatch

python/tests/tools/<namespace>/
└── test_functions.py ← unit tests (functional + security)
```

Also update:
- `python/commerce_mcp/tools/registry.py` — add namespace to `_ensure_all_namespaces_imported()`
- `python/commerce_mcp/server.py` — add `if _any("<ns>"):` mount block in `_mount_namespaces()`
- `python/commerce_mcp/config.py` — add `Actions` field if the namespace is missing

## Step 1: Read the TypeScript source

For each namespace, read all three TypeScript files before writing any Python:
- `typescript/src/shared/<namespace>/tools.ts` — tool names, descriptions, actions
- `typescript/src/shared/<namespace>/parameters.ts` — Zod schemas → Pydantic models
- `typescript/src/shared/<namespace>/functions.ts` — **read `contextToXFunctionMapping` carefully** — this is the security contract

## Step 2: Translate schemas (schemas.py)

Convert Zod to Pydantic v2:
- Every field gets `Field(description="...")`
- Optional fields: `str | None = Field(None, description="...")`
- camelCase API fields: use `alias=` + `model_config = {"populate_by_name": True}`
- Open-ended update objects: `model_config = {"extra": "allow"}`

## Step 3: Write handler functions (functions.py)

### Handler signature
```python
async def my_tool(params: MyParams, api: "CommercetoolsAPI", ctx: "CTContext") -> str:
    try:
        result = await api.get("/path", params={...})
        return transform_tool_output(result)
    except Exception as e:
        raise SDKError("operation name", e)
```

### Context-conditional dispatch — the most important part

The TypeScript `contextToXFunctionMapping` is the authoritative security contract. Map it faithfully to Python `if/elif` chains:

```python
async def read_order(params, api, ctx):
    if ctx.customer_id and ctx.business_unit_key:
        return await _read_order_as_associate(params, api, ctx)
    if ctx.customer_id:
        return await _read_order_customer(params, api, ctx)
    if ctx.store_key:
        return await _read_order_store(params, api, ctx)
    if ctx.is_admin:                          # explicit guard — never omit
        return await _read_order_admin(params, api, ctx)
    raise ContextError("read_order", "isAdmin, customerId, storeKey, or customerId+businessUnitKey")
```

**Critical mistakes to avoid:**
- Falling through to admin as the final `else` — silently grants admin access
- Omitting the `is_admin` guard — same result
- Allowing `customerId`-only for write operations when the TypeScript mapping excludes it

If `contextToXFunctionMapping` returns `{}` for a context combination, the Python handler **must** raise `ContextError` — never silently fall through.

**Typical per-namespace dispatch rules** (always verify against TypeScript source):

| Namespace | No-context result | Notes |
|-----------|------------------|-------|
| `orders` | `ContextError` | customer-only → read only; write needs store/admin/associate |
| `carts` | `ContextError` | all four ops need explicit context |
| `products` | `ContextError` for writes | `create`/`update` require `is_admin` |

## Step 4: Write __init__.py

Only `ToolDefinition` declarations — no FastMCP, no Context, no framework imports:

```python
from ..registry import ToolDefinition, register_tool
from .schemas import MyParams
from .functions import my_tool

_TOOLS = [
    ToolDefinition(
        method="my_tool",
        name="my_tool",
        description="...",
        parameters=MyParams,
        handler=my_tool,
        actions={"resource": {"read": True}},
    ),
]
for _tool in _TOOLS:
    register_tool(_tool)
```

Match the `actions` field exactly from the TypeScript source:
- View only: `actions={"products": {"read": True}}`
- Write only: `actions={"products": {"create": True}}`
- Combined: `actions={"order": {"read": True, "create": True}}`

## Step 5: Write tests (test_functions.py)

Every namespace test file must cover both functional correctness and security:

```python
# ── Functional ────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_list_X_calls_get(mock_api, admin_context):
    result = await list_x(ListXParams(), mock_api, admin_context)
    mock_api.get.assert_called_once()
    assert "expected-value" in result

@pytest.mark.asyncio
async def test_list_X_raises_sdk_error(mock_api, admin_context):
    mock_api.get.side_effect = Exception("500")
    with pytest.raises(SDKError, match="Failed to list x"):
        await list_x(ListXParams(), mock_api, admin_context)

# ── Security: context dispatch ─────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_create_X_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()  # no is_admin, no customer_id, no store_key
    with pytest.raises(ContextError, match="create_x"):
        await create_x(CreateXParams(...), mock_api, ctx)
    mock_api.post.assert_not_called()  # verify no API call was made

@pytest.mark.asyncio
async def test_create_X_raises_context_error_for_customer_only(mock_api):
    ctx = CTContext(customer_id="cust-1")  # valid for reads, not for writes
    with pytest.raises(ContextError, match="create_x"):
        await create_x(CreateXParams(...), mock_api, ctx)
    mock_api.post.assert_not_called()
```

Write one security test per invalid context combination that the TypeScript mapping excludes.

## Reference files

When in doubt about structure, read:
- `python/commerce_mcp/tools/products/` — reference implementation
- `python/commerce_mcp/tools/orders/__init__.py` — reference for context dispatch

## Running tests

```bash
cd python
pip install -e ".[dev]"
pytest tests/tools/<namespace>/
```
