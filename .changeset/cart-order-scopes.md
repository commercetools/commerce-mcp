---
"@commercetools/commerce-agent": patch
---

Grant the cart tools to tokens with the order scopes (`view_orders`, `manage_orders`, `manage_my_orders`). commercetools has no cart scope, so a scoped (non-admin) token previously lost every cart tool, including `replicate_carts`.
