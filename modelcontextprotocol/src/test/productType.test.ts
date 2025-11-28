import {main} from '..';
import {
  AuthConfig,
  CommercetoolsCommerceAgent,
  Configuration,
} from '@commercetools/commerce-agent/modelcontextprotocol';
import {StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js';

// Mock these imports
jest.mock('@commercetools/commerce-agent/modelcontextprotocol');
jest.mock('@modelcontextprotocol/sdk/server/stdio.js');

describe('Product Type Tools', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest
      .spyOn(CommercetoolsCommerceAgent, 'create')
      .mockImplementation(
        (_: {authConfig: AuthConfig; configuration: Configuration}) =>
          Promise.resolve<any>({
            connect: jest.fn(),
          })
      );
    jest.mock('dotenv', () => ({
      config: jest.fn().mockResolvedValue({}),
    }));
    process.env = {};
  });

  it('should initialize the server with product-type.read tool correctly', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=product-type.read',
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
        actions: {'product-type': {read: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });

  it('should initialize the server with product-type.create tool correctly', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=product-type.create',
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
        actions: {'product-type': {create: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });
  });

  it('should initialize the server with product-type.update tool correctly', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=product-type.update',
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
        actions: {'product-type': {update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });
  });

  it('should initialize the server with multiple product-type tools correctly', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=product-type.read,product-type.create,product-type.update',
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
        actions: {'product-type': {read: true, create: true, update: true}},
        context: {
          isAdmin: true,
          logging: false,
        },
      },
    });
  });

  it('should correctly pass customerId to configuration.context', async () => {
    process.argv = [
      'node',
      'index.js',
      '--tools=product-type.read',
      '--clientId=test_client_id',
      '--clientSecret=test_client_secret',
      '--authUrl=https://auth.commercetools.com',
      '--projectKey=test_project',
      '--apiUrl=https://api.commercetools.com',
      '--customerId=xxx',
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
        actions: {'product-type': {read: true}},
        context: {
          customerId: 'xxx',
          isAdmin: true,
          logging: false,
        },
      },
    });

    expect(StdioServerTransport).toHaveBeenCalled();
  });
});
