---
name: sync-prompts
description: Port TypeScript tool-description prompts to Python for the Commercetools MCP project. Use this skill whenever a Python namespace is missing a prompts.py file, tool descriptions are short inline one-liners instead of rich prompt strings, or the user wants to sync descriptions from TypeScript to Python. Trigger on phrases like "sync prompts", "add prompts.py", "fix tool descriptions", "port prompts to Python", "missing prompts", "descriptions are too short", or any mention of a namespace whose __init__.py has inline description strings instead of imported constants. Also trigger when the user mentions that the Python and TypeScript descriptions are out of sync.
---

# Sync TypeScript Prompts to Python

Each TypeScript namespace under `typescript/src/shared/<namespace>/` has a `prompts.ts` file that exports rich, multi-line description strings used as tool descriptions. The Python namespaces under `python/commerce_mcp/tools/<namespace>/` should mirror this pattern with a `prompts.py` file.

This skill creates `prompts.py` and updates `__init__.py` for one or more Python namespaces.

## Step 1: Identify which namespaces need work

If the user named specific namespace(s), use those. Otherwise, scan for all Python namespaces missing `prompts.py`:

```bash
for d in python/commerce_mcp/tools/*/; do
  [ -f "$d/__init__.py" ] && [ ! -f "$d/prompts.py" ] && echo "$(basename $d)"
done
```

Confirm the list with the user if it's more than a handful. For a single named namespace, proceed immediately.

## Step 2: Resolve the TypeScript namespace name

Python uses `snake_case`, TypeScript uses `kebab-case` — but some names also differ:

| Python namespace     | TypeScript namespace      |
|----------------------|---------------------------|
| `carts`              | `cart`                    |
| `orders`             | `order`                   |
| `order_edit`         | *(no TS counterpart)*     |
| anything else        | replace `_` with `-`      |

If the TypeScript directory doesn't exist, skip that namespace and note it to the user.

## Step 3: Read the TypeScript prompts.ts

Read `typescript/src/shared/<ts-namespace>/prompts.ts` in full. It exports constants that are TypeScript template literals (backtick strings). The constant names may be either camelCase (`readCategoryPrompt`) or UPPER_SNAKE_CASE (`READ_CUSTOMER_GROUP_PROMPT`) — both styles exist in the codebase.

## Step 4: Create prompts.py

Create `python/commerce_mcp/tools/<py-namespace>/prompts.py` with:

- One constant per exported prompt from the TS file
- Constant names in `UPPER_SNAKE_CASE` (Python convention), regardless of the TS style
  - `readCategoryPrompt` → `READ_CATEGORY_PROMPT`
  - `READ_CUSTOMER_GROUP_PROMPT` → stays `READ_CUSTOMER_GROUP_PROMPT`
- Content copied verbatim from the TS template literal — same text, just in Python triple-quoted strings
- Escaped quotes in TS (`\\"`) should become regular escaped quotes in Python (`\"` or use the string naturally)
- No extra imports, no `__all__`, no `PROMPTS` dict — just the bare constants

**Template:**
```python
READ_<NAMESPACE>_PROMPT = """
<content from TS template literal>
"""

CREATE_<NAMESPACE>_PROMPT = """
<content from TS template literal>
"""

UPDATE_<NAMESPACE>_PROMPT = """
<content from TS template literal>
"""
```

## Step 5: Update __init__.py

In `python/commerce_mcp/tools/<py-namespace>/__init__.py`:

1. Add an import line after the existing imports:
   ```python
   from .prompts import CREATE_<NS>_PROMPT, READ_<NS>_PROMPT, UPDATE_<NS>_PROMPT
   ```
   Import only the constants that actually exist in prompts.py.

2. Replace each inline `description="..."` or `description=(...)` with the corresponding constant:
   ```python
   description=READ_<NS>_PROMPT,
   ```

Match the tool method name to the right constant — `read_*` tools get `READ_*_PROMPT`, `create_*` get `CREATE_*_PROMPT`, etc. For method names that don't follow read/create/update (e.g., `replicate_cart`, `list_products`), look at the TS `tools.ts` to see which prompt constant it uses, or use the closest semantic match from the prompts.py you just created.

## Step 6: Verify

After writing both files, do a quick sanity check:
- `prompts.py` exists and has the expected constants
- `__init__.py` imports them and each `description=` field references a constant (not an inline string)
- Python can at least parse the file: `python -c "import python.commerce_mcp.tools.<namespace>"`

If the namespace has no TypeScript counterpart with a `prompts.ts`, note this to the user and leave the inline descriptions as-is.
