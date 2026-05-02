# Skill: Python Schema Alignment with TypeScript

## Problem

Python Pydantic schemas drift from the TypeScript Zod schemas in `typescript/src/shared/<namespace>/parameters.ts`. This drift causes Python tools to reject or silently drop parameters that TypeScript accepts, making the Python server a subset of the TypeScript server.

**Observed gap (carts):**
- TypeScript `readCartParameters` had 9 fields; Python `ReadCartParams` had 2
- TypeScript `createCartParameters` had 20+ fields; Python `CreateCartParams` had 2
- TypeScript had `replicateCartParameters`; Python had no such class at all

## Rule

**The TypeScript `parameters.ts` file is the authoritative schema source.** Every parameter that TypeScript accepts must appear in the Python schema with the correct type, alias, and default.

## How to Apply

### 1. Locate the TypeScript parameters file
```
typescript/src/shared/<namespace>/parameters.ts
```
Read it in full. Each `z.object({...})` export is one tool's parameters.

### 2. Map Zod types → Pydantic types

| Zod | Pydantic |
|-----|---------|
| `z.string()` | `str` |
| `z.string().optional()` | `str \| None = Field(None, ...)` |
| `z.number().int()` | `int` |
| `z.boolean()` | `bool` |
| `z.array(z.string())` | `list[str]` |
| `z.enum(["A","B"])` | `Literal["A","B"]` |
| `z.object({...})` | Nested `BaseModel` subclass |
| `.optional()` | `= Field(None, ...)` |
| `.default(x)` | `= Field(x, ...)` |
| `.min(n)` / `.max(n)` | `ge=n` / `le=n` in Field |

### 3. Translate camelCase → snake_case + alias

Every TypeScript camelCase parameter needs:
- Python field name in `snake_case`
- `alias="camelCase"` in Field

Example:
```python
# TypeScript: customerEmail: z.string().optional()
customer_email: str | None = Field(None, alias="customerEmail", description="...")
```

### 4. Add `model_config = {"populate_by_name": True}` to every model

This lets callers use either snake_case or camelCase.

### 5. Create sub-models for nested objects

If TypeScript uses an inline `z.object({typeId, id})`, create a named Python sub-model:
```python
class CartReference(BaseModel):
    id: str = Field(description="...")
    type_id: Literal["cart"] = Field("cart", alias="typeId")
    model_config = {"populate_by_name": True}
```

### 6. Preserve default values exactly

- `z.number().default(10)` → `int = Field(10, ...)`
- `z.array(...).default([])` → `list[...] = Field(default_factory=list, ...)`
- `z.boolean().default(false)` → `bool = False`

### 7. Check for new top-level exports (missing tools)

If TypeScript exports `replicateCartParameters` but Python has no `ReplicateCartParams`, that tool is completely missing. Create the Pydantic model and note that a new tool handler is needed.

## Checklist Before Declaring Done

- [ ] Every Zod export in `parameters.ts` has a corresponding Pydantic class
- [ ] Every field in each Zod schema has a corresponding Pydantic field
- [ ] All camelCase Zod fields have `alias=` in Python
- [ ] All nested `z.object({})` are extracted to named sub-models
- [ ] `model_config = {"populate_by_name": True}` on all models
- [ ] New classes noted as requiring handler + registration
- [ ] All tests pass: `python3 -m pytest tests/`
