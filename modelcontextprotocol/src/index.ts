#!/usr/bin/env node

import {
  Configuration,
  AvailableNamespaces,
  CommercetoolsCommerceAgent,
  CommercetoolsCommerceAgentStreamable,
  AuthConfig,
} from '@commercetools/commerce-agent/modelcontextprotocol';
import {
  FieldFilteringManagerConfig,
  FieldFilteringRule,
  FieldFilteringHandler,
} from '@commercetools/commerce-agent/modelcontextprotocol';
import {StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js';
import {red, yellow} from 'colors';

type Options = {
  tools?: string[];
  customerId?: string;
  cartId?: string;
  isAdmin?: boolean;
  storeKey?: string;
  businessUnitKey?: string;
  dynamicToolLoadingThreshold?: number;
  logging?: boolean;
  toolOutputFormat?: 'json' | 'tabular';
  fieldFiltering?: FieldFilteringManagerConfig;
};

type EnvVars = {
  clientId?: string;
  clientSecret?: string;
  authUrl?: string;
  projectKey?: string;
  apiUrl?: string;
  remote?: boolean;
  stateless?: boolean;
  port?: number;
  logging?: boolean;
  accessToken?: string;
  authType?: 'client_credentials' | 'auth_token';
};

const HIDDEN_ARGS = ['customerId', 'isAdmin', 'storeKey', 'businessUnitKey'];

const PUBLIC_ARGS = [
  'tools',
  'authType',
  'clientId',
  'clientSecret',
  'accessToken',
  'authUrl',
  'projectKey',
  'apiUrl',
  'dynamicToolLoadingThreshold',
  'toolOutputFormat',
];

const ACCEPTED_ARGS = [...PUBLIC_ARGS, ...HIDDEN_ARGS];

export const ACCEPTED_TOOLS = [
  'business-unit.read',
  'business-unit.create',
  'business-unit.update',
  'products.read',
  'products.create',
  'products.update',
  'project.read',
  'product-search.read',
  'category.read',
  'category.create',
  'category.update',
  'channel.read',
  'channel.create',
  'channel.update',
  'product-selection.read',
  'product-selection.create',
  'product-selection.update',
  'order.read',
  'order.create',
  'order.update',
  'cart.read',
  'cart.create',
  'cart.update',
  'customer.create',
  'customer.read',
  'customer.update',
  'customer-group.read',
  'customer-group.create',
  'customer-group.update',
  'quote.read',
  'quote.create',
  'quote.update',
  'quote-request.read',
  'quote-request.create',
  'quote-request.update',
  'staged-quote.read',
  'staged-quote.create',
  'staged-quote.update',
  'standalone-price.read',
  'standalone-price.create',
  'standalone-price.update',
  'product-discount.read',
  'product-discount.create',
  'product-discount.update',
  'cart-discount.read',
  'cart-discount.create',
  'cart-discount.update',
  'discount-code.read',
  'discount-code.create',
  'discount-code.update',
  'product-type.read',
  'product-type.create',
  'product-type.update',
  'bulk.create',
  'bulk.update',
  'inventory.read',
  'inventory.create',
  'inventory.update',
  'store.read',
  'store.create',
  'store.update',
  'review.read',
  'review.create',
  'review.update',

  'tax-category.read',
  'tax-category.create',
  'tax-category.update',

  'shipping-methods.read',
  'shipping-methods.create',
  'shipping-methods.update',

  'payments.read',
  'payments.create',
  'payments.update',

  'zone.read',
  'zone.create',
  'zone.update',

  'product-tailoring.read',
  'product-tailoring.create',
  'product-tailoring.update',

  'payment-methods.read',
  'payment-methods.create',
  'payment-methods.update',

  'recurring-orders.read',
  'recurring-orders.create',
  'recurring-orders.update',

  'shopping-lists.read',
  'shopping-lists.create',
  'shopping-lists.update',

  'extensions.read',
  'extensions.create',
  'extensions.update',

  'subscriptions.read',
  'subscriptions.create',
  'subscriptions.update',

  'custom-objects.read',
  'custom-objects.create',
  'custom-objects.update',

  'types.read',
  'types.create',
  'types.update',

  'payment-intents.update',

  'transactions.read',
  'transactions.create',
];

export function parseArgs(args: string[]): {options: Options; env: EnvVars} {
  const options: Options = {};
  const env: EnvVars = {};

  args.forEach((arg) => {
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');

      if (key == 'tools') {
        options.tools = value.split(',').map((tool) => tool.trim());
      } else if (key == 'authType') {
        env.authType = value as EnvVars['authType'];
      } else if (key == 'accessToken') {
        env.accessToken = value;
      } else if (key == 'clientId') {
        env.clientId = value;
      } else if (key == 'clientSecret') {
        env.clientSecret = value;
      } else if (key == 'authUrl') {
        env.authUrl = value;
      } else if (key == 'projectKey') {
        env.projectKey = value;
      } else if (key == 'apiUrl') {
        env.apiUrl = value;
      } else if (key == 'remote') {
        env.remote = value == 'true';
      } else if (key == 'stateless') {
        env.stateless = value == 'true';
      } else if (key == 'port') {
        env.port = Number(value);
      } else if (key == 'customerId') {
        options.customerId = value;
      } else if (key == 'isAdmin') {
        options.isAdmin = value === 'true';
      } else if (key == 'dynamicToolLoadingThreshold') {
        options.dynamicToolLoadingThreshold = Number(value);
      } else if (key == 'toolOutputFormat') {
        if (value === 'json' || value === 'tabular') {
          options.toolOutputFormat = value;
        }
      } else if (key == 'fieldFiltering') {
        options.fieldFiltering = tryParseFieldFiltering(value);
      } else if (key == 'logging') {
        options.logging = value == 'true';
      } else if (key == 'cartId') {
        options.cartId = value;
      } else if (key == 'storeKey') {
        options.storeKey = value;
      } else if (key == 'businessUnitKey') {
        options.businessUnitKey = value;
      } else {
        throw new Error(
          `Invalid argument: ${key}. Accepted arguments are: ${PUBLIC_ARGS.join(
            ', '
          )}`
        );
      }
    }
  });

  // Check if required tools arguments is present
  if (!options.tools) {
    if (!process.env.TOOLS) {
      throw new Error('The --tools arguments must be provided.');
    }
    options.tools = process.env.TOOLS.split(',').map((tool) => tool.trim());
  }

  // Validate tools against accepted enum values
  // Ensure tools are trimmed before validation
  options.tools = options.tools.map((tool: string) => tool.trim());
  options.tools.forEach((tool: string) => {
    if (tool == 'all' || tool == 'all.read') {
      return;
    }
    if (!ACCEPTED_TOOLS.includes(tool)) {
      throw new Error(
        `Invalid tool: ${tool}. Accepted tools are: ${ACCEPTED_TOOLS.join(
          ', '
        )}`
      );
    }
  });

  // Check for commercetools env vars
  env.authType =
    env.authType ||
    (process.env.AUTH_TYPE as EnvVars['authType']) ||
    'client_credentials';
  env.accessToken = env.accessToken || process.env.ACCESS_TOKEN;
  env.clientId = env.clientId || process.env.CLIENT_ID;
  env.clientSecret = env.clientSecret || process.env.CLIENT_SECRET;
  env.authUrl = env.authUrl || process.env.AUTH_URL;
  env.projectKey = env.projectKey || process.env.PROJECT_KEY;
  env.apiUrl = env.apiUrl || process.env.API_URL;

  env.remote = env.remote || process.env.REMOTE == 'true';
  env.logging = env.logging || process.env.LOGGING == 'true';
  env.stateless = env.stateless || process.env.STATELESS == 'true';
  env.port = env.port || Number(process.env.PORT);

  options.businessUnitKey =
    options.businessUnitKey || process.env.BUSINESS_UNIT_KEY;
  options.storeKey = options.storeKey || process.env.STORE_KEY;
  options.customerId = options.customerId || process.env.CUSTOMER_ID;
  if (options.isAdmin === undefined) {
    options.isAdmin = process.env.IS_ADMIN === 'true';
  }
  options.logging = options.logging || process.env.LOGGING == 'true';
  options.dynamicToolLoadingThreshold =
    options.dynamicToolLoadingThreshold ||
    (process.env.DYNAMIC_TOOL_LOADING_THRESHOLD
      ? Number(process.env.DYNAMIC_TOOL_LOADING_THRESHOLD)
      : undefined);

  if (
    (process.env.TOOL_OUTPUT_FORMAT &&
      process.env.TOOL_OUTPUT_FORMAT === 'tabular') ||
    process.env.TOOL_OUTPUT_FORMAT === 'json'
  ) {
    options.toolOutputFormat = process.env.TOOL_OUTPUT_FORMAT;
  }

  options.cartId = options.cartId || process.env.CART_ID;

  // Validate required commercetools credentials based on auth type
  if (!env.authUrl || !env.projectKey || !env.apiUrl) {
    throw new Error(
      'Missing required options. Please make sure to provide the values for "authUrl", "apiUrl", "projectKey" or via environment variables (AUTH_URL, API_URL, PROJECT_KEY).'
    );
  }

  // Validate auth-specific requirements
  switch (env.authType) {
    case 'client_credentials':
      if (!env.clientId || !env.clientSecret) {
        throw new Error(
          'Missing required client credentials when "authType" is "client_credentials". Please make sure to provide the values for "clientId", "clientSecret" or via environment variables (CLIENT_ID, CLIENT_SECRET).'
        );
      }
      break;
    case 'auth_token':
      if (!env.accessToken) {
        throw new Error(
          'Missing required access token when "authType" is "auth_token". Please make sure to provide the value for "accessToken" or via environment variable (ACCESS_TOKEN).'
        );
      }
      break;
    default:
      throw new Error(
        `Invalid auth type: ${env.authType}. Supported types are: client_credentials, auth_token`
      );
  }

  return {options, env};
}

function tryParseFieldFiltering(
  fieldFilteringString: string
): FieldFilteringManagerConfig | never {
  let fieldFilteringConfig: FieldFilteringManagerConfig;
  try {
    fieldFilteringConfig = JSON.parse(fieldFilteringString);
  } catch (error) {
    throw new Error(
      `Invalid argument: fieldFiltering. Error parsing JSON: ${error}`
    );
  }
  if (
    typeof fieldFilteringConfig !== 'object' ||
    fieldFilteringConfig === null ||
    Array.isArray(fieldFilteringConfig)
  ) {
    throw new Error(
      `Invalid argument: fieldFiltering. Value must be a stringified object of type FieldFilteringManagerConfig.`
    );
  }
  if (fieldFilteringConfig.paths) {
    if (!isFieldFilteringRuleArray(fieldFilteringConfig.paths)) {
      throw new Error(
        `Invalid argument: fieldFiltering.paths. Value must be a stringified array of type { type: "filter" | "redact", value: string, value: boolean }`
      );
    }
  }
  if (fieldFilteringConfig.properties) {
    if (!isFieldFilteringRuleArray(fieldFilteringConfig.properties)) {
      throw new Error(
        `Invalid argument: fieldFiltering.properties. Value must be a stringified array of type { type: "filter" | "redact", value: string, value: boolean }`
      );
    }
  }
  if (fieldFilteringConfig.whitelistPaths) {
    if (
      !isFieldFilteringRuleArray(
        // add value property to whitelistPaths depsite irrelevance to reuse isFieldFilteringRuleArray logic
        fieldFilteringConfig.whitelistPaths.map((path) => ({
          ...path,
          value: 'filter',
        }))
      )
    ) {
      throw new Error(
        `Invalid argument: fieldFiltering.whitelistPaths. Value must be a stringified array of type { value: string, value: boolean }`
      );
    }
  }
  if (fieldFilteringConfig.includes) {
    if (!isFieldFilteringRuleArray(fieldFilteringConfig.includes)) {
      throw new Error(
        `Invalid argument: fieldFiltering.includes. Value must be a stringified array of type { type: "filter" | "redact", value: string, value: boolean }`
      );
    }
  }
  if (fieldFilteringConfig.jsonRedactionText) {
    if (typeof fieldFilteringConfig.jsonRedactionText !== 'string') {
      throw new Error(
        `Invalid argument: fieldFiltering.jsonRedactionText. Value must be of type string`
      );
    }
  }
  if (fieldFilteringConfig.urlRedactionText) {
    if (typeof fieldFilteringConfig.urlRedactionText !== 'string') {
      throw new Error(
        `Invalid argument: fieldFiltering.urlRedactionText. Value must be of type string`
      );
    }
  }

  return fieldFilteringConfig;
}

function isFieldFilteringRuleArray(
  possibleRules: any
): possibleRules is FieldFilteringRule[] {
  if (!Array.isArray(possibleRules)) {
    return false;
  }
  return (
    possibleRules
      .map((rule) => isFieldFilteringRule(rule))
      .findIndex((bool) => bool === false) === -1
  );
}

function isFieldFilteringRule(
  possibleRule: any
): possibleRule is FieldFilteringRule {
  const rule = possibleRule as FieldFilteringRule;
  return (
    !!rule.value &&
    typeof rule.value === 'string' &&
    typeof rule.caseSensitive === 'boolean' &&
    (rule.type === 'filter' || rule.type === 'redact')
  );
}

function createAuthConfig(env: EnvVars): AuthConfig {
  const baseConfig = {
    authUrl: env.authUrl!,
    projectKey: env.projectKey!,
    apiUrl: env.apiUrl!,
  };

  switch (env.authType) {
    case 'client_credentials':
      return {
        type: 'client_credentials',
        clientId: env.clientId!,
        clientSecret: env.clientSecret!,
        ...baseConfig,
      };
    case 'auth_token':
      return {
        type: 'auth_token',
        clientId: env.clientId!,
        clientSecret: env.clientSecret!,
        accessToken: env.accessToken!,
        ...baseConfig,
      };
    default:
      throw new Error(`Unsupported auth type: ${env.authType}`);
  }
}

function handleError(error: any) {
  console.error(red('\n🚨  Error initializing commercetools MCP server:\n'));
  console.error(yellow(`   ${error.message}\n`));
}

export async function main() {
  require('dotenv').config({
    quiet: true,
  });
  const {options, env} = parseArgs(process.argv.slice(2));

  // Create the CommercetoolsCommerceAgent instance
  const selectedTools = options.tools!;
  const configuration: Configuration = {
    actions: {},
    context: {
      customerId: options.customerId,
      isAdmin: options.isAdmin,
      dynamicToolLoadingThreshold: options.dynamicToolLoadingThreshold,
      toolOutputFormat: options.toolOutputFormat,
      cartId: options.cartId,
      storeKey: options.storeKey,
      businessUnitKey: options.businessUnitKey,
      logging: options.logging,
      fieldFiltering: options.fieldFiltering
        ? new FieldFilteringHandler(options.fieldFiltering)
        : undefined,
    },
  };

  if (selectedTools[0] === 'all') {
    ACCEPTED_TOOLS.forEach((tool) => {
      if (!configuration.actions) {
        configuration.actions = {};
      }
      const [namespace, action] = tool.split('.');

      configuration.actions[namespace as AvailableNamespaces] = {
        ...configuration.actions[namespace as AvailableNamespaces],
        [action]: true,
      };
    });
  } else if (selectedTools[0] === 'all.read') {
    ACCEPTED_TOOLS.forEach((tool) => {
      if (!configuration.actions) {
        configuration.actions = {};
      }
      const [namespace, action] = tool.split('.');
      if (action === 'read') {
        configuration.actions[namespace as AvailableNamespaces] = {
          ...configuration.actions[namespace as AvailableNamespaces],
          [action]: true,
        };
      }
    });
  } else {
    selectedTools.forEach((tool: any) => {
      if (!configuration.actions) {
        configuration.actions = {};
      }
      // Trim the tool string before splitting to handle any remaining whitespace
      const trimmedTool = tool.trim();
      const [namespace, action] = trimmedTool
        .split('.')
        .map((part: string) => part.trim());
      if (!namespace || !action) {
        throw new Error(
          `Invalid tool format: ${tool}. Expected format: namespace.action (e.g., products.read)`
        );
      }
      configuration.actions[namespace as AvailableNamespaces] = {
        ...(configuration.actions[namespace as AvailableNamespaces] || {}),
        [action]: true,
      };
    });
  }

  const authConfig = createAuthConfig(env);

  // eslint-disable-next-line require-await
  async function getServer() {
    return CommercetoolsCommerceAgent.create({
      authConfig,
      configuration,
    });
  }

  if (env.remote) {
    const streamServer = new CommercetoolsCommerceAgentStreamable({
      authConfig,
      configuration,
      stateless: env.stateless,
      streamableHttpOptions: {
        sessionIdGenerator: undefined,
      },
    });

    const port = env.port || 8080;
    streamServer.listen(port, function () {
      console.error(`Stream server listening on`, port);
    });
  } else {
    const server = await getServer();
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error('MCP server is running...');
  }
}

if (require.main === module) {
  main().catch((error) => {
    handleError(error);
  });
}
