---
name: python-namespace-tests
description: Write and run the complete test suite for a Python namespace under python/tests/tools/<namespace>/. Use this skill whenever tests need to be written for a new or existing namespace, or when checking test coverage. Trigger on phrases like "write tests for namespace", "add tests for X", "test the X namespace", "namespace tests missing", "run namespace tests", "check test coverage for X".
---

# Writing Tests for a Python Namespace

Every namespace requires a test file at:

```
python/tests/tools/<namespace>/
├── __init__.py          ← empty, required for pytest discovery
└── test_functions.py    ← all handler tests
```

Both files must be created. If the `__init__.py` is missing, pytest will silently skip the directory.

---

## Imports

```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from commerce_mcp.tools.<namespace>.functions import list_x, create_x, update_x
from commerce_mcp.tools.<namespace>.functions import _list_x_admin, _list_x_store  # private fns, if needed
from commerce_mcp.tools.<namespace>.schemas import ListXParams, CreateXParams, UpdateXParams
from commerce_mcp.config import CTContext
from commerce_mcp.shared.errors import SDKError, ContextError
```

Rules:
- Always import from `.functions` and `.schemas` directly — never from the namespace `__init__`
- Import private functions (`_*`) only when you need to test implementation details of a specific scope variant
- `patch` is only needed for testing dispatch routing in complex namespaces (see below)

---

## The mock_api fixture

Define a local `mock_api` fixture in each test file. Do not use the one from `conftest.py` — the local fixture controls return values precisely.

```python
@pytest.fixture
def mock_api():
    api = MagicMock()
    api.get = AsyncMock(return_value={"count": 1, "results": [{"id": "x-1"}]})
    api.post = AsyncMock(return_value={"id": "x-1", "version": 2})
    return api
```

Set `return_value` to realistic API response shapes — the test assertions will check against these.

---

## The three mandatory test sections

### Section 1 — Functional: verify the API call is made correctly

Test that each public handler calls the right endpoint with the right parameters and returns JSON output.

```python
# ── Functional ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_x_calls_correct_path(mock_api):
    ctx = CTContext(is_admin=True)
    result = await list_x(ListXParams(), mock_api, ctx)
    mock_api.get.assert_called_once()
    assert mock_api.get.call_args[0][0] == "/x"
    assert '"id"' in result  # output is JSON


@pytest.mark.asyncio
async def test_list_x_applies_limit(mock_api):
    ctx = CTContext(is_admin=True)
    await list_x(ListXParams(limit=5), mock_api, ctx)
    params = mock_api.get.call_args[1]["params"]
    assert params["limit"] == 5


@pytest.mark.asyncio
async def test_list_x_applies_id_filter(mock_api):
    ctx = CTContext(is_admin=True)
    await list_x(ListXParams(id="x-42"), mock_api, ctx)
    params = mock_api.get.call_args[1]["params"]
    assert 'id="x-42"' in params.get("where", "")


@pytest.mark.asyncio
async def test_create_x_sends_correct_body(mock_api):
    ctx = CTContext(is_admin=True)
    await create_x(CreateXParams(name="test"), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["name"] == "test"


@pytest.mark.asyncio
async def test_update_x_sends_version_and_actions(mock_api):
    ctx = CTContext(is_admin=True)
    await update_x(UpdateXParams(id="x-1", version=3, actions=[{"action": "setKey", "key": "k"}]), mock_api, ctx)
    body = mock_api.post.call_args[1]["body"]
    assert body["version"] == 3
    assert body["actions"][0]["action"] == "setKey"
```

### Section 2 — Security: context dispatch routing

Test every valid routing branch AND every invalid context combination.

#### 2a — Route tests (one per valid context path)

```python
# ── Security: context dispatch ─────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_x_routes_to_admin(mock_api):
    ctx = CTContext(is_admin=True)
    await list_x(ListXParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/x"


@pytest.mark.asyncio
async def test_list_x_routes_to_store(mock_api):
    ctx = CTContext(store_key="eu-store")
    await list_x(ListXParams(), mock_api, ctx)
    assert "/in-store/key=eu-store/x" in mock_api.get.call_args[0][0]


@pytest.mark.asyncio
async def test_list_x_routes_to_customer(mock_api):
    ctx = CTContext(customer_id="cust-1")
    await list_x(ListXParams(), mock_api, ctx)
    assert mock_api.get.call_args[0][0] == "/me/x"


@pytest.mark.asyncio
async def test_list_x_routes_to_associate(mock_api):
    ctx = CTContext(customer_id="cust-1", business_unit_key="bu-1")
    await list_x(ListXParams(), mock_api, ctx)
    path = mock_api.get.call_args[0][0]
    assert "as-associate/cust-1" in path
    assert "in-business-unit/key=bu-1" in path
```

Only include tests for the context variants that the TypeScript `contextToXFunctionMapping` supports. Skip variants the mapping excludes.

#### 2b — ContextError tests (one per invalid combination)

Every public handler that has a `raise ContextError(...)` guard needs at least these two tests:

```python
@pytest.mark.asyncio
async def test_list_x_raises_context_error_with_no_context(mock_api):
    ctx = CTContext()  # no is_admin, no customer_id, no store_key
    with pytest.raises(ContextError, match="list_x"):
        await list_x(ListXParams(), mock_api, ctx)
    mock_api.get.assert_not_called()  # verify no API call was made
```

For write operations that exclude customer-only context:

```python
@pytest.mark.asyncio
async def test_create_x_raises_context_error_for_customer_only(mock_api):
    ctx = CTContext(customer_id="cust-1")  # valid for reads, not for writes
    with pytest.raises(ContextError, match="create_x"):
        await create_x(CreateXParams(name="test"), mock_api, ctx)
    mock_api.post.assert_not_called()
```

**`assert_not_called()` is mandatory on every ContextError test.** It proves the guard fires before any I/O, not after.

### Section 3 — SDK errors: exception wrapping

Test that every public handler wraps exceptions as `SDKError`.

```python
# ── SDK errors ─────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_x_raises_sdk_error_on_failure(mock_api):
    mock_api.get.side_effect = Exception("500 Server Error")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to list x"):
        await list_x(ListXParams(), mock_api, ctx)


@pytest.mark.asyncio
async def test_create_x_raises_sdk_error_on_failure(mock_api):
    mock_api.post.side_effect = Exception("400 Bad Request")
    ctx = CTContext(is_admin=True)
    with pytest.raises(SDKError, match="Failed to create x"):
        await create_x(CreateXParams(name="test"), mock_api, ctx)
```

The `match=` string must equal `"Failed to <verb> <resource>"` — this mirrors the first argument passed to `SDKError(...)` in `functions.py`.

---

## When to use patch() for dispatch tests

Use `patch()` when a namespace has many private scope variants and you want to assert that the dispatcher picks the right one without re-testing the private function's API call details. This is the pattern used in `orders`.

```python
@pytest.mark.asyncio
async def test_list_x_dispatches_to_admin(mock_api):
    ctx = CTContext(is_admin=True)
    with patch(
        "commerce_mcp.tools.<namespace>.functions._list_x_admin",
        new=AsyncMock(return_value="admin result"),
    ) as mock_fn:
        await list_x(ListXParams(), mock_api, ctx)
        mock_fn.assert_called_once()
```

Use the **full dotted module path** `commerce_mcp.tools.<namespace>.functions._<fn>` as the patch target — not the import alias.

When NOT to use patch(): if the route tests in Section 2a already verify the correct path via `mock_api.get.call_args`, patching is redundant. Prefer the simpler direct approach (carts pattern).

---

## Determining which tests to write

Read `functions.py` for the namespace and build a matrix:

| Handler | Context variants (from dispatch chain) | Excluded contexts |
|---------|---------------------------------------|-------------------|
| `list_x` | admin, store, customer, associate | none |
| `create_x` | admin, store, associate | customer-only |
| `update_x` | admin, store, associate | customer-only |

For each row: one route test per valid variant + one ContextError test per excluded variant + one ContextError test for empty context + one SDKError test.

---

## Running the tests

Always run after writing. A namespace is not done until all tests pass:

```bash
cd python
.venv/bin/pytest tests/tools/<namespace>/ -v
```

To run the full suite and confirm no regressions:

```bash
cd python
.venv/bin/pytest tests/ -q
```

Expected output: all tests pass, no warnings about missing files or import errors.

---

## Test coverage checklist

For each public handler in `functions.py`:

- [ ] At least one functional test (correct API path + JSON output)
- [ ] At least one param-passthrough test (limit, filter, id)
- [ ] One route test per valid context variant
- [ ] One `ContextError` test for `CTContext()` (no context), with `assert_not_called()`
- [ ] One `ContextError` test per excluded context combination, with `assert_not_called()`
- [ ] One `SDKError` test per handler
- [ ] Tests directory has an `__init__.py`
- [ ] `pytest tests/tools/<namespace>/ -v` passes with 0 failures
