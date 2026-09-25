import express from 'express';
import {
  AuthConfig,
  CommercetoolsCommerceAgent,
  Configuration,
} from '../modelcontextprotocol';
// Imported from the module that owns it, not via the barrel: the barrel
// re-exports this file, and a value read through that cycle is undefined.
import {
  DEFAULT_HOST,
  LOOPBACK_HOSTNAMES,
  normalizeBindHost,
} from '../shared/constants';
import {
  createMcpHandler,
  validateHostHeader,
} from '@modelcontextprotocol/server';
import {toNodeHandler} from '@modelcontextprotocol/node';
import {IApp, IStreamServerOptions} from '../types/configuration';
import {ExistingTokenAuth as E} from '../types/auth';

export default class CommercetoolsCommerceAgentStreamable {
  private app: IApp;
  private readonly authConfig: AuthConfig;
  private server: (sessionId?: string) => Promise<CommercetoolsCommerceAgent>;
  /**
   * Accepted for API compatibility and otherwise unused. The 2026-07-28 spec
   * has no protocol sessions, so the handler always serves statelessly
   * (DEVX-888) whatever this says.
   */
  private readonly stateless: boolean;
  private enforceAuthHeader: boolean;
  /** Hostnames (no port) this server answers for; `*` disables the check. */
  private allowedHosts: string[];
  /** Browser origins allowed to call this server; `*` disables the check. */
  private allowedOrigins: string[];

  private configuration: Configuration;

  constructor({
    authConfig,
    configuration,

    stateless = true,
    streamableHttpOptions,
    server,
    app,
    enforceAuthHeader = true,
    allowedHosts = LOOPBACK_HOSTNAMES,
    allowedOrigins = [],
  }: IStreamServerOptions) {
    this.server = server!;
    // Freeze a copy: our shared config cannot be mutated from here, and the
    // caller's object is left alone.
    this.authConfig = authConfig ? Object.freeze({...authConfig}) : authConfig!;
    this.configuration = configuration!;
    this.stateless = stateless;
    this.enforceAuthHeader = enforceAuthHeader;
    this.allowedHosts = allowedHosts;
    this.allowedOrigins = allowedOrigins;

    // initialize express app
    this.app = app ?? express();
    this.app.use(express.json());

    /**
     * One endpoint, both protocol eras.
     *
     * `createMcpHandler` builds a server per request from that request's
     * credentials, which is exactly what `getServer` already did. `legacy:
     * 'stateless'` keeps 2025-era clients working: their `initialize` still
     * negotiates, they just never get a session id.
     */
    const handler = createMcpHandler(
      (ctx) =>
        this.getServer(undefined, this.authConfigFor(ctx.authInfo?.token)),
      {
        legacy: 'stateless',
        responseMode: 'auto',
        onerror: (error: unknown) =>
          console.error('[mcp]', (error as Error)?.message ?? error),
      }
    );

    /**
     * The SDK's Node adapter owns the response write, including SSE
     * backpressure. Hand-rolling that bridge means client input flows back
     * through our own `res.send`, which SAST flags as a reflected-XSS shape.
     */
    const mcp = toNodeHandler(handler, {
      onerror: (error: unknown) =>
        console.error('[mcp:adapter]', (error as Error)?.message ?? error),
    });

    this.app.all('/mcp', (req, res) => {
      /**
       * Answer only for hostnames and origins we recognise. A DNS rebinding
       * attack reaches a loopback server through an attacker-controlled
       * hostname, which the browser still treats as same-origin — the `Host`
       * header is what gives it away. Checked before authentication so a
       * rebound request is turned away without touching credentials.
       */
      const untrusted = this.findUntrustedTarget(req.headers);
      if (untrusted) {
        return res.status(403).json({
          jsonrpc: '2.0',
          error: {code: -32004, message: untrusted},
          id: null,
        });
      }

      const token = this.extractBearerToken(
        req.headers.authorization as string | undefined
      );

      // `req.auth` is the adapter's documented hand-off to the handler's
      // pass-through `authInfo`; it never inspects headers or verifies tokens.
      if (token) {
        (req as {auth?: unknown}).auth = {
          token,
          clientId: 'commerce-mcp',
          scopes: [],
        };
      }

      /**
       * Let the SDK answer non-POST, so GET and DELETE return the 405 the
       * 2026-07-28 spec mandates rather than a 401. Those methods carry no
       * credentials to protect.
       */
      if (req.method !== 'POST') {
        return mcp(req, res, (req as {body?: unknown}).body);
      }

      /**
       * Mandate a valid Authorization header for all network requests. The
       * server must never fall back to its startup credentials for
       * over-the-network transports, otherwise an unauthenticated actor
       * would inherit the configured token's privileges.
       */
      if (this.enforceAuthHeader && !token) {
        return res.status(401).json({
          jsonrpc: '2.0',
          error: {
            code: -32001,
            message:
              'Unauthorized: A valid Authorization Bearer token is required',
          },
          id: null,
        });
      }

      return mcp(req, res, (req as {body?: unknown}).body);
    });
  }

  /**
   * A per-request auth config built from the caller's token. The shared
   * `this.authConfig` is never mutated — that would leak one request's token
   * into the next. Forcing `type: 'auth_token'` ensures the caller's bearer
   * token is the one forwarded to the commercetools API.
   */
  private authConfigFor(token?: string): AuthConfig {
    if (!token) return this.authConfig;
    return {...this.authConfig, type: 'auth_token', accessToken: token} as E;
  }

  /**
   * Extracts the bearer token from an Authorization header. Returns the token
   * only for a well-formed `Bearer <non-empty-token>` value (scheme is
   * case-insensitive); otherwise returns undefined. Structural validation only
   * — the token's actual validity is enforced by the commercetools API.
   */
  private extractBearerToken(authHeader?: string): string | undefined {
    if (!authHeader) return undefined;
    const [scheme, ...rest] = authHeader.trim().split(/\s+/);
    if (scheme?.toLowerCase() !== 'bearer') return undefined;
    const token = rest.join(' ').trim();
    return token.length > 0 ? token : undefined;
  }

  /**
   * Returns why a request's `Host`/`Origin` is not trusted, or undefined when
   * both are acceptable. `Host` is matched on hostname only, so the port the
   * server happens to run on does not have to be configured.
   */
  private findUntrustedTarget(
    headers: Record<string, string | string[] | undefined>
  ): string | undefined {
    return (
      this.findUntrustedHost(headers.host) ??
      this.findUntrustedOrigin(headers.origin)
    );
  }

  /**
   * Delegates `Host` parsing and matching to the SDK's `validateHostHeader`,
   * which has the same port-agnostic, hostname-allowlist semantics we had
   * (including bracketed IPv6). The wildcard and our message wording stay
   * here, so `--allowedHosts` behaves exactly as before.
   */
  private findUntrustedHost(host?: string | string[]): string | undefined {
    if (this.allowedHosts.includes('*')) return undefined;

    const header = typeof host === 'string' ? host : undefined;
    const result = validateHostHeader(header, this.allowedHosts);
    if (result.ok) return undefined;

    switch (result.errorCode) {
      case 'missing_host':
        return 'Forbidden: missing Host header';
      case 'invalid_host_header':
        return 'Forbidden: malformed Host header';
      default:
        return `Forbidden: Host "${result.hostname ?? header}" is not an allowed host for this server`;
    }
  }

  /**
   * Deliberately not delegated to the SDK's `validateOriginHeader`: that one
   * matches on hostname only, so a list of `https://app.example.com` would
   * start accepting `http://app.example.com` and any port. Our
   * `--allowedOrigins` values are full origins and are compared as such.
   */
  private findUntrustedOrigin(origin?: string | string[]): string | undefined {
    // Non-browser MCP clients send no Origin, and have nothing to spoof.
    if (typeof origin !== 'string' || origin.trim().length === 0)
      return undefined;
    if (this.allowedOrigins.includes('*')) return undefined;

    return this.isAllowed(origin, this.allowedOrigins)
      ? undefined
      : `Forbidden: Origin "${origin}" is not an allowed origin for this server`;
  }

  private isAllowed(value: string, allowList: string[]): boolean {
    const candidate = value.trim().toLowerCase();
    return allowList.some((entry) => entry.trim().toLowerCase() === candidate);
  }

  // eslint-disable-next-line require-await
  private async getServer(
    id?: string,
    authConfig: AuthConfig = this.authConfig
  ): Promise<CommercetoolsCommerceAgent> {
    if (this.server) return this.server(id);
    return CommercetoolsCommerceAgent.create({
      authConfig,
      configuration: {
        ...this.configuration,
        context: {
          ...this.configuration.context,
          // Always stateless: the 2026-07-28 handler has no sessions, so
          // reporting 'stateful' because the inert flag says so would put a
          // mode the server never serves into tool context and its logs.
          mode: 'stateless',
          sessionId: id,
        },
      },
    });
  }

  /**
   * Binds the HTTP server. Without an explicit `host` the server listens on
   * loopback only; widening it to other interfaces has to be asked for.
   * The `(port, callback)` form is still accepted.
   */
  listen(port: number, cb?: () => void): unknown;
  listen(port: number, host?: string, cb?: () => void): unknown;
  listen(
    port: number,
    hostOrCb?: string | (() => void),
    maybeCb?: () => void
  ): unknown {
    const host =
      typeof hostOrCb === 'string' ? normalizeBindHost(hostOrCb) : DEFAULT_HOST;
    const cb = typeof hostOrCb === 'function' ? hostOrCb : maybeCb;

    // Returned so callers can watch for a bind failure, which arrives as an
    // 'error' event rather than as a thrown error.
    return this.app.listen(port, host, cb);
  }
}
