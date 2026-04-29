---
"@commercetools/commerce-mcp": major
"@commercetools/commerce-agent": major
---

major package updates and bug fixes

### What Changed
- Tool output now is defaulted to `json`
_this means if `--toolOutputFormat` option is not specified then it defaults to `json`_

- Tool output text in `json` format has been dropped
_the root explanatory text for tool output json object has been removed_

```ts
// before
{
  "READ CART DISCOUNT RESULT": {
    limit: 10,
    offset: 0,
    count: 10,
    results: [
      {
        id: '123',
        name: 'Cart Discount 1',
        description: 'This is a cart discount',
        code: '1234567890',
      }
    ],
  },
}

// after
{
  limit: 10,
  offset: 0,
  count: 10,
  results: [
    {
      id: '123',
      name: 'Cart Discount 1',
      description: 'This is a cart discount',
      code: '1234567890',
    }
  ],
}
```
The `READ CART DISCOUNT RESULT` text has been dropped

- The `all` tool now requires setting `isAdmin` option to `true`

```bash
npx -y @commercetools/commerce-mcp --tools="all" --isAdmin=true ...
```

