import {AuthConfig, CommercetoolsCommerceAgent} from '../modelcontextprotocol';
import {AvailableNamespaces, Tool} from './tools';
import {IncomingMessage, ServerResponse} from 'node:http';
import {
  FieldFilteringManager,
  FieldFilteringManagerConfig,
} from '@commercetools/processors';

// Actions restrict the subset of API calls that can be made. They should
// be used in conjunction with Restricted API Keys. Setting a permission to false
// prevents the related "tool" from being considered.
export type Permission = 'create' | 'update' | 'read';

export type Actions = {
  [K in AvailableNamespaces]?: {
    [K in Permission]?: boolean;
  };
} & {
  balance?: {
    read?: boolean;
  };
};

// Context are settings that are applied to all requests made by the integration.
export type Context = {
  // Account is a Connected Account ID. If set, the integration will
  // make requests for this Account.
  customerId?: string;
  storeKey?: string;
  distributionChannelId?: string;
  supplyChannelId?: string;
  isAdmin?: boolean;
  cartId?: string;
  businessUnitKey?: string;
  dynamicToolLoadingThreshold?: number;
  sessionId?: string;
  mode?: 'stateless' | 'stateful';
  logging?: boolean;
  toolOutputFormat?: 'json' | 'tabular';
  fieldFiltering?: FieldFilteringManagerConfig | FieldFilteringManager;
};

export type CommercetoolsFuncContext = Context & {
  projectKey: string;
};

// Configuration provides various settings and options for the integration
// to tune and manage how it behaves.
export type Configuration = {
  customTools?: Array<Tool>;
  actions?: Actions;
  context?: Context;
};

type IRequest = {
  headers: Record<string, string | string[] | undefined>;
  body: unknown;
} & IncomingMessage;

type IResponse = {
  headersSent: boolean;
  status: (code: number) => IResponse;
  json: (data: unknown) => void;
  on: (event: string, listener: (...args: unknown[]) => void) => void;
} & ServerResponse<IncomingMessage>;
/**
 * Options that were forwarded to the v1 `StreamableHTTPServerTransport`.
 *
 * @deprecated Inert since the move to `createMcpHandler` (DEVX-886). The
 * 2026-07-28 spec has no protocol sessions, so `sessionIdGenerator` and the
 * other session knobs have nothing to configure. Kept so existing callers
 * still typecheck; it will be removed in the next major.
 */
export type StreamableHttpOptions = Record<string, unknown>;

export interface IApp {
  use: (middleware: any) => void;
  post: (
    path: string,
    handler: (req: IRequest, res: IResponse) => void
  ) => void;
  get: (path: string, handler: (req: IRequest, res: IResponse) => void) => void;
  /**
   * Every method on one path. The 2026-07-28 handler answers GET and DELETE
   * with 405 itself, so routing only POST would return 404 instead.
   */
  all: (path: string, handler: (req: IRequest, res: IResponse) => void) => void;
  listen: (port: number, host: string, cb?: () => void) => unknown;
}

type IWithServerInstance = {
  authConfig?: AuthConfig;
  configuration?: Configuration;
  server: (sessionId?: string) => Promise<CommercetoolsCommerceAgent>;
  stateless?: boolean;
  /** @deprecated See {@link StreamableHttpOptions}. */
  streamableHttpOptions?: StreamableHttpOptions;
  app?: IApp;
  /**
   * When true (default), every HTTP request must carry a valid
   * `Authorization: Bearer <token>` header or it is rejected with 401.
   * Set to false only when the embedding application handles authentication
   * itself (e.g. via the injected `server` factory).
   */
  enforceAuthHeader?: boolean;
  /**
   * Hostnames (without port) this server answers for. Requests whose `Host`
   * header resolves to anything else are rejected with 403, which is what
   * stops a DNS rebinding attack from driving a loopback server through an
   * attacker-controlled hostname. Defaults to localhost/127.0.0.1/[::1];
   * pass `['*']` to accept any host.
   */
  allowedHosts?: string[];
  /**
   * Browser origins allowed to call this server. Requests without an `Origin`
   * header (every non-browser MCP client) are unaffected; a request that
   * carries one must match this list. Defaults to none; pass `['*']` to
   * accept any origin.
   */
  allowedOrigins?: string[];
};

type IWithServerConfig = {
  authConfig: AuthConfig;
  configuration: Configuration;
  server?: undefined;
  stateless?: boolean;
  /** @deprecated See {@link StreamableHttpOptions}. */
  streamableHttpOptions?: StreamableHttpOptions;
  app?: IApp;
  /**
   * When true (default), every HTTP request must carry a valid
   * `Authorization: Bearer <token>` header or it is rejected with 401.
   * Set to false only when the embedding application handles authentication
   * itself (e.g. via the injected `server` factory).
   */
  enforceAuthHeader?: boolean;
  /**
   * Hostnames (without port) this server answers for. Requests whose `Host`
   * header resolves to anything else are rejected with 403, which is what
   * stops a DNS rebinding attack from driving a loopback server through an
   * attacker-controlled hostname. Defaults to localhost/127.0.0.1/[::1];
   * pass `['*']` to accept any host.
   */
  allowedHosts?: string[];
  /**
   * Browser origins allowed to call this server. Requests without an `Origin`
   * header (every non-browser MCP client) are unaffected; a request that
   * carries one must match this list. Defaults to none; pass `['*']` to
   * accept any origin.
   */
  allowedOrigins?: string[];
};

export type IStreamServerOptions = IWithServerInstance | IWithServerConfig;
