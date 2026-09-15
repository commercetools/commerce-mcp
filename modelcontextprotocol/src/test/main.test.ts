import {main} from '../index';
import {
  AuthConfig,
  CommercetoolsCommerceAgent,
  CommercetoolsCommerceAgentStreamable,
  Configuration,
} from '@commercetools/commerce-agent/modelcontextprotocol';
import {StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js';
import {McpServer} from '@modelcontextprotocol/sdk/server/mcp.js';

jest.mock('@commercetools/commerce-agent/modelcontextprotocol', () => ({
  ...jest.requireActual('@commercetools/commerce-agent/modelcontextprotocol'),
}));
jest.mock('@modelcontextprotocol/sdk/server/stdio.js');
jest.mock('@modelcontextprotocol/sdk/server/mcp.js');

describe('main function', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (McpServer as jest.Mock).mockClear();
    jest.mock('dotenv', () => ({
      config: jest.fn().mockResolvedValue({}),
    }));
    process.env = {};

    jest
      .spyOn(CommercetoolsCommerceAgent, 'create')
      .mockImplementation(
        (_: {authConfig: AuthConfig; configuration: Configuration}) =>
          Promise.resolve<any>({
            connect: jest.fn(),
          })
      );
  });

  it('should initialize the server with tools=all correctly', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=all',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {
          products: {read: true, create: true, update: true},
          project: {read: true, update: true},
          'product-search': {read: true},
          category: {read: true, create: true, update: true},
          'product-selection': {read: true, create: true, update: true},
          order: {read: true, create: true, update: true},
          cart: {read: true, create: true, update: true},
          customer: {read: true, create: true, update: true},
          'customer-group': {read: true, create: true, update: true},
          quote: {read: true, create: true, update: true},
          'quote-request': {read: true, create: true, update: true},
          'staged-quote': {read: true, create: true, update: true},
          'standalone-price': {read: true, create: true, update: true},
          'product-discount': {read: true, create: true, update: true},
          'cart-discount': {read: true, create: true, update: true},
          'discount-code': {read: true, create: true, update: true},
          'product-type': {read: true, create: true, update: true},
          inventory: {read: true, create: true, update: true},
          channel: {read: true, create: true, update: true},
          store: {read: true, create: true, update: true},
          review: {read: true, create: true, update: true},
          bulk: {create: true, update: true},
          'business-unit': {read: true, create: true, update: true},
          payments: {read: true, create: true, update: true},
          'shipping-methods': {read: true, create: true, update: true},
          'tax-category': {read: true, create: true, update: true},
          types: {read: true, create: true, update: true},
          zone: {read: true, create: true, update: true},
          'recurring-orders': {read: true, create: true, update: true},
          'shopping-lists': {read: true, create: true, update: true},
          extensions: {read: true, create: true, update: true},
          subscriptions: {read: true, create: true, update: true},
          'payment-methods': {read: true, create: true, update: true},
          'product-tailoring': {read: true, create: true, update: true},
          'custom-objects': {read: true, create: true, update: true},
          'payment-intents': {update: true},
          transactions: {read: true, create: true},
          'approval-flow': {read: true, update: true},
          'approval-rule': {read: true, create: true, update: true},
          'associate-role': {read: true, create: true, update: true},
          'order-edit': {read: true, create: true, update: true},
          'product-selection-assignment': {read: true},
          'recurrence-policy': {read: true, create: true, update: true},
          states: {read: true, create: true, update: true},
        },
        context: {
          isAdmin: true,
          storeKey: undefined,
          cartId: undefined,
          customerId: undefined,
          businessUnitKey: undefined,
          dynamicToolLoadingThreshold: undefined,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with logging option (logging=false)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_products',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
      '--logging=false',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {products: {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with logging option (logging=true)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_products',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
      '--logging=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {products: {read: true}},
        context: {
          isAdmin: true,
          logging: true,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_products)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_products',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {products: {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_products)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_products',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {products: {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_shopping_lists)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_shopping_lists',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'shopping-lists': {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_products)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_products',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {products: {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_project)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_project',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {project: {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_product_search)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_product_search',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'product-search': {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_categories)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_categories',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {category: {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_categories)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_categories',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {category: {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_categories)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_categories',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {category: {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_product_selections)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_product_selections',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'product-selection': {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_product_selections)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_product_selections',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'product-selection': {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_product_selections)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_product_selections',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'product-selection': {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_orders)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_orders',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {order: {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_orders)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_orders',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {order: {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_orders)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_orders',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {order: {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with read_carts tool correctly', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_carts',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {cart: {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with create_carts tool correctly', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_carts',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {cart: {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with update_carts tool correctly', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_carts',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {cart: {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_customers)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_customers',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {customer: {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_customers)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_customers',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {customer: {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_customers)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_customers',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {customer: {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with read_customer_groups tool correctly', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_customer_groups',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'customer-group': {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with create_customer_groups tool correctly', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_customer_groups',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'customer-group': {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with update_customer_groups tool correctly', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_customer_groups',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'customer-group': {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_standalone_prices)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_standalone_prices',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'standalone-price': {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_standalone_prices)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_standalone_prices',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'standalone-price': {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_standalone_prices)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_standalone_prices',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'standalone-price': {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_product_discounts)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_product_discounts',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'product-discount': {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_product_discounts)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_product_discounts',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'product-discount': {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_product_discounts)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_product_discounts',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'product-discount': {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_cart_discounts)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_cart_discounts',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'cart-discount': {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_cart_discounts)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_cart_discounts',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'cart-discount': {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_cart_discounts)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_cart_discounts',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'cart-discount': {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_discount_codes)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_discount_codes',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'discount-code': {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_discount_codes)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_discount_codes',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'discount-code': {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_discount_codes)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_discount_codes',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'discount-code': {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_bulk)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_bulk',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {bulk: {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_bulk)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_bulk',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {bulk: {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_inventory)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_inventory',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {inventory: {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_inventory)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_inventory',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {inventory: {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_inventory)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_inventory',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {inventory: {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_stores)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_stores',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {store: {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_stores)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_stores',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {store: {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_stores)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_stores',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {store: {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_quotes)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_quotes',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {quote: {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_quotes)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_quotes',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {quote: {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_quotes)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_quotes',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {quote: {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (read_staged_quotes)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_staged_quotes',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'staged-quote': {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (create_staged_quotes)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=create_staged_quotes',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'staged-quote': {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with specific tools correctly (update_staged_quotes)', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=update_staged_quotes',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {'staged-quote': {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with customerId and multiple allowed tools', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_products,read_orders,read_carts',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--customerId=xxx',
      '--isAdmin=true',
      '--businessUnitKey=yyy',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {
          products: {read: true},
          order: {read: true},
          cart: {read: true},
        },
        context: {
          customerId: 'xxx',
          isAdmin: true,
          logging: false,
          businessUnitKey: 'yyy',
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it.each([
    {
      authType: 'client_credentials',
      authArgs: [
        '--authType=client_credentials',
        '--clientId=test_client_id',
        '--clientSecret=test_client_secret',
      ],
      expectedAuthConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
    },
    {
      authType: 'auth_token',
      authArgs: ['--authType=auth_token', '--accessToken=test_access_token'],
      expectedAuthConfig: {
        type: 'auth_token',
        accessToken: 'test_access_token',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
    },
  ])(
    'should initialize the server with authType=$authType correctly',
    async ({authType, authArgs, expectedAuthConfig}) => {
      process.argv = [
        'node',
        'index.js',
        '--tools=read_products',
        ...authArgs,
        '--authUrl=https://auth.commercetools.com',
        '--projectKey=test_project',
        '--apiUrl=https://api.commercetools.com',
        '--isAdmin=true',
      ];

      await main();

      expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
        authConfig: expectedAuthConfig,
        configuration: {
          actions: {products: {read: true}},
          context: {
            isAdmin: true,
            logging: false,
          },
        },
      });

      expect(StdioServerTransport).toHaveBeenCalled();
    }
  );

  it('should use client_credentials as default authType when not specified', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=read_products',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--isAdmin=true',
    ];

    await main();

    expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
      authConfig: {
        type: 'client_credentials',
        clientId: 'test_client_id',
        clientSecret: 'test_client_secret',
        authUrl: 'https://auth.commercetools.com',
        projectKey: 'test_project',
        apiUrl: 'https://api.commercetools.com',
      },
      configuration: {
        actions: {products: {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  // Test cases for authType CLI argument
  describe('authType CLI argument', () => {
    beforeEach(() => {
      jest.clearAllMocks();
      jest.mock('dotenv', () => ({
        config: jest.fn().mockResolvedValue({}),
      }));

      jest
        .spyOn(CommercetoolsCommerceAgent, 'create')
        .mockImplementation(
          (_: {authConfig: AuthConfig; configuration: Configuration}) =>
            Promise.resolve<any>({
              connect: jest.fn(),
            })
        );
    });

    it.each([
      {
        authType: 'client_credentials',
        authArgs: [
          '--authType=client_credentials',
          '--clientId=test_client_id',
          '--clientSecret=test_client_secret',
        ],
        expectedAuthConfig: {
          type: 'client_credentials',
          clientId: 'test_client_id',
          clientSecret: 'test_client_secret',
          authUrl: 'https://auth.commercetools.com',
          projectKey: 'test_project',
          apiUrl: 'https://api.commercetools.com',
        },
      },
      {
        authType: 'auth_token',
        authArgs: ['--authType=auth_token', '--accessToken=test_access_token'],
        expectedAuthConfig: {
          type: 'auth_token',
          accessToken: 'test_access_token',
          authUrl: 'https://auth.commercetools.com',
          projectKey: 'test_project',
          apiUrl: 'https://api.commercetools.com',
        },
      },
    ])(
      'should initialize the server with authType=$authType correctly',
      async ({authType, authArgs, expectedAuthConfig}) => {
        process.argv = [
          'node',
          'index.js',
          '--tools=read_products',
          ...authArgs,
          '--authUrl=https://auth.commercetools.com',
          '--projectKey=test_project',
          '--apiUrl=https://api.commercetools.com',
          '--isAdmin=true',
        ];

        await main();

        expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
          authConfig: expectedAuthConfig,
          configuration: {
            actions: {products: {read: true}},
            context: {
              isAdmin: true,
              logging: false,
            },
          },
        });

        expect(StdioServerTransport).toHaveBeenCalled();
      }
    );

    it('should throw error for unsupported authType=password', async () => {
      process.argv = [
        'node',
        'index.js',
        '--tools=read_products',
        '--authType=password',
        '--clientId=test_client_id',
        '--clientSecret=test_client_secret',
        '--authUrl=https://auth.commercetools.com',
        '--projectKey=test_project',
        '--apiUrl=https://api.commercetools.com',
        '--isAdmin=true',
      ];

      await expect(main()).rejects.toThrow(
        'Invalid auth type: password. Supported types are: client_credentials, auth_token'
      );
    });

    it('should use client_credentials as default when authType=empty_string is provided', async () => {
      process.argv = [
        'node',
        'index.js',
        '--tools=read_products',
        '--authType=',
        '--clientId=test_client_id',
        '--clientSecret=test_client_secret',
        '--authUrl=https://auth.commercetools.com',
        '--projectKey=test_project',
        '--apiUrl=https://api.commercetools.com',
        '--isAdmin=true',
      ];

      await main();

      expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
        authConfig: {
          type: 'client_credentials',
          clientId: 'test_client_id',
          clientSecret: 'test_client_secret',
          authUrl: 'https://auth.commercetools.com',
          projectKey: 'test_project',
          apiUrl: 'https://api.commercetools.com',
        },
        configuration: {
          actions: {products: {read: true}},
          context: {
            isAdmin: true,
            logging: false,
          },
        },
      });

      expect(StdioServerTransport).toHaveBeenCalled();
    });
  });

  describe('remote host binding', () => {
    let listenSpy: jest.SpyInstance;

    const remoteArgs = (extra: string[] = []) => [
      'node',
      'index.js',
      '--tools=read_products',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--remote=true',
      ...extra,
    ];

    beforeEach(() => {
      listenSpy = jest
        .spyOn(CommercetoolsCommerceAgentStreamable.prototype, 'listen')
        .mockImplementation(() => undefined);
    });

    afterEach(() => listenSpy.mockRestore());

    it('binds loopback by default', async () => {
      process.argv = remoteArgs();

      await main();

      expect(listenSpy).toHaveBeenCalledWith(
        8080,
        '127.0.0.1',
        expect.any(Function)
      );
    });

    it('binds the host given via --host', async () => {
      process.argv = remoteArgs(['--host=0.0.0.0', '--port=9000']);

      await main();

      expect(listenSpy).toHaveBeenCalledWith(
        9000,
        '0.0.0.0',
        expect.any(Function)
      );
    });

    it.each([
      {host: '0.0.0.0', expected: 'every network interface on this machine'},
      {host: '::', expected: 'every network interface on this machine'},
      {host: '192.168.1.10', expected: 'reachable from outside this machine'},
    ])(
      'names the exposure specific to --host=$host',
      async ({host, expected}) => {
        const errorSpy = jest
          .spyOn(console, 'error')
          .mockImplementation(() => {});

        process.argv = remoteArgs([`--host=${host}`]);
        await main();

        const warning = errorSpy.mock.calls
          .flat()
          .map(String)
          .find((line) => line.includes('The MCP server is'));

        errorSpy.mockRestore();

        expect(warning).toContain(host);
        expect(warning).toContain(expected);
      }
    );

    it('warns when bound beyond loopback, and stays quiet otherwise', async () => {
      const errorSpy = jest
        .spyOn(console, 'error')
        .mockImplementation(() => {});

      process.argv = remoteArgs(['--host=0.0.0.0']);
      await main();
      const warned = errorSpy.mock.calls
        .flat()
        .some((arg) => String(arg).includes('The MCP server is bound to'));

      errorSpy.mockClear();

      process.argv = remoteArgs();
      await main();
      const quiet = !errorSpy.mock.calls
        .flat()
        .some((arg) => String(arg).includes('The MCP server is bound to'));

      errorSpy.mockRestore();

      expect(warned).toBe(true);
      expect(quiet).toBe(true);
    });
  });

  describe('remote host and origin allow-lists', () => {
    let listenSpy: jest.SpyInstance;
    let constructorSpy: jest.SpyInstance;

    const remoteArgs = (extra: string[] = []) => [
      'node',
      'index.js',
      '--tools=read_products',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--remote=true',
      ...extra,
    ];

    beforeEach(() => {
      listenSpy = jest
        .spyOn(CommercetoolsCommerceAgentStreamable.prototype, 'listen')
        .mockImplementation(() => undefined);
      constructorSpy = jest
        .spyOn(console, 'error')
        .mockImplementation(() => {});
    });

    afterEach(() => {
      listenSpy.mockRestore();
      constructorSpy.mockRestore();
    });

    const optionsOf = (instance: any) => ({
      allowedHosts: instance.allowedHosts,
      allowedOrigins: instance.allowedOrigins,
    });

    it('allows loopback out of the box', async () => {
      process.argv = remoteArgs();

      await main();

      expect(optionsOf(listenSpy.mock.instances[0])).toEqual({
        allowedHosts: ['localhost', '127.0.0.1', '[::1]'],
        allowedOrigins: [],
      });
    });

    it('adds the bound interface so the server answers on its own address', async () => {
      process.argv = remoteArgs(['--host=192.168.1.10']);

      await main();

      expect(listenSpy.mock.instances[0].allowedHosts).toEqual(
        expect.arrayContaining(['127.0.0.1', '192.168.1.10'])
      );
    });

    it('does not add a wildcard bind to the allow-list', async () => {
      process.argv = remoteArgs(['--host=0.0.0.0']);

      await main();

      expect(listenSpy.mock.instances[0].allowedHosts).not.toContain('0.0.0.0');
    });

    it('passes --allowedHosts and --allowedOrigins through', async () => {
      process.argv = remoteArgs([
        '--allowedHosts=mcp.example.com',
        '--allowedOrigins=https://app.example.com',
      ]);

      await main();

      expect(optionsOf(listenSpy.mock.instances[0])).toEqual({
        allowedHosts: expect.arrayContaining(['127.0.0.1', 'mcp.example.com']),
        allowedOrigins: ['https://app.example.com'],
      });
    });
  });

  describe('remote bind failures and wildcard hosts', () => {
    let listenSpy: jest.SpyInstance;
    let errorSpy: jest.SpyInstance;

    const remoteArgs = (extra: string[] = []) => [
      'node',
      'index.js',
      '--tools=read_products',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--remote=true',
      ...extra,
    ];

    /**
     * Stands in for the http.Server express returns: `address()` is null until
     * the bind succeeds, and failures arrive as an 'error' event.
     */
    const fakeServer = ({
      address = null,
      error,
    }: {address?: unknown; error?: NodeJS.ErrnoException} = {}) => ({
      address: () => address,
      on: (event: string, listener: (err: NodeJS.ErrnoException) => void) => {
        if (event === 'error' && error) listener(error);
      },
    });

    const loggedLines = () => errorSpy.mock.calls.flat().map(String);

    beforeEach(() => {
      errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    });

    afterEach(() => {
      listenSpy?.mockRestore();
      errorSpy.mockRestore();
      process.exitCode = undefined;
    });

    it('binds every interface for --host=*', async () => {
      listenSpy = jest
        .spyOn(CommercetoolsCommerceAgentStreamable.prototype, 'listen')
        .mockImplementation(() => fakeServer({address: {port: 8080}}));

      process.argv = remoteArgs(['--host=*']);
      await main();

      expect(listenSpy).toHaveBeenCalledWith(
        8080,
        '0.0.0.0',
        expect.any(Function)
      );
      // The warning must name the address actually bound, not the shorthand.
      expect(
        loggedLines().some((line) => line.includes('bound to 0.0.0.0'))
      ).toBe(true);
    });

    it('falls back to loopback for an empty --host= rather than opening up', async () => {
      listenSpy = jest
        .spyOn(CommercetoolsCommerceAgentStreamable.prototype, 'listen')
        .mockImplementation(() => fakeServer({address: {port: 8080}}));

      process.argv = remoteArgs(['--host=']);
      await main();

      expect(listenSpy).toHaveBeenCalledWith(
        8080,
        '127.0.0.1',
        expect.any(Function)
      );
    });

    it('keeps a wildcard shorthand out of the Host allow-list', async () => {
      listenSpy = jest
        .spyOn(CommercetoolsCommerceAgentStreamable.prototype, 'listen')
        .mockImplementation(() => fakeServer({address: {port: 8080}}));

      process.argv = remoteArgs(['--host=*']);
      await main();

      const allowed = listenSpy.mock.instances[0].allowedHosts;
      expect(allowed).not.toContain('*');
      expect(allowed).not.toContain('0.0.0.0');
    });

    it('reports a bind failure instead of exiting silently', async () => {
      listenSpy = jest
        .spyOn(CommercetoolsCommerceAgentStreamable.prototype, 'listen')
        .mockImplementation(() =>
          fakeServer({
            error: Object.assign(new Error('listen EADDRINUSE'), {
              code: 'EADDRINUSE',
            }),
          })
        );

      process.argv = remoteArgs(['--port=8080']);
      await main();

      expect(
        loggedLines().some((line) =>
          line.includes('Unable to bind 127.0.0.1:8080 (EADDRINUSE)')
        )
      ).toBe(true);
      expect(process.exitCode).toBe(1);
    });

    it.each([
      {address: null, bound: false},
      {address: {port: 8080}, bound: true},
    ])(
      'logs "listening" only once the bind took (address: $address)',
      async ({address, bound}) => {
        listenSpy = jest
          .spyOn(CommercetoolsCommerceAgentStreamable.prototype, 'listen')
          .mockImplementation((_port, _host, cb) => {
            const server = fakeServer({address});
            // Express invokes this asynchronously, once the bind resolved.
            setImmediate(() => (cb as () => void)?.());
            return server;
          });

        process.argv = remoteArgs();
        await main();
        await new Promise(setImmediate);

        expect(
          loggedLines().some((line) => line.includes('listening on'))
        ).toBe(bound);
      }
    );
  });
});
