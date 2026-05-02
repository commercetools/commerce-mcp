# Skill: Python Function Logic Alignment with TypeScript

## Problem

Python handler functions contain simplified logic that doesn't match the TypeScript scope functions. Typical divergences found in carts:

1. **Missing id/key branches**: Python had a single `where` query; TypeScript checks `id` first, then `key`, then falls back to query.
2. **Wrong endpoint for customer context**: Python used `/me/carts`; TypeScript uses `/carts?where=customerId="..."` with admin API.
3. **Missing store injection**: Python didn't inject `store` into create cart body for store context; TypeScript does.
4. **Missing ownership verification**: Python skipped the `verifyCartBelongsToCustomer` / `verifyCartBelongsToStore` GET calls.
5. **Missing `storeKey` param support**: TypeScript's admin `queryCarts` routes through `/in-store/key={storeKey}` if `params.storeKey` is set; Python ignored it.
6. **Missing associate id/key dispatch**: Python only queried; TypeScript dispatches to `readAssociateCartById` or `readAssociateCartByKey` when those params are present.

## Rule

**The TypeScript scope files are the authoritative logic source.** For each namespace, read all four scope files and replicate the logic in Python:

- `admin.functions.ts` → `_*_admin` handlers
- `customer.functions.ts` → `_*_customer` handlers
- `store.functions.ts` → `_*_store` handlers
- `as-associate.functions.ts` → `_*_as_associate` handlers

## How to Apply

### 1. Read the TypeScript scope files

For namespace `<N>`:
```
typescript/src/shared/<N>/admin.functions.ts
typescript/src/shared/<N>/customer.functions.ts
typescript/src/shared/<N>/store.functions.ts
typescript/src/shared/<N>/as-associate.functions.ts
typescript/src/shared/<N>/base.functions.ts   ← understand the helper paths
```

### 2. Translate each exported function to Python private helpers

Each TypeScript `export const readXxx = async (apiRoot, context, params)` becomes `async def _read_xxx_<scope>(params, api, ctx)`.

### 3. Replicate the conditional dispatch order exactly

Copy the `if (params.id)` / `if (params.key)` / `if (params.customerId)` / `if (params.where)` branching verbatim. These priority rules prevent subtle bugs.

### 4. Replicate ownership verification

Customer context: fetch the cart and verify `cart.customerId === ctx.customer_id`.
Store context: fetch the cart and verify `cart.store?.key === ctx.store_key`.

```python
async def _verify_cart_belongs_to_customer(api, customer_id, cart_id=None, cart_key=None):
    cart = await api.get(f"/carts/{cart_id}") if cart_id else await api.get(f"/carts/key={cart_key}")
    return cart.get("customerId") == customer_id
```

### 5. Use `model_dump(by_alias=True, exclude_none=True)` for request bodies

Do not hand-pick fields. Dump the entire params model:
```python
body = params.model_dump(by_alias=True, exclude_none=True)
```

Then inject context-specific overrides after dumping:
```python
body["customerId"] = ctx.customer_id          # customer context
body["store"] = {"key": ctx.store_key, "typeId": "store"}  # store context
body["businessUnit"] = {"typeId": "business-unit", "key": ctx.business_unit_key}  # associate
```

### 6. Replicate in-store endpoint logic for replicate and update

TypeScript uses `/in-store/key={storeKey}/carts/replicate` and `/in-store/key={storeKey}/carts/{id}` when `storeKey` is present. Python must do the same:

```python
prefix = f"/in-store/key={store_key}" if store_key else ""
result = await api.post(f"{prefix}/carts/replicate", body=body)
```

### 7. Associate paths

All associate operations use the base path:
```python
base = f"/as-associate/{ctx.customer_id}/in-business-unit/key={ctx.business_unit_key}"
```

Append `/carts/{id}`, `/carts/key={key}`, `/carts`, or `/carts/replicate` as needed.

### 8. Serialize actions

```python
def _serialize_actions(actions: list) -> list[dict]:
    return [a.model_dump(by_alias=True, exclude_none=True) for a in actions]
```

## Checklist Before Declaring Done

- [ ] Every TypeScript scope function has a corresponding Python `_*_<scope>` handler
- [ ] id/key/customerId/where dispatch order matches TypeScript for all read functions
- [ ] Customer and store functions verify ownership before mutating
- [ ] Create functions inject the right context fields (customerId, store, businessUnit)
- [ ] Replicate functions use `/carts/replicate` endpoint (optionally prefixed by in-store path)
- [ ] Update functions support both id and key with optional storeKey
- [ ] Associate functions use the full `/as-associate/.../in-business-unit/.../...` path
- [ ] All tests pass: `python3 -m pytest tests/`
