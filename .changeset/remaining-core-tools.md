---
"@commercetools/commerce-agent": minor
---

Expose the remaining `@commercetools/tools-core` tools:

- attribute groups: `read_attribute_groups`, `create_attribute_groups`, `update_attribute_groups` (scope key `attribute-group`)
- `read_messages` (scope key `message`), `read_product_projections` (scope key `product-projection`) and `read_customer_search` (scope key `customer-search`)
- Checkout applications and payment integrations: `read/create/update_applications` (scope key `application`) and `read/create/update_payment_integrations` (scope key `payment-integration`)
- `replicate_carts` and `apply_order_edits`, gated by their own `replicate` / `apply` actions rather than `create` / `update`
