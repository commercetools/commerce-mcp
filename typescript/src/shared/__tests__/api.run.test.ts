import * as platformSdk from '@commercetools/platform-sdk';
import {CustomersHandler} from '@commercetools/tools-core';
import CommercetoolsAPI from '../api';
import type {AuthConfig} from '../../types/auth';

// Keep the ts-client builder inert so the CommercetoolsAPI constructor succeeds.
jest.mock('@commercetools/ts-client', () => {
  const builder = new Proxy(
    {},
    {
      get: (_t, prop) => (prop === 'build' ? () => ({}) : () => builder),
    }
  );
  return {ClientBuilder: jest.fn(() => builder)};
});

jest.mock('@commercetools/platform-sdk', () => ({
  createApiBuilderFromCtpClient: jest.fn(() => ({})),
}));

const authConfig = {
  type: 'auth_token',
  projectKey: 'proj-1',
  apiUrl: 'https://api.europe-west1.gcp.commercetools.com',
  authUrl: 'https://auth.europe-west1.gcp.commercetools.com',
  accessToken: 'tok',
} as unknown as AuthConfig;

describe('CommercetoolsAPI.run bridge dispatch', () => {
  afterEach(() => jest.restoreAllMocks());

  it('routes read_customers into the core CustomersHandler with a self-service scoped context', async () => {
    // Stub the handler execution so the SDK layer is never touched; assert the
    // ToolExecutionContext the bridge builds.
    const executeSpy = jest
      .spyOn(CustomersHandler.prototype, 'execute')
      .mockResolvedValue({id: 'cust-self'});

    const api = new CommercetoolsAPI(authConfig, {customerId: 'cust-self'});
    const result = await api.run('read_customers', {id: 'someone-else'});

    expect(result).toEqual({id: 'cust-self'});
    expect(executeSpy).toHaveBeenCalledTimes(1);
    const ctx = executeSpy.mock.calls[0][0];
    expect(ctx.toolName).toBe('read_customers');
    expect(ctx.configuration.projectKey).toBe('proj-1');
    expect(ctx.configuration.metadata?.customer).toEqual({
      typeId: 'customer',
      id: 'cust-self',
    });
    // params are forwarded (self-service scoping is enforced inside the handler).
    expect(ctx.parameters).toMatchObject({id: 'someone-else'});
  });

  it('injects context.storeKey into parameters for store-scoped calls', async () => {
    const executeSpy = jest
      .spyOn(CustomersHandler.prototype, 'execute')
      .mockResolvedValue({results: []});

    const api = new CommercetoolsAPI(authConfig, {storeKey: 'store-1'});
    await api.run('read_customers', {});

    const ctx = executeSpy.mock.calls[0][0];
    expect(ctx.parameters).toMatchObject({storeKey: 'store-1'});
  });

  it('passes a custom execute function through unchanged', async () => {
    const api = new CommercetoolsAPI(authConfig, {isAdmin: true});
    const execute = jest.fn(() => Promise.resolve('custom-result'));

    const result = await api.run('any_custom_tool', {foo: 'bar'}, execute);

    expect(execute).toHaveBeenCalledTimes(1);
    expect(result).toBe('custom-result');
  });

  it('throws on an unknown method', async () => {
    const api = new CommercetoolsAPI(authConfig, {isAdmin: true});
    await expect(api.run('not_a_real_tool', {})).rejects.toThrow(
      /Invalid method/
    );
  });

  it('uses createApiBuilderFromCtpClient to build the platform apiRoot', () => {
    // eslint-disable-next-line no-new
    new CommercetoolsAPI(authConfig, {isAdmin: true});
    expect(platformSdk.createApiBuilderFromCtpClient).toHaveBeenCalled();
  });
});
