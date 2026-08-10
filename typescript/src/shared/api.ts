import {
  Client,
  ClientBuilder,
  MethodType,
  HttpMiddlewareOptions,
  TokenInfo,
  ClientRequest,
} from '@commercetools/ts-client';
import {
  ApiRoot,
  createApiBuilderFromCtpClient,
} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../types/configuration';
import {
  AuthConfig,
  ClientCredentialsAuth,
  ExistingTokenAuth,
  Introspect,
} from '../types/auth';
import pkg from '../../package.json';
import type {
  Configuration as CoreConfiguration,
  IApiClientFactory,
} from '@commercetools/tools-core';
import {
  BridgeApiClientFactory,
  buildCoreConfiguration,
  buildExecutionContext,
  createHandler,
  deriveCheckoutUrl,
  mergeContextIntoParams,
  resolveMethod,
} from './bridge';
import type {BaseResourceHandler} from '@commercetools/tools-core';
import {contextToResourceBasedToolSystemFunctionMapping} from './resource-based-tools-system/functions';

class CommercetoolsAPI {
  private client: Client | undefined;
  private checkoutClient: Client | undefined;
  private authConfig: AuthConfig;
  private context: Context;
  public apiRoot: ApiRoot;

  // Bridge to @commercetools/tools-core resource handlers.
  private bridgeFactory: IApiClientFactory<CoreConfiguration>;
  private coreConfiguration: CoreConfiguration;
  private handlerCache: Map<string, BaseResourceHandler<CoreConfiguration>> =
    new Map();

  constructor(authConfig: AuthConfig, context?: Context) {
    this.context = context!;
    this.authConfig = authConfig;
    this.client = this.createClient();

    if (!this.client) {
      throw new Error('Failed to create client');
    }

    this.apiRoot = createApiBuilderFromCtpClient(this.client);
    this.getApiRoot = this.getApiRoot.bind(this);

    // Core handlers reuse this instance's authenticated client(s).
    this.bridgeFactory = new BridgeApiClientFactory((apiKind) =>
      this.getBridgeClient(apiKind)
    );
    this.coreConfiguration = buildCoreConfiguration(
      this.authConfig,
      this.context
    );
  }

  /** Returns the ts-client for the requested API host, building/caching the checkout client on demand. */
  private getBridgeClient(apiKind: 'platform' | 'checkout'): Client {
    if (apiKind === 'checkout') {
      if (!this.checkoutClient) {
        const checkoutUrl = deriveCheckoutUrl(
          (this.authConfig as {apiUrl?: string}).apiUrl
        );
        this.checkoutClient = this.createClient(
          checkoutUrl ? {apiUrl: checkoutUrl} : undefined
        );
      }
      return this.checkoutClient;
    }
    return this.getClient();
  }

  public getClient(): Client {
    return this.client!;
  }

  private getApiRoot = <T>(
    fn: (client: Client, baseUrl?: string) => T,
    baseUrl?: string
  ): T => {
    return fn(this.createClient({apiUrl: baseUrl}), baseUrl);
  };

  private createClient(options?: Partial<AuthConfig>): Client | never {
    const {authUrl, projectKey, apiUrl} = {
      ...this.authConfig,
      ...options,
    };

    const httpMiddlewareOptions: HttpMiddlewareOptions = {
      host: apiUrl,
    };

    const client = new ClientBuilder()
      .withHttpMiddleware(httpMiddlewareOptions)
      .withConcurrentModificationMiddleware()
      .withCorrelationIdMiddleware()
      .withUserAgentMiddleware({
        libraryName: 'commerce-mcp',
        libraryVersion: pkg.version,
      })
      .withLoggerMiddleware({
        loggerFn: ({headers}) => {
          const {sessionId, mode} = this.context;
          // eslint-disable-next-line
          this.context.logging &&
            console.error(
              JSON.stringify({
                mode,
                ...(mode == 'stateful' && {sessionId}),
                correlationId: `${headers?.['x-correlation-id']}`,
              })
            );
        },
      });

    if (this.authConfig.type === 'client_credentials') {
      return client
        .withClientCredentialsFlow({
          host: authUrl,
          projectKey: projectKey,
          credentials: {
            clientId: this.authConfig.clientId,
            clientSecret: this.authConfig.clientSecret,
          },
        })
        .build();
    }

    if (this.authConfig.type === 'auth_token') {
      const authorizationHeader = `Bearer ${this.authConfig.accessToken}`;
      return client
        .withExistingTokenFlow(authorizationHeader, {force: true})
        .build();
    }

    this.handleUnrecognizedAuthConfig(this.authConfig);
  }

  private handleUnrecognizedAuthConfig(authConfig: AuthConfig): never {
    throw new Error(`Unrecognized auth type: ${authConfig.type}`);
  }

  private async getToken(): Promise<string> {
    const authToken = (this.authConfig as ExistingTokenAuth).accessToken;
    if (authToken) return Promise.resolve(authToken);

    const {clientId, clientSecret} = this.authConfig as ClientCredentialsAuth;
    const req: ClientRequest = {
      uri: `/oauth/token`,
      method: 'POST' as MethodType,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        Authorization: `Basic ${Buffer.from(
          `${clientId}:${clientSecret}`
        ).toString('base64')}`,
      },
      body: `grant_type=client_credentials`,
    };

    const tokenObject = await this.getAuthClient().execute<TokenInfo>(req);
    return tokenObject.body!.access_token;
  }

  private getAuthClient(): Client {
    return new ClientBuilder()
      .withUserAgentMiddleware({
        libraryName: 'commerce-mcp',
        libraryVersion: pkg.version,
      })
      .withHttpMiddleware({
        host: this.authConfig.authUrl,
        stringBodyContentTypes: ['application/x-www-form-urlencoded'],
        httpClient: fetch,
      })
      .build();
  }

  async introspect(): Promise<Array<string>> {
    const token = await this.getToken();
    const {clientId, clientSecret} = this.authConfig as ClientCredentialsAuth;

    const req: ClientRequest = {
      uri: `/oauth/introspect`,
      method: 'POST' as MethodType,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        Authorization: `Basic ${Buffer.from(
          `${clientId}:${clientSecret}`
        ).toString('base64')}`,
      },
      body: `token=${token}`,
    };

    const res = await this.getAuthClient().execute<Introspect>(req);

    // check if token is active/valid
    if (!res.body?.active) {
      throw new Error(
        'Inactive or invalid auth token, please provide a valid token'
      );
    }

    return res.body?.scope.split(' ').map((scope) => scope.split(':')[0]) || [];
  }

  // eslint-disable-next-line require-await
  async run(
    method: string,
    arg: any,
    execute?: (args: Record<string, unknown>, api: ApiRoot) => Promise<unknown>
  ): Promise<unknown> {
    // handle custom tool execution
    if (execute && typeof execute == 'function') {
      return execute(arg, this.apiRoot);
    }

    // handle the dynamic (resource-based) tool-system meta tools, which are
    // not backed by a core resource handler.
    const metaFunctionMap = contextToResourceBasedToolSystemFunctionMapping(
      this.context
    );
    const metaFunc = metaFunctionMap[method];
    if (metaFunc) {
      return metaFunc(
        this.apiRoot,
        {projectKey: this.authConfig.projectKey, ...this.context},
        arg
      );
    }

    // handle core tool execution via @commercetools/tools-core handlers
    const resolved = resolveMethod(method);
    if (!resolved) {
      throw new Error('Invalid method ' + method);
    }
    const {def} = resolved;

    let handler = this.handlerCache.get(def.nsKey);
    if (!handler) {
      handler = createHandler(def, this.bridgeFactory);
      this.handlerCache.set(def.nsKey, handler);
    }

    const params = mergeContextIntoParams(
      def,
      (arg ?? {}) as Record<string, unknown>,
      this.context
    );
    const authToken = (this.authConfig as ExistingTokenAuth).accessToken ?? '';
    const executionContext = buildExecutionContext(
      method,
      params,
      this.coreConfiguration,
      authToken,
      this.context?.sessionId
    );

    return handler.execute(executionContext);
  }
}

export default CommercetoolsAPI;
