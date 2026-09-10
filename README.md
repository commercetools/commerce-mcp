# commercetools Commerce MCP

This repository contains both an MCP server (which you can integrate with many MCP clients) and commerce agent that can be used from within agent frameworks.

# commercetools Model Context Protocol

## Setup

To run the commercetools MCP server using npx, use the following command:

### Client Credentials Authentication (Default)

```bash
# To set up all available tools (authType is optional, defaults to client_credentials)
npx -y @commercetools/commerce-mcp --tools=all --clientId=CLIENT_ID --clientSecret=CLIENT_SECRET --projectKey=PROJECT_KEY --authUrl=AUTH_URL --apiUrl=API_URL

# Explicitly specify client_credentials (optional)
npx -y @commercetools/commerce-mcp --tools=all --authType=client_credentials --clientId=CLIENT_ID --clientSecret=CLIENT_SECRET --projectKey=PROJECT_KEY --authUrl=AUTH_URL --apiUrl=API_URL

# To set up all read-only tools
npx -y @commercetools/commerce-mcp --tools=read_all --clientId=CLIENT_ID --clientSecret=CLIENT_SECRET --projectKey=PROJECT_KEY --authUrl=AUTH_URL --apiUrl=API_URL

```

```bash
# To set up specific tools
npx -y @commercetools/commerce-mcp --tools=read_products,create_products --clientId=CLIENT_ID --clientSecret=CLIENT_SECRET --projectKey=PROJECT_KEY --authUrl=AUTH_URL --apiUrl=API_URL
```

### Access Token Authentication

```bash
# To set up all available tools with access token
npx -y @commercetools/commerce-mcp --tools=all --authType=auth_token --accessToken=ACCESS_TOKEN --projectKey=PROJECT_KEY --authUrl=AUTH_URL --apiUrl=API_URL

# To set up all read-only tools with access token
npx -y @commercetools/commerce-mcp --tools=read_all --authType=auth_token --accessToken=ACCESS_TOKEN --projectKey=PROJECT_KEY --authUrl=AUTH_URL --apiUrl=API_URL
```

Make sure to replace `CLIENT_ID`, `CLIENT_SECRET`, `PROJECT_KEY`, `AUTH_URL`, `API_URL`, and `ACCESS_TOKEN` with your actual values. If using the customerId parameter, replace `CUSTOMER_ID` with the actual customer ID. Alternatively, you could set the API_KEY in your environment variables.

### Authentication Options

The MCP server supports two authentication methods:

| Authentication Type            | Required Arguments                                         | Description                                                                                                                          |
| ------------------------------ | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `client_credentials` (default) | `--clientId`, `--clientSecret`                             | Uses API client credentials for authentication. `--authType=client_credentials` is optional since this is the default                |
| `auth_token`                   | `--accessToken`, (optional `--clientId`, `--clientSecret`) | Uses a pre-existing access token for authentication. Requires `--authType=auth_token` and optional `--clientId` and `--clientSecret` |

With `--authType=auth_token`, `--accessToken` (or `ACCESS_TOKEN`) is only required for the stdio transport, which has no way to receive a token later. A remote server (`--remote=true`) does not necessarily need it at startup: every request must carry its own `Authorization: Bearer <token>` header, and that token is used for the request. Passing `--accessToken` alongside `--remote=true` is still allowed, but per-request tokens always take precedence.

### Customer context

Pass `--customerId=CUSTOMER_ID` to run the server in customer self-service mode. When set, tools for customer-owned resources are automatically scoped to that customer and limited to safe operations:

- **customers** — only the customer's own profile can be read.
- **orders**, **carts**, **recurring-orders** — queries are restricted to the customer's records; look-ups by id/key are ownership-checked.
- **quotes**, **quote-requests**, **shopping-lists** — restricted to the customer's own records; carts and shopping lists created this way are owned by the customer, and updates verify ownership. Quote updates are limited to customer-permitted actions (accept/decline, request renegotiation).

Resources that are not customer-owned (for example `products` or `categories`) are unaffected. Combine `--customerId` with `--businessUnitKey` to operate as a B2B associate within a Business Unit instead.

### Usage with Claude Desktop

Add the following to your `claude_desktop_config.json`. See [here](https://modelcontextprotocol.io/quickstart/user) for more details.

#### Client Credentials Authentication

```json
{
  "mcpServers": {
    "commercetools": {
      "command": "npx",
      "args": [
        "-y",
        "@commercetools/commerce-mcp@latest",
        "--tools=all",
        "--clientId=CLIENT_ID",
        "--clientSecret=CLIENT_SECRET",
        "--authUrl=AUTH_URL",
        "--projectKey=PROJECT_KEY",
        "--apiUrl=API_URL",
        "--dynamicToolLoadingThreshold=30"
      ]
    }
  }
}
```

**Note**: You can optionally add `"--authType=client_credentials"` to be explicit, but it's not required since this is the default.

#### Access Token Authentication

```json
{
  "mcpServers": {
    "commercetools": {
      "command": "npx",
      "args": [
        "-y",
        "@commercetools/commerce-mcp@latest",
        "--tools=all",
        "--authType=auth_token",
        "--accessToken=ACCESS_TOKEN",
        "--authUrl=AUTH_URL",
        "--projectKey=PROJECT_KEY",
        "--apiUrl=API_URL"
      ]
    }
  }
}
```

**Alternative: To use only read-only tools, replace `"--tools=all"` with `"--tools=read_all"`**

## Available tools

### Special Tool Options

| Tool       | Description                                                      |
| ---------- | ---------------------------------------------------------------- |
| `all`      | Enable all available tools (read, create, and update operations) |
| `read_all` | Enable all read-only tools (safe for read-only access)           |

### Individual Tools

| Tool                       | Description                                                                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `read_approval_flows`       | [Read Approval Flow](https://docs.commercetools.com/api/projects/approval-flows#query-approvalflows)                               |
| `update_approval_flows`     | [Update Approval Flow](https://docs.commercetools.com/api/projects/approval-flows#update-approvalflow-by-id)                       |
| `read_approval_rules`       | [Read Approval Rule](https://docs.commercetools.com/api/projects/approval-rules#query-approvalrules)                               |
| `create_approval_rules`     | [Create Approval Rule](https://docs.commercetools.com/api/projects/approval-rules#create-approvalrule)                             |
| `update_approval_rules`     | [Update Approval Rule](https://docs.commercetools.com/api/projects/approval-rules#update-approvalrule-by-id)                       |
| `read_associate_roles`      | [Read Associate Role](https://docs.commercetools.com/api/projects/associate-roles#query-associate-roles)                           |
| `create_associate_roles`    | [Create Associate Role](https://docs.commercetools.com/api/projects/associate-roles#create-associate-role)                         |
| `update_associate_roles`    | [Update Associate Role](https://docs.commercetools.com/api/projects/associate-roles#update-associate-role-by-id)                   |
| `read_order_edits`          | [Read Order Edit](https://docs.commercetools.com/api/projects/order-edits#query-orderedits)                                        |
| `create_order_edits`        | [Create Order Edit](https://docs.commercetools.com/api/projects/order-edits#create-orderedit)                                      |
| `update_order_edits`        | [Update or Apply Order Edit](https://docs.commercetools.com/api/projects/order-edits#update-orderedit-by-id)                       |
| `read_product_selection_assignments` | [Read Products in Product Selection](https://docs.commercetools.com/api/projects/product-selections#query-productselection-products) |
| `read_recurrence_policies`   | [Read Recurrence Policy](https://docs.commercetools.com/api/projects/recurrence-policies#query-recurrencepolicies)                 |
| `create_recurrence_policies` | [Create Recurrence Policy](https://docs.commercetools.com/api/projects/recurrence-policies#create-recurrencepolicy)                |
| `update_recurrence_policies` | [Update Recurrence Policy](https://docs.commercetools.com/api/projects/recurrence-policies#update-recurrencepolicy-by-id)          |
| `read_states`              | [Read State](https://docs.commercetools.com/api/projects/states#query-states)                                                      |
| `create_states`            | [Create State](https://docs.commercetools.com/api/projects/states#create-state)                                                    |
| `update_states`            | [Update State](https://docs.commercetools.com/api/projects/states#update-state-by-id)                                              |
| `read_products`            | [Read product information](https://docs.commercetools.com/api/projects/products#query-products)                                    |
| `create_products`          | [Create product information](https://docs.commercetools.com/api/projects/products#create-product)                                  |
| `update_products`          | [Update product information](https://docs.commercetools.com/api/projects/products#update-product)                                  |
| `read_project`             | [Read project information](https://docs.commercetools.com/api/projects/project#get-project)                                        |
| `read_product_search`      | [Search products](https://docs.commercetools.com/api/projects/products#search-products)                                            |
| `read_categories`            | [Read category information](https://docs.commercetools.com/api/projects/categories#get-category-by-id)                             |
| `create_categories`          | [Create category](https://docs.commercetools.com/api/projects/categories#create-category)                                          |
| `update_categories`          | [Update category](https://docs.commercetools.com/api/projects/categories#update-category)                                          |
| `read_channels`             | [Read channel information](https://docs.commercetools.com/api/projects/channels#query-channels)                                    |
| `create_channels`           | [Create channel](https://docs.commercetools.com/api/projects/channels#create-channel)                                              |
| `update_channels`           | [Update channel information](https://docs.commercetools.com/api/projects/channels#update-channel)                                  |
| `read_product_selections`   | [Read product selection](https://docs.commercetools.com/api/projects/product-selections#get-productselection-by-id)                |
| `create_product_selections` | [Create product selection](https://docs.commercetools.com/api/projects/product-selections#create-a-productselection)               |
| `update_product_selections` | [Update product selection](https://docs.commercetools.com/api/projects/product-selections#update-productselection)                 |
| `read_orders`               | [Read order information](https://docs.commercetools.com/api/projects/orders#get-order-by-id)                                       |
| `create_orders`             | [Create order](https://docs.commercetools.com/api/projects/orders#create-order-from-cart) (from cart, quote, import)               |
| `update_orders`             | [Update order information](https://docs.commercetools.com/api/projects/orders#update-order)                                        |
| `read_carts`                | [Read cart information](https://docs.commercetools.com/api/projects/carts#get-cart-by-id)                                          |
| `create_carts`              | [Create cart](https://docs.commercetools.com/api/projects/carts#create-cart)                                                       |
| `update_carts`              | [Update cart information](https://docs.commercetools.com/api/projects/carts#update-cart)                                           |
| `read_customers`            | [Read customer information](https://docs.commercetools.com/api/projects/customers#query-customers)                                 |
| `create_customers`          | [Create customer](https://docs.commercetools.com/api/projects/customers#create-customer)                                           |
| `update_customers`          | [Update customer information](https://docs.commercetools.com/api/projects/customers#update-customer)                               |
| `read_customer_groups`      | [Read customer group](https://docs.commercetools.com/api/projects/customerGroups#get-customergroup)                                |
| `create_customer_groups`    | [Create customer group](https://docs.commercetools.com/api/projects/customerGroups#create-customergroup)                           |
| `update_customer_groups`    | [Update customer group](https://docs.commercetools.com/api/projects/customerGroups#update-customergroup)                           |
| `read_quotes`               | [Read quote information](https://docs.commercetools.com/api/projects/quotes#get-quote-by-id)                                       |
| `create_quotes`             | [Create quote](https://docs.commercetools.com/api/projects/quotes#create-quote-from-staged-quote)                                  |
| `update_quotes`             | [Update quote information](https://docs.commercetools.com/api/projects/quotes#update-quote)                                        |
| `read_quote_requests`       | [Read quote request](https://docs.commercetools.com/api/projects/quote-requests#get-quoterequest-by-id)                            |
| `create_quote_requests`     | [Create quote request](https://docs.commercetools.com/api/projects/quote-requests#create-quoterequest)                             |
| `update_quote_requests`     | [Update quote request](https://docs.commercetools.com/api/projects/quote-requests#update-quoterequest)                             |
| `read_staged_quotes`        | [Read staged quote](https://docs.commercetools.com/api/projects/staged-quotes#get-stagedquote-by-id)                               |
| `create_staged_quotes`      | [Create staged quote](https://docs.commercetools.com/api/projects/staged-quotes#create-stagedquote)                                |
| `update_staged_quotes`      | [Update staged quote](https://docs.commercetools.com/api/projects/staged-quotes#update-stagedquote)                                |
| `read_standalone_prices`    | [Read standalone price](https://docs.commercetools.com/api/projects/standalone-prices#get-standaloneprice-by-id)                   |
| `create_standalone_prices`  | [Create standalone price](https://docs.commercetools.com/api/projects/standalone-prices#create-standaloneprice)                    |
| `update_standalone_prices`  | [Update standalone price](https://docs.commercetools.com/api/projects/standalone-prices#update-standaloneprice)                    |
| `read_product_discounts`    | [Read product discount](https://docs.commercetools.com/api/projects/productDiscounts#get-productdiscount-by-id)                    |
| `create_product_discounts`  | [Create product discount](https://docs.commercetools.com/api/projects/productDiscounts#create-productdiscount)                     |
| `update_product_discounts`  | [Update product discount](https://docs.commercetools.com/api/projects/productDiscounts#update-productdiscount)                     |
| `read_cart_discounts`       | [Read cart discount](https://docs.commercetools.com/api/projects/cartDiscounts#get-cartdiscount-by-id)                             |
| `create_cart_discounts`     | [Create cart discount](https://docs.commercetools.com/api/projects/cartDiscounts#create-cartdiscount)                              |
| `update_cart_discounts`     | [Update cart discount](https://docs.commercetools.com/api/projects/cartDiscounts#update-cartdiscount)                              |
| `read_discount_codes`       | [Read discount code information](https://docs.commercetools.com/api/projects/discount-codes#get-discountcode-by-id)                |
| `create_discount_codes`     | [Create discount code](https://docs.commercetools.com/api/projects/discount-codes#create-discountcode)                             |
| `update_discount_codes`     | [Update discount code information](https://docs.commercetools.com/api/projects/discount-codes#update-discountcode)                 |
| `read_product_types`        | [Read product type](https://docs.commercetools.com/api/projects/productTypes#get-producttype-by-id)                                |
| `create_product_types`      | [Create product type](https://docs.commercetools.com/api/projects/productTypes#create-producttype)                                 |
| `update_product_types`      | [Update product type](https://docs.commercetools.com/api/projects/productTypes#update-producttype)                                 |
| `create_bulk`              | Create entities in bulk                                                                                                            |
| `update_bulk`              | Update entities in bulk                                                                                                            |
| `read_inventory`           | [Read inventory information](https://docs.commercetools.com/api/projects/inventory#get-inventoryentry-by-id)                       |
| `create_inventory`         | [Create inventory](https://docs.commercetools.com/api/projects/inventory#create-inventoryentry)                                    |
| `update_inventory`         | [Update inventory information](https://docs.commercetools.com/api/projects/inventory#update-inventoryentry)                        |
| `read_stores`               | [Read store](https://docs.commercetools.com/api/projects/stores#get-store-by-id)                                                   |
| `create_stores`             | [Create store](https://docs.commercetools.com/api/projects/stores#create-store)                                                    |
| `update_stores`             | [Update store](https://docs.commercetools.com/api/projects/stores#update-store)                                                    |
| `read_business_units`       | [Read business unit](https://docs.commercetools.com/api/projects/business-units#get-businessunit-by-id)                            |
| `create_business_units`     | [Create business unit](https://docs.commercetools.com/api/projects/business-units#create-businessunit)                             |
| `update_business_units`     | [Update business unit](https://docs.commercetools.com/api/projects/business-units#update-businessunit)                             |
| `read_payments`            | [Read payment information](https://docs.commercetools.com/api/projects/payments#get-payment-by-id)                                 |
| `create_payments`          | [Create payment](https://docs.commercetools.com/api/projects/payments#create-payment)                                              |
| `update_payments`          | [Update payment information](https://docs.commercetools.com/api/projects/payments#update-actions)                                  |
| `read_tax_categories`        | [Read tax category information](https://docs.commercetools.com/api/projects/taxCategories#get-taxcategory-by-id)                   |
| `create_tax_categories`      | [Create tax category](https://docs.commercetools.com/api/projects/taxCategories#create-taxcategory)                                |
| `update_tax_categories`      | [Update tax category information](https://docs.commercetools.com/api/projects/taxCategories#update-taxcategory)                    |
| `read_shipping_methods`    | [Read shipping method information](https://docs.commercetools.com/api/projects/shippingMethods#get-shippingmethod-by-id)           |
| `create_shipping_methods`  | [Create shipping method](https://docs.commercetools.com/api/projects/shippingMethods#create-shippingmethod)                        |
| `update_shipping_methods`  | [Update shipping method information](https://docs.commercetools.com/api/projects/shippingMethods#update-shippingmethod)            |
| `read_zones`                | [Read zone information](https://docs.commercetools.com/api/projects/zones#get-zone-by-id)                                          |
| `create_zones`              | [Create zone](https://docs.commercetools.com/api/projects/zones#create-zone)                                                       |
| `update_zones`              | [Update zone information](https://docs.commercetools.com/api/projects/zones#update-zone)                                           |
| `read_recurring_orders`    | [Read recurring order information](https://docs.commercetools.com/api/projects/recurring-orders#get-recurringorder-by-id)          |
| `create_recurring_orders`  | [Create recurring order](https://docs.commercetools.com/api/projects/recurring-orders#create-recurringorder)                       |
| `update_recurring_orders`  | [Update recurring order information](https://docs.commercetools.com/api/projects/recurring-orders#update-recurringorder)           |
| `read_shopping_lists`      | [Read shopping list information](https://docs.commercetools.com/api/projects/shoppingLists#get-shoppinglist-by-id)                 |
| `create_shopping_lists`    | [Create shopping list](https://docs.commercetools.com/api/projects/shoppingLists#create-shoppinglist)                              |
| `update_shopping_lists`    | [Update shopping list information](https://docs.commercetools.com/api/projects/shoppingLists#update-shoppinglist)                  |
| `read_extensions`          | [Read extension information](https://docs.commercetools.com/api/projects/extensions#get-extension-by-id)                           |
| `create_extensions`        | [Create extension](https://docs.commercetools.com/api/projects/extensions#create-an-extension)                                     |
| `update_extensions`        | [Update extension information](https://docs.commercetools.com/api/projects/extensions#update-an-extension)                         |
| `read_subscriptions`       | [Read subscription information](https://docs.commercetools.com/api/projects/subscriptions#get-subscription-by-id)                  |
| `create_subscriptions`     | [Create subscription](https://docs.commercetools.com/api/projects/subscriptions#create-a-subscription)                             |
| `update_subscriptions`     | [Update subscription information](https://docs.commercetools.com/api/projects/subscriptions#update-subscription)                   |
| `read_payment_methods`     | [Read payment method information](https://docs.commercetools.com/api/projects/paymentMethods#get-paymentmethod-by-id)              |
| `create_payment_methods`   | [Create payment method](https://docs.commercetools.com/api/projects/paymentMethods#create-paymentmethod)                           |
| `update_payment_methods`   | [Update payment method information](https://docs.commercetools.com/api/projects/paymentMethods#update-paymentmethod)               |
| `read_product_tailoring`   | [Read product tailoring information](https://docs.commercetools.com/api/projects/productTailoring#get-producttailoring-by-id)      |
| `create_product_tailoring` | [Create product tailoring](https://docs.commercetools.com/api/projects/productTailoring#create-producttailoring)                   |
| `update_product_tailoring` | [Update product tailoring information](https://docs.commercetools.com/api/projects/productTailoring#update-producttailoring)       |
| `read_custom_objects`      | [Read custom object information](https://docs.commercetools.com/api/projects/custom-objects#get-customobject-by-container-and-key) |
| `create_custom_objects`    | [Create custom object](https://docs.commercetools.com/api/projects/custom-objects#create-or-update-customobject)                   |
| `update_custom_objects`    | [Update custom object information](https://docs.commercetools.com/api/projects/custom-objects#create-or-update-customobject)       |
| `read_types`               | [Read type information](https://docs.commercetools.com/api/projects/types#get-type-by-id)                                          |
| `create_types`             | [Create type](https://docs.commercetools.com/api/projects/types#create-type)                                                       |
| `update_types`             | [Update type information](https://docs.commercetools.com/api/projects/types#update-type)                                           |

To view information on how to develop the MCP server, see [this README](/modelcontextprotocol/README.md).

## Dynamic Tool Loading

The MCP server includes a dynamic tool loading feature that automatically switches to a more efficient loading strategy when the number of enabled tools exceeds a configurable threshold. This helps optimize performance and reduce context usage when working with large numbers of tools.

### How it works

- **Default threshold**: 30 tools
- **Behavior**: When the number of enabled tools exceeds the threshold, the server switches to dynamic tool loading

### Configuration

You can configure the dynamic tool loading threshold in two ways:

#### Command Line Argument

```bash
npx -y @commercetools/commerce-mcp --tools=all --dynamicToolLoadingThreshold=50 --clientId=CLIENT_ID --clientSecret=CLIENT_SECRET --projectKey=PROJECT_KEY --authUrl=AUTH_URL --apiUrl=API_URL
```

#### Environment Variable

```bash
export DYNAMIC_TOOL_LOADING_THRESHOLD=50
npx -y @commercetools/commerce-mcp --tools=all --clientId=CLIENT_ID --clientSecret=CLIENT_SECRET --projectKey=PROJECT_KEY --authUrl=AUTH_URL --apiUrl=API_URL
```

### Example with Claude Desktop

```json
{
  "mcpServers": {
    "commercetools": {
      "command": "npx",
      "args": [
        "-y",
        "@commercetools/commerce-mcp@latest",
        "--tools=all",
        "--clientId=CLIENT_ID",
        "--clientSecret=CLIENT_SECRET",
        "--authUrl=AUTH_URL",
        "--projectKey=PROJECT_KEY",
        "--apiUrl=API_URL",
        "--dynamicToolLoadingThreshold=25"
      ]
    }
  }
}
```

# Commerce MCP

The commercetools Commerce MCP enables popular agent frameworks including LangChain, Vercel's AI SDK, and Model Context Protocol (MCP) to integrate with APIs through function calling. The library is not exhaustive of the entire commercetools API. It includes support for TypeScript and is built directly on top of the [Node][node-sdk] SDK.

Included below are basic instructions, but refer to the [TypeScript](/typescript) package for more information.

## TypeScript

### Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package run:

```
npm install @commercetools/commerce-agent
```

#### Requirements

- Node 18+

### Usage

The library needs to be configured with your commercetools project credentials which are available in your [Merchant center](https://docs.commercetools.com/getting-started/create-api-client).
**Important**: Ensure that the API client credentials have the necessary scopes aligned with the actions you configure in the commerce agent. For example, if you configure `products: { read: true }`, your API client must have the `view_products` scope.
Additionally, `configuration` enables you to specify the types of actions that can be taken using the commerce agent.

### Client Credentials Authentication (Default)

```typescript
import { CommercetoolsCommerceAgent } from "@commercetools/commerce-agent/langchain";

const commercetoolsCommerceAgent = await CommercetoolsCommerceAgent.create({
  authConfig: {
    type: 'client_credentials',
    clientId: process.env.CLIENT_ID!,
    clientSecret: process.env.CLIENT_SECRET!,
    projectKey: process.env.PROJECT_KEY!,
    authUrl: process.env.AUTH_URL!,
    apiUrl: process.env.API_URL!,
  },
  configuration: {
    actions: {
      products: {
        read: true,
        create: true,
        update: true,
      },
      project: {
        read: true,
      },
    },
  },
});
```

### Access Token Authentication

```typescript
import { CommercetoolsCommerceAgent } from "@commercetools/commerce-agent/langchain";

const commercetoolsCommerceAgent = await CommercetoolsCommerceAgent.create({
  authConfig: {
    type: "auth_token",
    accessToken: process.env.ACCESS_TOKEN!,
    projectKey: process.env.PROJECT_KEY!,
    authUrl: process.env.AUTH_URL!,
    apiUrl: process.env.API_URL!,
  },
  configuration: {
    actions: {
      products: {
        read: true,
        create: true,
        update: true,
      },
      project: {
        read: true,
      },
    },
  },
});
```

#### Tools

The commerce agent works with LangChain and Vercel's AI SDK and can be passed as a list of tools. For example:

```typescript
import { AgentExecutor, createStructuredChatAgent } from "langchain/agents";

const tools = commercetoolsCommerceAgent.getTools();

const agent = await createStructuredChatAgent({
  llm,
  tools,
  prompt,
});

const agentExecutor = new AgentExecutor({
  agent,
  tools,
});
```

## Model Context Protocol

The commercetools Commerce MCP also supports setting up your own MCP server. For example:

```typescript
import { CommercetoolsCommerceAgent } from "@commercetools/commerce-agent/modelcontextprotocol";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = await CommercetoolsCommerceAgent.create({
  authConfig: {
    type: 'client_credentials',
    clientId: process.env.CLIENT_ID!,
    clientSecret: process.env.CLIENT_SECRET!,
    projectKey: process.env.PROJECT_KEY!,
    authUrl: process.env.AUTH_URL!,
    apiUrl: process.env.API_URL!,
  },
  configuration: {
    actions: {
      products: {
        read: true,
      },
      cart: {
        read: true,
        create: true,
        update: true,
      },
    },
  },
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("My custom commercetools MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});
```

#### getTools()

Returns the current set of available tools that can be used with LangChain, AI SDK, or other agent frameworks:

```typescript
const tools = commercetoolsCommerceAgent.getTools();
```

#### Custom Tools

The self managed `@commercetools/commerce-agent` includes supports for custom tools. A list of custom tools implementations can be passed over and registered at runtime by the bootstrapping MCP server. This is especially useful when the intended tool is not yet implemented into the Commerce MCP or to give users complete control and customization of their tools behaviour and how it interact with the underlying LLM.

usage

```typescript
import { CommercetoolsCommerceAgent } from "@commercetools/commerce-agent/modelcontextprotocol";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = await CommercetoolsCommerceAgent.create({
  authConfig: {...},
  configuration: {
    customTools: [
      {
        name: "Get Project",
        method: "get_project",
        description: `This tool will fetch information about a commercetools project.\n\n
           This tool will accept a project and fetch information about the provided key. \n\n
          `, // It is important that this description is well details and explicitly descripts what this tool does and the paramenters it receieves/
        parameters: z.object({
          projectKey: z
            .string()
            .optional()
            .describe(
              "The key of the project to read. If not provided, the current project will be used."
            ),
        }),
        actions: {},
        execute: async (args: { projectKey: string }, api: ApiRoot) => {
          // already existing functions can be used here e.g const response = await import('ctService').getProject('demo-project-key-a7fc1182');
          const response = await api.withProjectKey(args).get().execute();
          return JSON.stringify(response);
        },
      },
      ...
    ],
    actions: {...},
  },
});
...
```

### Streamable HTTP MCP server

As of version `v2.0.0` of the `@commercetools/commerce-mcp` MCP server now supports Streamable HTTP (remote) server.

```typescript
npx -y @commercetools/commerce-mcp \
  --tools=all \
  --authType=client_credentials \
  --clientId=CLIENT_ID \
  --clientSecret=CLIENT_SECRET \
  --projectKey=PROJECT_KEY \
  --authUrl=AUTH_URL \
  --apiUrl=API_URL \
  --remote=true \
  --stateless=true \
  --host=127.0.0.1 \
  --port=8888
```

`--host` controls the network interface the remote server binds to. It defaults to
`127.0.0.1`, so a freshly started server is reachable from the local machine only.
Pass `--host=0.0.0.0` (or a specific interface address) to accept connections from
elsewhere — that is what container and Kubernetes deployments need in order for port
mapping to work — and the server prints a warning at startup reminding you the port is
now network-reachable, with a louder one for `0.0.0.0`/`::` since a wildcard bind also
covers interfaces you may not have had in mind. `HOST` works as an environment variable
equivalent.

`--host` takes an interface address. `--host=*` is accepted as a shorthand and binds
`0.0.0.0`; `--host=` (empty) falls back to the loopback default rather than opening the
server up. Note that `*` means something different in `--allowedHosts` below, where it
disables the check rather than selecting an interface.

Prefer `127.0.0.1` over `localhost`: on many systems `localhost` resolves to the IPv6
loopback (`::1`) first, so the server would bind IPv6 only and IPv4 clients could not
connect. A host that cannot be resolved or an address already in use is reported as
`Unable to bind <host>:<port>` and the process exits non-zero.

#### Host and Origin allow-lists

The remote server only answers for hostnames it recognises. By default that is
`localhost`, `127.0.0.1` and `[::1]`, plus whatever `--host` was set to (unless it is a
wildcard). A request whose `Host` header says anything else is rejected with
`403 Forbidden`.

This is what stops a **DNS rebinding** attack. A malicious page can flip its own
hostname to resolve to `127.0.0.1`, at which point the browser keeps treating it as the
same origin and lets the page's JavaScript talk to a local MCP server. Same-origin
policy and the absence of CORS headers do not help, because after the rebind the
request no longer looks cross-origin — but the `Host` header still carries the
attacker's hostname, so checking it turns the request away.

Serving the MCP server under a real hostname therefore needs that hostname declared:

```bash
npx -y @commercetools/commerce-mcp ... \
  --remote=true \
  --host=0.0.0.0 \
  --allowedHosts=mcp.example.com,mcp.internal
```

`--allowedOrigins` does the same for browser callers: a request carrying an `Origin`
header must match the list, which is empty by default. Requests without an `Origin` —
every non-browser MCP client — are unaffected, and no permissive
`Access-Control-Allow-Origin` header is ever sent.

Both accept comma-separated values, both have environment variable equivalents
(`ALLOWED_HOSTS`, `ALLOWED_ORIGINS`), and both accept `*` to disable the check. Use `*`
only when something in front of the server already validates the `Host` header —
it re-opens the rebinding hole described above.

You can connect to the running remote server using Claude by specifying the below in the `claude_desktop_config.json` file.

```json
{
  "mcpServers": {
    "commercetools": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8888/mcp",
        "--header",
        "Authorization: Bearer ${CTP_ACCESS_TOKEN}"
      ]
    }
  }
}
```

> **🔒 Authentication is required for the remote server.** Every HTTP request to
> `/mcp` **must** include a valid `Authorization: Bearer <commercetools-access-token>`
> header. The token is forwarded directly to the commercetools API, so it must be a
> valid commercetools OAuth access token with the scopes you want the caller to have.
> Requests with a missing or malformed header are rejected with `401 Unauthorized`.
>
> The credentials provided to the server at startup (`--clientId`/`--clientSecret` or
> `--accessToken`) are **not** used to serve network requests — they only satisfy the
> CLI's startup validation. This prevents an unauthenticated network caller from
> inheriting the server's configured credentials.
>
> Advanced embedders who perform their own authentication can opt out of this check by
> passing `enforceAuthHeader: false` to `CommercetoolsCommerceAgentStreamable` (see the
> SDK usage below). This is **not** recommended for network-exposed deployments.
>
> The startup credentials are frozen at construction and every request derives its own
> copy, so one request can never influence the credentials used by the next. In stateful
> mode (`--stateless=false`) a session additionally remembers the token it was opened
> with — knowing a session ID is not enough to continue someone else's session, and a
> mismatch is rejected with `403 Forbidden`. Callers that rotate their token mid-session
> should open a new session.

You can also use the Streamable HTTP server with the Commerce Agent like an SDK and develop on it.

```typescript
import express from "express";
import {
  CommercetoolsCommerceAgent,
  CommercetoolsCommerceAgentStreamable,
} from "@commercetools/commerce-agent/modelcontextprotocol";

const expressApp = express();

const getAgentServer = async () => {
  return CommercetoolsCommerceAgent.create({
    authConfig: {
      type: "client_credentials",
      clientId: process.env.CLIENT_ID!,
      clientSecret: process.env.CLIENT_SECRET!,
      projectKey: process.env.PROJECT_KEY!,
      authUrl: process.env.AUTH_URL!,
      apiUrl: process.env.API_URL!,
    },
    configuration: {
      actions: {
        products: {
          read: true,
        },
        cart: {
          read: true,
          create: true,
          update: true,
        },
      },
    },
  });
};

const serverStreamable = new CommercetoolsCommerceAgentStreamable({
  stateless: false, // make the MCP server stateless/stateful
  server: getAgentServer,
  app: expressApp, // optional express app instance
  // By default every request must send an `Authorization: Bearer <token>`
  // header (otherwise it is rejected with 401). If your `getAgentServer`
  // factory already handles authentication, set this to false to opt out.
  // enforceAuthHeader: false,
  streamableHttpOptions: {
    sessionIdGenerator: undefined,
  },
});

serverStreamable.listen(8888, function () {
  console.log("listening on 8888");
});
```

Without using the `CommercetoolsCommerceAgent`, you can directly use only the `CommercetoolsCommerceAgentStreamable` class and the agent server will be bootstrapped internally.

```typescript
import { CommercetoolsCommerceAgentStreamable } from "@commercetools/commerce-agent/modelcontextprotocol";
import express from "express";

const expressApp = express();

const server = new CommercetoolsCommerceAgentStreamable({
  authConfig: {
    type: "client_credentials",
    clientId: process.env.CLIENT_ID!,
    clientSecret: process.env.CLIENT_SECRET!,
    projectKey: process.env.PROJECT_KEY!,
    authUrl: process.env.AUTH_URL!,
    apiUrl: process.env.API_URL!,
  },
  configuration: {
    actions: {
      project: {
        read: true,
      },
      // other tools can go here
    },
  },

  stateless: false,
  app: expressApp,
  streamableHttpOptions: {
    sessionIdGenerator: undefined,
  },
});

server.listen(8888, function () {
  console.log("listening on 8888");
});
```
