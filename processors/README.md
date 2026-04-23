# @commercetools/processors

**Output processors** for MCP-style tool payloads and similar JSON: declarative **field filtering** (drop keys) and **redaction** (mask values, including query strings inside URL-shaped strings), plus **transform** helpers that turn structured tool results into **tabular** or **JSON** text for LLMs.

The library is **domain-agnostic**: you pass plain objects/arrays/primitives (anything you would normally `JSON.parse`). Rules use **dot paths** from the root of the value you pass into `filterFields`.

---

## Install

```bash
npm add @commercetools/processors
```

or

```
yarn add @commercetools/processors
```

You can also use `npm` or `yarn` with the same package name.

**Runtime:** Node **≥ 18**.

---

## Package layout (what each area does)

| Area                                                                                       | Responsibility                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`FieldFilteringHandler`**                                                                | Walks a value recursively. On **objects**, applies rules per key path; on **arrays**, maps each element (path rules do not add array indices—see below). On **strings**, if the string is a **valid URL**, runs the same rule logic on **query parameter names**; other strings are left as-is. |
| **`FieldFilteringManagerConfig`**                                                          | Declarative lists of rules (`paths`, `properties`, `includes`) plus optional **whitelist** paths and custom **redaction placeholder** strings for JSON vs URL query values.                                                                                                                     |
| **`FieldFilteringManager`**                                                                | Interface: `filterFields` + `filterUrlFields`. Swap in your own implementation (e.g. remote policy) and use **`isFieldFilteringManager`** at runtime to tell **config** from **instance**.                                                                                                      |
| **`transformToolOutput`**                                                                  | Converts `data` into a **string**: default **`tabular`** (indented, property names via `transformPropertyName`, booleans as `Yes`/`No`, tables for arrays of objects where applicable); optional **`json`** stringifies JSON.                                                                   |
| **`transformPropertyName`**                                                                | Turns identifiers like `orderLineId` or `order_line_id` into human-oriented labels (used internally by tabular output and titles).                                                                                                                                                              |
| **`urlHelpers`**                                                                           | **`isValidUrl`**, **`normaliseUrl`**, **`generateQueryString`** — small utilities shared with URL handling in the handler.                                                                                                                                                                      |
| **`defaultFilteringRules`**, **`defaultJsonRedactionText`**, **`defaultUrlRedactionText`** | Defaults for redaction placeholders when you omit them in config (`[REDACTED]` / `REDACTED`).                                                                                                                                                                                                   |

---

## Usage overview

```ts
import {
  FieldFilteringHandler,
  type FieldFilteringManagerConfig,
  type FieldFilteringRule,
  type FieldFilteringManager,
  isFieldFilteringManager,
  defaultFilteringRules,
  defaultJsonRedactionText,
  defaultUrlRedactionText,
  transformToolOutput,
  transformPropertyName,
  isValidUrl,
  generateQueryString,
  normaliseUrl,
} from '@commercetools/processors';
```

Typical flow: **clone** (or parse fresh JSON) → **`new FieldFilteringHandler(config).filterFields(data)`** → optionally **`transformToolOutput({ data: safe, ... })`** before sending to a model, agent or client.

---

## Field filtering and redaction

### Why cloning matters

`filterFields` **mutates** object graphs in place (delete keys, replace values). If the same object is referenced elsewhere (cache, logger, retry), those views change too. Always **`structuredClone`**, `JSON.parse(JSON.stringify(x))`, or another **deep copy** before filtering when you need isolation.

### How rules are evaluated (mental model)

For each object key, the handler builds a **path** like `parent.child.leaf`. Then, for **filter** or **redact** separately:

1. **Whitelist** — if the current path matches a whitelist entry, **no** filter/redact on that path from the declarative lists (exact / case rules as in tests).
2. **`paths`** — full path match; **`filter`** removes that property; **`redact`** replaces the **entire value at that path** with `jsonRedactionText` (the subtree is not traversed further for path-redact in the same way as nested keys—see handler tests for edge cases).
3. **`properties`** — compares the **last segment** of the path (the key name) to each rule.
4. **`includes`** — substring match on that **last segment** (e.g. `secret` matches `clientSecret` when case-insensitive).

**Arrays:** elements are processed with the **same** `currentPath` as the parent array (no `.0`, `.1` in the path). Rules keyed on **property names** or **`includes`** still apply inside objects **inside** arrays; **full `paths`** rules that assume `items.0.field` will **not** match the stock handler—use **`properties`/`includes`** or a custom **`FieldFilteringManager`**.

### `FieldFilteringManagerConfig` (reference)

Every top-level field is **optional**; supply only what you need.

| Option                  | Type                                 | Role                                                                                                                                                                                                                                           |
| ----------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`paths`**             | `FieldFilteringRule[]`               | Match the **full dot-path** from the root of the value passed to `filterFields`. `type: 'filter'` removes the key. `type: 'redact'` replaces that node’s value with `jsonRedactionText` (often a whole object becomes the placeholder string). |
| **`properties`**        | `FieldFilteringRule[]`               | Match the **leaf key name** at **any** depth (e.g. every `token` key).                                                                                                                                                                         |
| **`includes`**          | `FieldFilteringRule[]`               | Match when the leaf name **contains** `rule.value` (substring), with optional case folding per rule.                                                                                                                                           |
| **`whitelistPaths`**    | `Omit<FieldFilteringRule, 'type'>[]` | Paths that **suppress** filter/redact from the lists above when the evaluated path matches (see tests for exact vs case-insensitive behaviour).                                                                                                |
| **`jsonRedactionText`** | `string?`                            | Replacement for redacted **JSON** values (default **`[REDACTED]`**).                                                                                                                                                                           |
| **`urlRedactionText`**  | `string?`                            | Replacement for redacted **URL query** values (default **`REDACTED`**).                                                                                                                                                                        |

### `FieldFilteringRule`

| Field               | Meaning                                                                                      |
| ------------------- | -------------------------------------------------------------------------------------------- |
| **`value`**         | Path, leaf name, or substring needle (depending on which array the rule sits in).            |
| **`caseSensitive`** | If `false`, comparisons use case-insensitive matching where implemented.                     |
| **`type`**          | **`'filter'`** — remove key (or query param). **`'redact'`** — keep key/name, replace value. |

### `FieldFilteringManager` and `isFieldFilteringManager`

Use a **custom class** that implements `filterFields` / `filterUrlFields` when you need logging, remote policy, or different path semantics than `FieldFilteringHandler`. **`isFieldFilteringManager(x)`** returns true when `x` has both methods (duck typing), so you can accept **either** plain **config** or a ready-made **manager** from configuration:

```ts
import {
  FieldFilteringHandler,
  isFieldFilteringManager,
  type FieldFilteringManager,
  type FieldFilteringManagerConfig,
} from '@commercetools/processors';

function getHandler(
  input: FieldFilteringManagerConfig | FieldFilteringManager
): FieldFilteringManager {
  if (isFieldFilteringManager(input)) {
    return input;
  }
  return new FieldFilteringHandler(input);
}

const handler = getHandler({
  properties: [{value: 'x', caseSensitive: true, type: 'filter'}],
});
const out = handler.filterFields({x: 1, y: 2});

// Expected `out`:
// { y: 2 }
```

---

## Examples: `FieldFilteringHandler` on JSON

```ts
import {
  FieldFilteringHandler,
  type FieldFilteringManagerConfig,
} from '@commercetools/processors';

const config: FieldFilteringManagerConfig = {
  // Full path: redact only this branch's value (here the string becomes "[REDACTED]")
  paths: [
    {value: 'credentials.accessToken', caseSensitive: true, type: 'redact'},
  ],
  // Any key named apiKey (any casing): remove entirely
  properties: [{value: 'apiKey', caseSensitive: false, type: 'filter'}],
  // Any leaf name containing "secret": redact value, keep key
  includes: [{value: 'secret', caseSensitive: false, type: 'redact'}],
};

const toolResult = {
  credentials: {accessToken: 'tok', refresh: 'r'},
  apiKey: 'k',
  clientSecret: 's',
};

const safe = structuredClone(toolResult);
new FieldFilteringHandler(config).filterFields(safe);

// Expected `safe` (JSON-serialized for clarity):
// {"credentials":{"accessToken":"[REDACTED]","refresh":"r"},"clientSecret":"[REDACTED]"}
// - paths: credentials.accessToken value replaced; refresh unchanged
// - properties: apiKey key removed
// - includes: clientSecret value redacted (leaf name contains "secret")
```

---

## Examples: `filterUrlFields` (query string)

Rules use the same machinery: **filter** drops a query pair; **redact** keeps the name and sets the value to **`urlRedactionText`**.

```ts
import {FieldFilteringHandler} from '@commercetools/processors';

const redacted = new FieldFilteringHandler({
  properties: [{value: 'sig', caseSensitive: false, type: 'redact'}],
}).filterUrlFields('https://x.example/y?sig=abc123&ok=1');

// Expected `redacted`:
// "https://x.example/y?sig=REDACTED&ok=1"

const stripped = new FieldFilteringHandler({
  properties: [{value: 'token', caseSensitive: false, type: 'filter'}],
}).filterUrlFields('https://api.example.com/callback?token=abc&ok=1');

// Expected `stripped`:
// "https://api.example.com/callback?ok=1"
```

---

## Examples: `transformToolOutput`

`format` defaults to **`'tabular'`**. With a **`title`**, the title is uppercased (after `transformPropertyName`) and used as a heading. Booleans become **`Yes`/`No`**; nested objects get indented lines; empty plain objects yield **`no properties`** (with optional title prefix—see below).

### Tabular, with title

```ts
import {transformToolOutput} from '@commercetools/processors';

const text = transformToolOutput({
  data: {orderId: '123', total: {currency: 'EUR', centAmount: 4200}},
  title: 'Order summary',
  format: 'tabular',
});

// Expected `text` (string; newlines shown as \n here):
// "ORDER SUMMARY\nOrder Id: 123\nTotal:\n\tCurrency: EUR\n\tCent Amount: 4200"
```

### Tabular, no title

```ts
const plain = transformToolOutput({
  data: {a: 1},
  format: 'tabular',
});

// Expected `plain`:
// "A: 1"
```

### Tabular, empty object

```ts
const empty = transformToolOutput({data: {}, format: 'tabular'});

// Expected `empty`:
// "no properties"
```

### Tabular, boolean

```ts
const stock = transformToolOutput({
  data: {inStock: true},
  format: 'tabular',
});

// Expected `stock`:
// "In Stock: Yes"
```

### JSON format

With **`format: 'json'`**, output is `JSON.stringify` of the data (or a single-key object whose key is the transformed title when `title` is set).

```ts
const json = transformToolOutput({
  data: {orderId: '123', total: {currency: 'EUR', centAmount: 4200}},
  title: 'Order summary',
  format: 'json',
});

// Expected `json` (parsed shape):
// {"ORDER SUMMARY":{"orderId":"123","total":{"currency":"EUR","centAmount":4200}}}
// Exact string spacing follows JSON.stringify.
```

---

## Examples: `transformPropertyName`

Splits **camelCase**, **PascalCase**, **snake_case**, and **kebab-case** into words and applies light title-style casing (see unit tests for acronym edge cases).

```ts
import {transformPropertyName} from '@commercetools/processors';

transformPropertyName('customerId');
// Expected: "Customer Id"

transformPropertyName('order_line_id');
// Expected: "Order Line Id"

transformPropertyName('propertyNameSDK');
// Expected: "Property Name SDK"
```

---

## Examples: URL helpers

```ts
import {
  isValidUrl,
  normaliseUrl,
  generateQueryString,
} from '@commercetools/processors';

isValidUrl('https://example.com/path?q=1');
// Expected: true

isValidUrl('not a url');
// Expected: false

normaliseUrl('https://a.com//b/../c?x=1');
// Example output (string; normalises slashes/host segment style — see tests for full matrix):
// "https://a.com/b/../c?x=1"

generateQueryString({a: 1, b: [2, 3]});
// Expected (qs indices format; leading `?`):
// "?a=1&b[0]=2&b[1]=3"
```

More cases: **`processors/test/field-filtering/urlHelpers.test.ts`**.

---

## Defaults export

```ts
import {
  defaultFilteringRules,
  defaultJsonRedactionText,
  defaultUrlRedactionText,
} from '@commercetools/processors';

// `defaultFilteringRules` is a FieldFilteringManagerConfig-shaped object with only the default redaction strings set.
// `defaultJsonRedactionText` === '[REDACTED]'
// `defaultUrlRedactionText` === 'REDACTED'
```

---

## Build from source (monorepo)

```bash
pnpm --filter @commercetools/processors install
pnpm --filter @commercetools/processors run build
pnpm --filter @commercetools/processors run test
```

---

## Further reading

Behavioural details (whitelist vs paths, URL bracket keys, empty-rule short-circuit, etc.) are covered [here](test/field-filtering/FieldFilteringHandler.test.ts) and [here](test/transform/transformToolOutput.test.ts)
