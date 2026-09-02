import {createHash, randomUUID} from 'node:crypto';
import express from 'express';
import {
  AuthConfig,
  CommercetoolsCommerceAgent,
  Configuration,
} from '../modelcontextprotocol';
// Imported from the module that owns it, not via the barrel: the barrel
// re-exports this file, and a value read through that cycle is undefined.
import {DEFAULT_HOST} from '../shared/constants';
import {StreamableHTTPServerTransport} from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import {isInitializeRequest} from '@modelcontextprotocol/sdk/types.js';
import {IApp, IStreamServerOptions} from '../types/configuration';
import {ExistingTokenAuth as E} from '../types/auth';

export default class CommercetoolsCommerceAgentStreamable {
  private app: IApp;
  private readonly authConfig: AuthConfig;
  private server: (sessionId?: string) => Promise<CommercetoolsCommerceAgent>;
  private transports: {[sessionId: string]: StreamableHTTPServerTransport} = {};
  private sessionTokens: {[sessionId: string]: string} = {};
  private stateless: boolean;
  private enforceAuthHeader: boolean;

  private configuration: Configuration;

  constructor({
    authConfig,
    configuration,

    stateless = true,
    streamableHttpOptions,
    server,
    app,
    enforceAuthHeader = true,
  }: IStreamServerOptions) {
    this.server = server!;
    // Freeze a copy: our shared config cannot be mutated from here, and the
    // caller's object is left alone.
    this.authConfig = authConfig ? Object.freeze({...authConfig}) : authConfig!;
    this.configuration = configuration!;
    this.stateless = stateless;
    this.enforceAuthHeader = enforceAuthHeader;

    // initialize express app
    this.app = app ?? express();
    this.app.use(express.json());

    /**
     * streambale endpoint
     */
    this.app.post('/mcp', async (req, res) => {
      try {
        const authHeader = req.headers.authorization as string | undefined;
        const token = this.extractBearerToken(authHeader);

        /**
         * Mandate a valid Authorization header for all network requests.
         * The server must never fall back to its startup/system credentials
         * for over-the-network transports, otherwise an unauthenticated actor
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

        /**
         * Build a per-request auth config from the caller's token. We never
         * mutate the shared `this.authConfig` (which would leak one request's
         * token into others). Forcing `type: 'auth_token'` ensures the caller's
         * bearer token is the one forwarded to the commercetools API.
         */
        const requestAuthConfig: AuthConfig = token
          ? ({
              ...this.authConfig,
              type: 'auth_token',
              accessToken: token,
            } as E)
          : this.authConfig;

        /**
         * A stateful session holds an agent already bound to the credentials
         * of the caller that opened it, so knowing a session id must not be
         * enough to borrow those credentials: the token has to match too.
         */
        if (!this.isSessionOpener(req.headers['mcp-session-id'], token)) {
          return res.status(403).json({
            jsonrpc: '2.0',
            error: {
              code: -32003,
              message: 'Forbidden: this session belongs to another caller',
            },
            id: null,
          });
        }

        let transport: StreamableHTTPServerTransport;
        let serverInstance = await this.getServer(undefined, requestAuthConfig);

        if (stateless) {
          transport = new StreamableHTTPServerTransport({
            ...streamableHttpOptions,
            sessionIdGenerator: undefined,
          });

          // if stateless then close each transport and server after use
          res.on('close', async () => {
            // close the transport and server
            await transport.close();
            await serverInstance.close();
          });

          // connect server to the transport
          await serverInstance.connect(transport);
        } else {
          const sessionId = req.headers['mcp-session-id'] as string | undefined;
          if (sessionId && this.transports[sessionId]) {
            transport = this.transports[sessionId];
          } else if (!sessionId && isInitializeRequest(req.body)) {
            const generator =
              streamableHttpOptions.sessionIdGenerator &&
              typeof streamableHttpOptions.sessionIdGenerator == 'function'
                ? streamableHttpOptions.sessionIdGenerator
                : randomUUID;

            transport = new StreamableHTTPServerTransport({
              sessionIdGenerator: generator,
              onsessioninitialized: async (sessionId) => {
                // Store the transport by session ID
                this.transports[sessionId] = transport;

                // Remember who may keep using this session
                const fingerprint = this.fingerprintToken(token);
                if (fingerprint) {
                  this.sessionTokens[sessionId] = fingerprint;
                }

                // connect server to the transport
                serverInstance = await this.getServer(
                  sessionId,
                  requestAuthConfig
                );
                await serverInstance.connect(transport);
              },
            });

            // Clean up transport when closed
            transport.onclose = () => {
              if (transport.sessionId) {
                delete this.transports[transport.sessionId];
                delete this.sessionTokens[transport.sessionId];
              }
            };
          } else {
            return res.status(400).json({
              jsonrpc: '2.0',
              error: {
                code: -32000,
                message: 'Bad Request: No valid session ID provided',
              },
              id: null,
            });
          }
        }

        // finally handle requests
        await transport.handleRequest(req, res, req.body);
      } catch (err: unknown) {
        // handle error
        console.error('Error handling request', err);
        if (!res.headersSent) {
          res.status(500).json({
            jsonrpc: '2.0',
            error: {
              code: -32603,
              message: 'Internal server error',
            },
            id: null,
          });
        }
      }
    });

    /**
     * sse endpoint
     *
     * TODO:
     * decide on how to handle SSE requests
     */
    this.app.get('/mcp', (req, res) => {
      const authHeader = req.headers.authorization as string | undefined;
      if (this.enforceAuthHeader && !this.extractBearerToken(authHeader)) {
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
      /* noop */
    });
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
   * Whether `token` may use the given session. Sessions opened without a
   * bearer token (only possible when `enforceAuthHeader` is off) are left
   * unrestricted; every other session requires the token it was opened with.
   */
  private isSessionOpener(
    sessionId: string | string[] | undefined,
    token?: string
  ): boolean {
    if (typeof sessionId !== 'string') return true;

    const opener = this.sessionTokens[sessionId];
    if (!opener) return true;

    return opener === this.fingerprintToken(token);
  }

  /** Truncated SHA-256 of a token, so raw tokens are never held in memory here. */
  private fingerprintToken(token?: string): string | undefined {
    if (!token) return undefined;
    return createHash('sha256').update(token).digest('hex').slice(0, 32);
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
          mode: this.stateless ? 'stateless' : 'stateful',
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
  listen(port: number, cb?: () => void): void;
  listen(port: number, host?: string, cb?: () => void): void;
  listen(port: number, hostOrCb?: string | (() => void), maybeCb?: () => void) {
    const host = typeof hostOrCb === 'string' ? hostOrCb : DEFAULT_HOST;
    const cb = typeof hostOrCb === 'function' ? hostOrCb : maybeCb;

    this.app.listen(port, host, cb);
  }
}
