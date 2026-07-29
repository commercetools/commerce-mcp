import {main} from '../index';
import {
  AuthConfig,
  CommercetoolsCommerceAgent,
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
});
