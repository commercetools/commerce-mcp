/* eslint-disable no-new */
import {randomUUID} from 'node:crypto';
import express, {Express, Request, Response} from 'express';
import {createMcpHandler} from '@modelcontextprotocol/server';
import CommercetoolsCommerceAgentStreamable from '../streamable';
import {DEFAULT_HOST} from '../../shared/constants';
import {CommercetoolsCommerceAgent} from '../../modelcontextprotocol';

jest.mock('node:crypto', () => ({
  ...jest.requireActual('node:crypto'),
  randomUUID: jest.fn(),
}));

jest.mock('express', () => {
  const mockApp = {
    use: jest.fn(),
    post: jest.fn(),
    get: jest.fn(),
    all: jest.fn(),
    listen: jest.fn(),
  };

  const expressFunction = jest.fn(() => mockApp);
  (expressFunction as any).json = jest.fn(() => jest.fn());
  return expressFunction;
});

// These tests cover our routing and guards, not the SDK's Node adapter. The
// real adapter needs a live socket (`res.on`), so it is stubbed and asserted
// on as the delegation target.
const mockNodeHandler = jest.fn();
jest.mock('@modelcontextprotocol/node', () => ({
  toNodeHandler: jest.fn(() => mockNodeHandler),
}));

jest.mock('@modelcontextprotocol/server', () => ({
  ...jest.requireActual('@modelcontextprotocol/server'),
  createMcpHandler: jest.fn(() => ({fetch: jest.fn()})),
}));

jest.mock('../../modelcontextprotocol', () => ({
  CommercetoolsCommerceAgent: {
    create: jest.fn(),
  },
}));

describe('CommercetoolsCommerceAgentStreamable', () => {
  let mockApp: any;
  let mockServer: jest.MockedFunction<() => Promise<any>>;
  let mockCommercetoolsServer: any;

  const mockAuthConfig = {
    accessToken: 'test-token',
    projectKey: 'test-project',
  } as any;

  const mockConfiguration = {
    host: 'test-host',
    apiUrl: 'test-api-url',
  } as any;

  const mockStreamableHttpOptions = {
    sessionIdGenerator: jest.fn().mockReturnValue('custom-session-id'),
  };

  beforeEach(() => {
    jest.clearAllMocks();

    console.error = jest.fn();
    mockApp = {
      use: jest.fn(),
      post: jest.fn(),
      get: jest.fn(),
      all: jest.fn(),
      listen: jest.fn(),
    };
    (express as jest.MockedFunction<typeof express>).mockReturnValue(mockApp);

    mockCommercetoolsServer = {
      connect: jest.fn().mockResolvedValue(undefined),
      close: jest.fn().mockResolvedValue(undefined),
    };
    mockServer = jest.fn().mockResolvedValue(mockCommercetoolsServer);

    mockNodeHandler.mockReset();

    (CommercetoolsCommerceAgent.create as jest.Mock).mockResolvedValue(
      mockCommercetoolsServer
    );

    (randomUUID as jest.Mock).mockReturnValue('mock-uuid-123');
  });

  describe('Constructor', () => {
    test('should initialize with default express app when none provided', () => {
      new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

      expect(express).toHaveBeenCalled();
      expect(mockApp.use).toHaveBeenCalledWith(expect.any(Function));
      // One handler for every method: the SDK answers GET/DELETE with 405,
      // which routing only POST would turn into a 404.
      expect(mockApp.all).toHaveBeenCalledWith('/mcp', expect.any(Function));
    });

    test('should use provided express app', () => {
      const customApp = {...mockApp};
      new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
        app: customApp,
      } as any);

      expect(express).not.toHaveBeenCalled();
      expect(customApp.use).toHaveBeenCalledWith(expect.any(Function));
    });

    test('should setup middleware and routes', () => {
      new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

      expect(mockApp.use).toHaveBeenCalled();
      // One handler for every method: the SDK answers GET/DELETE with 405,
      // which routing only POST would turn into a 404.
      expect(mockApp.all).toHaveBeenCalledWith('/mcp', expect.any(Function));
    });
  });

  describe('POST /mcp endpoint - Stateless mode (default)', () => {
    let instance: CommercetoolsCommerceAgentStreamable;
    let postHandler: (req: any, res: any) => void;
    let mockReq: Partial<Request>;
    let mockRes: Partial<Response>;

    beforeEach(() => {
      instance = new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
        streamableHttpOptions: mockStreamableHttpOptions,
      });

      const postCall = mockApp.all.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      );
      postHandler = postCall[1];

      mockReq = {
        headers: {host: '127.0.0.1:8888', authorization: 'Bearer test-token'},
        body: {method: 'test'},
        method: 'POST',
      };

      mockRes = {
        on: jest.fn(),
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
        headersSent: false,
      };
    });

    test('delegates an authorized request to the SDK handler', async () => {
      mockReq.headers = {
        host: '127.0.0.1:8888',
        authorization: 'Bearer new-auth-token',
      };

      await postHandler(mockReq, mockRes);

      // The SDK adapter owns the response write, including SSE backpressure.
      expect(mockNodeHandler).toHaveBeenCalledWith(
        mockReq,
        mockRes,
        mockReq.body
      );
    });

    test("hands the caller's token to the handler as authInfo", async () => {
      mockReq.headers = {
        host: '127.0.0.1:8888',
        authorization: 'Bearer new-auth-token',
      };

      await postHandler(mockReq, mockRes);

      // `req.auth` is the adapter's documented hand-off to `ctx.authInfo`,
      // which is what builds the per-request auth config.
      expect((mockReq as {auth?: unknown}).auth).toMatchObject({
        token: 'new-auth-token',
      });
    });

    test('should reject request without authorization token with 401', async () => {
      mockReq.headers = {host: '127.0.0.1:8888'};

      await postHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(401);
      expect(mockRes.json).toHaveBeenCalledWith({
        jsonrpc: '2.0',
        error: {
          code: -32001,
          message:
            'Unauthorized: A valid Authorization Bearer token is required',
        },
        id: null,
      });
      expect(mockNodeHandler).not.toHaveBeenCalled();
    });

    test('should reject request with a malformed authorization header with 401', async () => {
      // Missing scheme and empty bearer token are both malformed.
      const malformedHeaders = ['token-without-scheme', 'Bearer ', 'Bearer'];
      await Promise.all(
        malformedHeaders.map((header) => {
          const req = {
            headers: {host: '127.0.0.1:8888', authorization: header},
            body: {method: 'test'},
            method: 'POST',
          };
          const res = {
            on: jest.fn(),
            status: jest.fn().mockReturnThis(),
            json: jest.fn().mockReturnThis(),
            headersSent: false,
          };
          return Promise.resolve(postHandler(req, res)).then(() => {
            expect(res.status).toHaveBeenCalledWith(401);
          });
        })
      );
      expect(mockNodeHandler).not.toHaveBeenCalled();
    });

    test('surfaces a failed server build as an error, not a hang', async () => {
      // The route used to wrap everything in try/catch and answer 500 itself.
      // That went away with the SDK adapter, which owns the response now — so
      // assert the factory's rejection still reaches the handler rather than
      // leaving the request unanswered.
      jest.clearAllMocks();
      const boom = new Error(
        'Unable to initialze `CommercetoolsCommerceAgent`'
      );
      const failing = jest.fn().mockRejectedValue(boom);

      new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: failing,
      } as any);

      const factory = (createMcpHandler as jest.Mock).mock.calls.at(-1)![0] as (
        ctx: unknown
      ) => Promise<unknown>;

      await expect(factory({authInfo: {token: 't'}})).rejects.toThrow(
        'Unable to initialze'
      );
      expect(failing).toHaveBeenCalled();
    });

    // One case per method rather than a loop: each needs its own fresh
    // handler mock, which `beforeEach` already provides.
    test.each(['GET', 'DELETE'])(
      'lets %s through so the SDK can answer 405',
      async (method) => {
        // The 2026-07-28 spec removed the GET endpoint; the handler returns
        // 405. Blocking on auth first would return 401 instead, and these
        // methods carry no credentials to protect.
        const req = {headers: {host: '127.0.0.1:8888'}, method};
        const res = {
          on: jest.fn(),
          status: jest.fn().mockReturnThis(),
          json: jest.fn().mockReturnThis(),
        };

        await postHandler(req, res);

        expect(res.status).not.toHaveBeenCalledWith(401);
        expect(mockNodeHandler).toHaveBeenCalled();
      }
    );
  });

  describe('shared auth config hardening (COM-15-010)', () => {
    test('freezes the startup config so a request cannot mutate it', () => {
      const authConfig = {...mockAuthConfig, accessToken: 'startup-token'};
      const instance = new CommercetoolsCommerceAgentStreamable({
        authConfig,
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

      const shared = (instance as any).authConfig;
      expect(Object.isFrozen(shared)).toBe(true);
      expect(() => {
        shared.accessToken = 'leaked-token';
      }).toThrow(TypeError);
      expect(shared.accessToken).toBe('startup-token');
    });

    test('leaves the startup config untouched after serving a request', async () => {
      jest.clearAllMocks();
      const authConfig = {...mockAuthConfig, accessToken: 'startup-token'};
      const instance = new CommercetoolsCommerceAgentStreamable({
        authConfig,
        configuration: mockConfiguration,
        server: mockServer,
      } as any);
      const postCalls = mockApp.all.mock.calls.filter(
        (call: any) => call[0] === '/mcp'
      );
      const handler = postCalls[postCalls.length - 1][1];

      await handler(
        {
          headers: {
            host: '127.0.0.1:8888',
            authorization: 'Bearer caller-token',
          },
          body: {},
        },
        {
          on: jest.fn(),
          status: jest.fn().mockReturnThis(),
          json: jest.fn().mockReturnThis(),
          headersSent: false,
        }
      );

      expect((instance as any).authConfig.accessToken).toBe('startup-token');
    });
  });

  describe('getServer method (private)', () => {
    test('should return provided server', async () => {
      const instance = new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

      const result = await (instance as any).getServer();

      expect(mockServer).toHaveBeenCalled();
      expect(result).toBe(mockCommercetoolsServer);
    });

    test('should call provided server with the sessionId', async () => {
      const _mockServer = jest
        .fn()
        .mockImplementation((sessionId: string) => mockServer);
      const instance = new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: _mockServer,
      } as any);

      const sessionId = 'test-session-id';
      await (instance as any).getServer(sessionId);

      expect(_mockServer).toHaveBeenCalled();
      expect(_mockServer).toHaveBeenCalledWith(sessionId);
    });

    test('should return provided server with session ID', async () => {
      const instance = new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

      const result = await (instance as any).getServer('test-session-id');

      expect(mockServer).toHaveBeenCalled();
      expect(result).toBe(mockCommercetoolsServer);
    });

    test('reports stateless even when the inert flag asks for stateful', async () => {
      // `stateless: false` no longer changes how the server serves — the
      // 2026-07-28 handler has no sessions. Reporting 'stateful' here would
      // put a mode the server never serves into tool context and its logs.
      const instance = new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        stateless: false,
      } as any);

      const result = await (instance as any).getServer('session-123');

      expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
        authConfig: mockAuthConfig,
        configuration: {
          ...mockConfiguration,
          context: {
            ...mockConfiguration.context,
            mode: 'stateless',
            sessionId: 'session-123',
          },
        },
      });
      expect(result).toBe(mockCommercetoolsServer);
    });

    test('should create server with stateless mode', async () => {
      const instance = new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        stateless: true,
      } as any);

      const result = await (instance as any).getServer();

      expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith({
        authConfig: mockAuthConfig,
        configuration: {
          ...mockConfiguration,
          context: {
            ...mockConfiguration.context,
            mode: 'stateless',
            sessionId: undefined,
          },
        },
      });
      expect(result).toBe(mockCommercetoolsServer);
    });
  });

  describe('Host and Origin validation (COM-15-006)', () => {
    const newRes = () =>
      ({
        on: jest.fn(),
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
        headersSent: false,
      }) as any;

    const handlerFor = (options: Record<string, unknown> = {}) => {
      jest.clearAllMocks();
      new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
        streamableHttpOptions: mockStreamableHttpOptions,
        ...options,
      } as any);

      const calls = mockApp.all.mock.calls.filter(
        (call: any) => call[0] === '/mcp'
      );
      return calls[calls.length - 1][1];
    };

    const call = async (
      handler: (req: any, res: any) => unknown,
      headers: Record<string, string>
    ) => {
      const res = newRes();
      await handler(
        {
          headers: {authorization: 'Bearer test-token', ...headers},
          body: {},
          method: 'POST',
        },
        res
      );
      return res;
    };

    const forbidden = (res: any, fragment: string) => {
      expect(res.status).toHaveBeenCalledWith(403);
      expect(res.json).toHaveBeenCalledWith({
        jsonrpc: '2.0',
        error: {code: -32004, message: expect.stringContaining(fragment)},
        id: null,
      });
    };

    describe('Host header', () => {
      it.each(['127.0.0.1:8888', 'localhost:8888', '[::1]:8888', 'localhost'])(
        'serves the loopback host %s by default',
        async (host) => {
          const res = await call(handlerFor(), {host});

          expect(res.status).not.toHaveBeenCalledWith(403);
        }
      );

      test('rejects a rebound attacker hostname', async () => {
        const res = await call(handlerFor(), {host: 'xxx.attacker.com:8888'});

        forbidden(res, 'Host "xxx.attacker.com" is not an allowed host');
        expect(mockServer).not.toHaveBeenCalled();
      });

      test('rejects a missing Host header', async () => {
        const res = await call(handlerFor(), {});

        forbidden(res, 'missing Host header');
      });

      test('rejects a malformed Host header', async () => {
        const res = await call(handlerFor(), {host: '[::1'});

        forbidden(res, 'malformed Host header');
      });

      test('serves a configured hostname, whatever port it arrives on', async () => {
        const handler = handlerFor({allowedHosts: ['mcp.example.com']});

        const allowed = await call(handler, {host: 'MCP.example.com:9000'});
        expect(allowed.status).not.toHaveBeenCalledWith(403);

        const denied = await call(handler, {host: '127.0.0.1:9000'});
        forbidden(denied, 'not an allowed host');
      });

      test('accepts any host when the list is a wildcard', async () => {
        const res = await call(handlerFor({allowedHosts: ['*']}), {
          host: 'anything.example.com',
        });

        expect(res.status).not.toHaveBeenCalledWith(403);
      });

      test('is checked before authentication', async () => {
        const res = newRes();
        await handlerFor()(
          {headers: {host: 'xxx.attacker.com'}, body: {}},
          res
        );

        // 403 for the wrong host, not 401 for the missing token.
        expect(res.status).toHaveBeenCalledWith(403);
        expect(res.status).not.toHaveBeenCalledWith(401);
      });
    });

    describe('Origin header', () => {
      test('serves requests that carry no Origin, as MCP clients do', async () => {
        const res = await call(handlerFor(), {host: '127.0.0.1:8888'});

        expect(res.status).not.toHaveBeenCalledWith(403);
      });

      test('rejects a browser origin by default', async () => {
        const res = await call(handlerFor(), {
          host: '127.0.0.1:8888',
          origin: 'https://xxx.attacker.com:8080',
        });

        forbidden(
          res,
          'Origin "https://xxx.attacker.com:8080" is not an allowed origin'
        );
      });

      test('serves a configured origin and refuses the rest', async () => {
        const handler = handlerFor({
          allowedOrigins: ['https://app.example.com'],
        });

        const allowed = await call(handler, {
          host: '127.0.0.1:8888',
          origin: 'https://app.example.com',
        });
        expect(allowed.status).not.toHaveBeenCalledWith(403);

        const denied = await call(handler, {
          host: '127.0.0.1:8888',
          origin: 'https://evil.example.com',
        });
        forbidden(denied, 'not an allowed origin');
      });

      test('accepts any origin when the list is a wildcard', async () => {
        const res = await call(handlerFor({allowedOrigins: ['*']}), {
          host: '127.0.0.1:8888',
          origin: 'https://anything.example.com',
        });

        expect(res.status).not.toHaveBeenCalledWith(403);
      });
    });

    test('guards the GET endpoint too', () => {
      const getHandler = handlerFor();
      const res = newRes();

      getHandler(
        {headers: {host: 'xxx.attacker.com', authorization: 'Bearer t'}},
        res
      );

      forbidden(res, 'not an allowed host');
    });
  });

  describe('listen method', () => {
    const build = () =>
      new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

    test('binds loopback by default, keeping the (port, callback) form', () => {
      const callback = jest.fn();

      build().listen(3000, callback);

      expect(mockApp.listen).toHaveBeenCalledWith(3000, '127.0.0.1', callback);
    });

    test('should call app.listen with port only', () => {
      build().listen(8080);

      expect(mockApp.listen).toHaveBeenCalledWith(8080, '127.0.0.1', undefined);
    });

    test('binds the host it is given', () => {
      const callback = jest.fn();

      build().listen(8080, '0.0.0.0', callback);

      expect(mockApp.listen).toHaveBeenCalledWith(8080, '0.0.0.0', callback);
    });

    it.each(['*', ''])(
      'binds every interface when given the %p shorthand',
      (host) => {
        // A literal `*` reaches dns.lookup() and never binds.
        build().listen(8080, host);

        expect(mockApp.listen).toHaveBeenCalledWith(8080, '0.0.0.0', undefined);
      }
    );

    test('returns the server so callers can watch for bind failures', () => {
      const server = {address: () => null};
      mockApp.listen.mockReturnValue(server);

      expect(build().listen(8080)).toBe(server);
    });

    test('exposes the loopback default it applies', () => {
      expect(DEFAULT_HOST).toBe('127.0.0.1');
    });
  });

  describe('GET /mcp endpoint', () => {
    test('should register GET endpoint', () => {
      new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

      const getCall = mockApp.all.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      );
      expect(getCall).toBeDefined();
      expect(getCall[1]).toBeInstanceOf(Function);
    });

    test('should handle authorized GET requests (noop)', () => {
      new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

      const getCall = mockApp.all.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      );

      const getHandler = getCall[1];
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
      };
      getHandler(
        {
          headers: {host: '127.0.0.1:8888', authorization: 'Bearer test-token'},
          method: 'GET',
        },
        mockRes
      );
      expect(mockRes.status).not.toHaveBeenCalledWith(401);
      expect(mockNodeHandler).toHaveBeenCalled();
    });

    test('hands an unauthorized GET to the SDK, which answers 405', async () => {
      // Changed in the 2026-07-28 model: GET is no longer an MCP endpoint, so
      // the SDK returns 405. Rejecting it with 401 first would hide that, and
      // a GET carries no credentials worth protecting.
      new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

      const getHandler = mockApp.all.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      )[1];
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
      };

      await getHandler(
        {headers: {host: '127.0.0.1:8888'}, method: 'GET'},
        mockRes
      );

      expect(mockRes.status).not.toHaveBeenCalledWith(401);
      expect(mockNodeHandler).toHaveBeenCalled();
    });
  });

  describe('Authorization token handling', () => {
    let postHandler: (req: any, res: any) => void;

    /** The per-request factory the route handed to `createMcpHandler`. */
    const serverFactory = () =>
      (createMcpHandler as jest.Mock).mock.calls.at(-1)![0] as (
        ctx: unknown
      ) => Promise<unknown>;

    const newRes = () => ({
      on: jest.fn(),
      status: jest.fn().mockReturnThis(),
      json: jest.fn().mockReturnThis(),
      headersSent: false,
    });

    beforeEach(() => {
      jest.clearAllMocks();
      new CommercetoolsCommerceAgentStreamable({
        authConfig: {...mockAuthConfig, accessToken: 'original-token'},
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

      postHandler = mockApp.all.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      )[1];
    });

    test('accepts a request carrying an Authorization header', async () => {
      const res = newRes();
      await postHandler(
        {
          headers: {
            host: '127.0.0.1:8888',
            authorization: 'Bearer header-token',
          },
          body: {},
          method: 'POST',
        },
        res
      );

      expect(res.status).not.toHaveBeenCalledWith(401);
      expect(mockNodeHandler).toHaveBeenCalled();
    });

    test('should NOT fall back to config token when no header (401)', async () => {
      const res = newRes();
      await postHandler(
        {headers: {host: '127.0.0.1:8888'}, body: {}, method: 'POST'},
        res
      );

      expect(res.status).toHaveBeenCalledWith(401);
      expect(mockNodeHandler).not.toHaveBeenCalled();
    });

    test('builds the per-request server from the caller token, as auth_token', async () => {
      jest.clearAllMocks();
      // No injected `server` factory, so the bootstrapped path runs and
      // CommercetoolsCommerceAgent.create receives the per-request authConfig.
      new CommercetoolsCommerceAgentStreamable({
        authConfig: {
          ...mockAuthConfig,
          type: 'client_credentials',
          clientId: 'startup-client',
          clientSecret: 'startup-secret',
        },
        configuration: mockConfiguration,
      } as any);

      await serverFactory()({authInfo: {token: 'caller-token'}});

      expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith(
        expect.objectContaining({
          authConfig: expect.objectContaining({
            type: 'auth_token',
            accessToken: 'caller-token',
          }),
        })
      );
    });

    test('falls back to the startup config when no caller token is present', async () => {
      jest.clearAllMocks();
      new CommercetoolsCommerceAgentStreamable({
        authConfig: {
          ...mockAuthConfig,
          type: 'client_credentials',
          clientId: 'startup-client',
        },
        configuration: mockConfiguration,
        enforceAuthHeader: false,
      } as any);

      await serverFactory()({});

      expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith(
        expect.objectContaining({
          authConfig: expect.objectContaining({type: 'client_credentials'}),
        })
      );
    });

    test('should allow header-less requests when enforceAuthHeader is false', async () => {
      jest.clearAllMocks();
      new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
        enforceAuthHeader: false,
      } as any);

      const handler = mockApp.all.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      )[1];
      const res = newRes();

      await handler(
        {headers: {host: '127.0.0.1:8888'}, body: {}, method: 'POST'},
        res
      );

      expect(res.status).not.toHaveBeenCalledWith(401);
      expect(mockNodeHandler).toHaveBeenCalled();
    });
  });
});
