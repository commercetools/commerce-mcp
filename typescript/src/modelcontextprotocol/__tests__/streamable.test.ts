/* eslint-disable no-new */
import {randomUUID} from 'node:crypto';
import express, {Express, Request, Response} from 'express';
import CommercetoolsCommerceAgentStreamable from '../streamable';
import {DEFAULT_HOST} from '../../shared/constants';
import {StreamableHTTPServerTransport} from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import {isInitializeRequest} from '@modelcontextprotocol/sdk/types.js';
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
    listen: jest.fn(),
  };

  const expressFunction = jest.fn(() => mockApp);
  (expressFunction as any).json = jest.fn(() => jest.fn());
  return expressFunction;
});

jest.mock('@modelcontextprotocol/sdk/server/streamableHttp.js', () => ({
  StreamableHTTPServerTransport: jest.fn(),
}));

jest.mock('@modelcontextprotocol/sdk/types.js', () => ({
  isInitializeRequest: jest.fn(),
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
  let mockTransport: any;

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
      listen: jest.fn(),
    };
    (express as jest.MockedFunction<typeof express>).mockReturnValue(mockApp);

    mockCommercetoolsServer = {
      connect: jest.fn().mockResolvedValue(undefined),
      close: jest.fn().mockResolvedValue(undefined),
    };
    mockServer = jest.fn().mockResolvedValue(mockCommercetoolsServer);

    mockTransport = {
      handleRequest: jest.fn().mockResolvedValue(undefined),
      close: jest.fn().mockResolvedValue(undefined),
      sessionId: 'test-session-id',
      onclose: undefined,
    };
    (StreamableHTTPServerTransport as jest.Mock).mockImplementation(
      () => mockTransport
    );

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
      expect(mockApp.post).toHaveBeenCalledWith('/mcp', expect.any(Function));
      expect(mockApp.get).toHaveBeenCalledWith('/mcp', expect.any(Function));
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
      expect(mockApp.post).toHaveBeenCalledWith('/mcp', expect.any(Function));
      expect(mockApp.get).toHaveBeenCalledWith('/mcp', expect.any(Function));
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

      const postCall = mockApp.post.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      );
      postHandler = postCall[1];

      mockReq = {
        headers: {authorization: 'Bearer test-token'},
        body: {method: 'test'},
      };

      mockRes = {
        on: jest.fn(),
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
        headersSent: false,
      };
    });

    test('should handle request with authorization token', async () => {
      mockReq.headers = {authorization: 'Bearer new-auth-token'};

      await postHandler(mockReq, mockRes);

      expect(StreamableHTTPServerTransport).toHaveBeenCalledWith({
        ...mockStreamableHttpOptions,
        sessionIdGenerator: undefined,
      });
      expect(mockServer).toHaveBeenCalled();
      expect(mockCommercetoolsServer.connect).toHaveBeenCalledWith(
        mockTransport
      );
      expect(mockTransport.handleRequest).toHaveBeenCalledWith(
        mockReq,
        mockRes,
        mockReq.body
      );
    });

    test('should reject request without authorization token with 401', async () => {
      mockReq.headers = {};

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
      expect(mockServer).not.toHaveBeenCalled();
      expect(mockTransport.handleRequest).not.toHaveBeenCalled();
    });

    test('should reject request with a malformed authorization header with 401', async () => {
      // Missing scheme and empty bearer token are both malformed.
      const malformedHeaders = ['token-without-scheme', 'Bearer ', 'Bearer'];
      await Promise.all(
        malformedHeaders.map((header) => {
          const req = {
            headers: {authorization: header},
            body: {method: 'test'},
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
      expect(mockServer).not.toHaveBeenCalled();
      expect(mockTransport.handleRequest).not.toHaveBeenCalled();
    });

    test('should setup cleanup on response close', async () => {
      await postHandler(mockReq, mockRes);

      expect(mockRes.on).toHaveBeenCalledWith('close', expect.any(Function));

      const closeHandler = (mockRes.on as jest.Mock).mock.calls[0][1];
      await closeHandler();

      expect(mockTransport.close).toHaveBeenCalled();
      expect(mockCommercetoolsServer.close).toHaveBeenCalled();
    });

    test('should handle transport errors gracefully', async () => {
      const error = new Error('Transport error');
      mockTransport.handleRequest.mockRejectedValue(error);

      await postHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(500);
      expect(mockRes.json).toHaveBeenCalledWith({
        jsonrpc: '2.0',
        error: {
          code: -32603,
          message: 'Internal server error',
        },
        id: null,
      });
    });

    test('should not send error response if headers already sent', async () => {
      mockRes.headersSent = true;
      mockTransport.handleRequest.mockRejectedValue(new Error('Test error'));

      await postHandler(mockReq, mockRes);

      expect(console.error).toHaveBeenCalled();
      expect(mockRes.status).not.toHaveBeenCalled();
      expect(mockRes.json).not.toHaveBeenCalled();
    });
  });

  describe('POST /mcp endpoint - Stateful mode', () => {
    let instance: CommercetoolsCommerceAgentStreamable;
    let postHandler: (req: any, res: any) => void;
    let mockReq: Partial<Request>;
    let mockRes: Partial<Response>;

    beforeEach(() => {
      instance = new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
        stateless: false,
        streamableHttpOptions: mockStreamableHttpOptions,
      });

      const postCall = mockApp.post.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      );
      postHandler = postCall[1];

      mockReq = {
        headers: {authorization: 'Bearer test-token'},
        body: {method: 'initialize', params: {}},
      };

      mockRes = {
        on: jest.fn(),
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
        headersSent: false,
      };
    });

    test('should create new transport for initialize request', async () => {
      (isInitializeRequest as unknown as jest.Mock).mockReturnValue(true);

      await postHandler(mockReq, mockRes);
      const transportCall = (StreamableHTTPServerTransport as jest.Mock).mock
        .calls[0][0];

      transportCall.onsessioninitialized('existing-session-id');
      await new Promise(setImmediate);

      expect(StreamableHTTPServerTransport).toHaveBeenCalledWith({
        sessionIdGenerator: mockStreamableHttpOptions.sessionIdGenerator,
        onsessioninitialized: expect.any(Function),
      });
      expect(mockCommercetoolsServer.connect).toHaveBeenCalledWith(
        mockTransport
      );
    });

    test('should use randomUUID when sessionIdGenerator not provided', async () => {
      instance = new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
        stateless: false,
        streamableHttpOptions: {
          sessionIdGenerator: undefined,
        },
      });
      const postCall = mockApp.post.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      );
      postHandler = postCall[1];
      (isInitializeRequest as unknown as jest.Mock).mockReturnValue(true);
      await postHandler(mockReq, mockRes);
      expect(StreamableHTTPServerTransport).toHaveBeenCalled();
    });

    test('should return 400 for invalid session request', async () => {
      (isInitializeRequest as unknown as jest.Mock).mockReturnValue(false);
      mockReq.headers = {authorization: 'Bearer test-token'}; // No session ID

      await postHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(400);
      expect(mockRes.json).toHaveBeenCalledWith({
        jsonrpc: '2.0',
        error: {
          code: -32000,
          message: 'Bad Request: No valid session ID provided',
        },
        id: null,
      });
    });

    test('should handle existing session ID', async () => {
      (isInitializeRequest as unknown as jest.Mock).mockReturnValue(true);
      await postHandler(mockReq, mockRes);

      const transportCall = (StreamableHTTPServerTransport as jest.Mock).mock
        .calls[0][0];
      transportCall.onsessioninitialized('existing-session-id');

      jest.clearAllMocks();
      mockReq.headers = {
        authorization: 'Bearer test-token',
        'mcp-session-id': 'existing-session-id',
      };

      await postHandler(mockReq, mockRes);

      expect(StreamableHTTPServerTransport).not.toHaveBeenCalled();
      expect(mockTransport.handleRequest).toHaveBeenCalledWith(
        mockReq,
        mockRes,
        mockReq.body
      );
    });

    test('should setup transport cleanup on close', async () => {
      (isInitializeRequest as unknown as jest.Mock).mockReturnValue(true);

      await postHandler(mockReq, mockRes);

      expect(typeof mockTransport.onclose).toBe('function');

      // Simulate transport close
      mockTransport.onclose();
      expect(mockTransport.onclose).toBeDefined();
    });
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
      const postCalls = mockApp.post.mock.calls.filter(
        (call: any) => call[0] === '/mcp'
      );
      const handler = postCalls[postCalls.length - 1][1];

      await handler(
        {headers: {authorization: 'Bearer caller-token'}, body: {}},
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

  describe('POST /mcp endpoint - session binding (stateful)', () => {
    const newRes = () =>
      ({
        on: jest.fn(),
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
        headersSent: false,
      }) as any;

    const buildInstance = (options: Record<string, unknown> = {}) => {
      jest.clearAllMocks();
      const instance = new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
        stateless: false,
        streamableHttpOptions: mockStreamableHttpOptions,
        ...options,
      } as any);

      const postCalls = mockApp.post.mock.calls.filter(
        (call: any) => call[0] === '/mcp'
      );
      return {instance, handler: postCalls[postCalls.length - 1][1]};
    };

    const openSession = async (
      handler: (req: any, res: any) => Promise<void>,
      token: string | undefined,
      sessionId: string
    ) => {
      (isInitializeRequest as unknown as jest.Mock).mockReturnValue(true);
      await handler(
        {
          headers: token ? {authorization: `Bearer ${token}`} : {},
          body: {method: 'initialize', params: {}},
        },
        newRes()
      );

      const transportOptions = (
        StreamableHTTPServerTransport as jest.Mock
      ).mock.calls.slice(-1)[0][0];
      await transportOptions.onsessioninitialized(sessionId);
      await new Promise(setImmediate);
    };

    const continueSession = async (
      handler: (req: any, res: any) => Promise<void>,
      token: string | undefined,
      sessionId: string
    ) => {
      (isInitializeRequest as unknown as jest.Mock).mockReturnValue(false);
      const res = newRes();
      mockTransport.handleRequest.mockClear();
      await handler(
        {
          headers: {
            ...(token ? {authorization: `Bearer ${token}`} : {}),
            'mcp-session-id': sessionId,
          },
          body: {method: 'tools/list', params: {}},
        },
        res
      );
      return res;
    };

    test('rejects another caller reusing a session id with 403', async () => {
      const {handler} = buildInstance();
      await openSession(handler, 'victim-token', 'session-1');

      const res = await continueSession(handler, 'attacker-token', 'session-1');

      expect(res.status).toHaveBeenCalledWith(403);
      expect(res.json).toHaveBeenCalledWith({
        jsonrpc: '2.0',
        error: {
          code: -32003,
          message: 'Forbidden: this session belongs to another caller',
        },
        id: null,
      });
      expect(mockTransport.handleRequest).not.toHaveBeenCalled();
    });

    test('rejects a session-id-only request when the header is dropped', async () => {
      const {handler} = buildInstance({enforceAuthHeader: false});
      await openSession(handler, 'victim-token', 'session-1');

      const res = await continueSession(handler, undefined, 'session-1');

      expect(res.status).toHaveBeenCalledWith(403);
      expect(mockTransport.handleRequest).not.toHaveBeenCalled();
    });

    test('lets the opener keep using its own session', async () => {
      const {handler} = buildInstance();
      await openSession(handler, 'victim-token', 'session-1');

      const res = await continueSession(handler, 'victim-token', 'session-1');

      expect(res.status).not.toHaveBeenCalledWith(403);
      expect(mockTransport.handleRequest).toHaveBeenCalled();
    });

    test('does not restrict sessions opened without a token', async () => {
      const {handler} = buildInstance({enforceAuthHeader: false});
      await openSession(handler, undefined, 'session-1');

      const res = await continueSession(handler, 'any-token', 'session-1');

      expect(res.status).not.toHaveBeenCalledWith(403);
    });

    test('forgets the session token when the transport closes', async () => {
      const {instance, handler} = buildInstance();
      await openSession(handler, 'victim-token', 'session-1');

      expect((instance as any).sessionTokens['session-1']).toBeDefined();

      mockTransport.sessionId = 'session-1';
      mockTransport.onclose();

      expect((instance as any).sessionTokens['session-1']).toBeUndefined();
      expect((instance as any).transports['session-1']).toBeUndefined();
    });

    test('never keeps the raw token in the session map', async () => {
      const {instance, handler} = buildInstance();
      await openSession(handler, 'victim-token', 'session-1');

      expect(Object.values((instance as any).sessionTokens)).not.toContain(
        'victim-token'
      );
    });

    test('ignores an unknown session id, leaving the 400 path intact', async () => {
      const {handler} = buildInstance();

      const res = await continueSession(handler, 'some-token', 'never-opened');

      expect(res.status).toHaveBeenCalledWith(400);
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

    test('should create server when not provided', async () => {
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
            mode: 'stateful',
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

      const getCall = mockApp.get.mock.calls.find(
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

      const getCall = mockApp.get.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      );

      const getHandler = getCall[1];
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
      };
      const result = getHandler(
        {headers: {authorization: 'Bearer test-token'}},
        mockRes
      );
      expect(result).toBeUndefined();
      expect(mockRes.status).not.toHaveBeenCalledWith(401);
    });

    test('should reject unauthorized GET requests with 401', async () => {
      new CommercetoolsCommerceAgentStreamable({
        authConfig: mockAuthConfig,
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

      const getCall = mockApp.get.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      );

      const getHandler = getCall[1];
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
      };
      await getHandler({headers: {}}, mockRes);
      expect(mockRes.status).toHaveBeenCalledWith(401);
    });
  });

  describe('Authorization token handling', () => {
    let instance: CommercetoolsCommerceAgentStreamable;
    let postHandler: (req: any, res: any) => void;

    beforeEach(() => {
      instance = new CommercetoolsCommerceAgentStreamable({
        authConfig: {...mockAuthConfig, accessToken: 'original-token'},
        configuration: mockConfiguration,
        server: mockServer,
      } as any);

      const postCall = mockApp.post.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      );
      postHandler = postCall[1];
    });

    test('should accept request with authorization header token', async () => {
      const mockReq = {
        headers: {authorization: 'Bearer header-token'},
        body: {},
      };
      const mockRes = {
        on: jest.fn(),
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
        headersSent: false,
      };

      await postHandler(mockReq, mockRes);
      expect(mockServer).toHaveBeenCalled();
      expect(mockRes.status).not.toHaveBeenCalledWith(401);
    });

    test('should NOT fall back to config token when no header (401)', async () => {
      const mockReq = {
        headers: {},
        body: {},
      };
      const mockRes = {
        on: jest.fn(),
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
        headersSent: false,
      };

      await postHandler(mockReq, mockRes);
      expect(mockRes.status).toHaveBeenCalledWith(401);
      expect(mockServer).not.toHaveBeenCalled();
    });

    test('should forward the header token (type auth_token) to the bootstrapped server', async () => {
      // Reset so the post handler we look up belongs to the instance below,
      // not the one constructed in beforeEach (shared mockApp accumulates).
      jest.clearAllMocks();
      // No injected `server` factory, so the bootstrapped path is used and
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

      const postCall = mockApp.post.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      );
      const handler = postCall[1];

      const mockReq = {
        headers: {authorization: 'Bearer caller-token'},
        body: {},
      };
      const mockRes = {
        on: jest.fn(),
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
        headersSent: false,
      };

      await handler(mockReq, mockRes);

      expect(CommercetoolsCommerceAgent.create).toHaveBeenCalledWith(
        expect.objectContaining({
          authConfig: expect.objectContaining({
            type: 'auth_token',
            accessToken: 'caller-token',
          }),
        })
      );
    });

    test('should allow header-less requests when enforceAuthHeader is false', async () => {
      // Reset so the post handler we look up belongs to the instance below.
      jest.clearAllMocks();
      new CommercetoolsCommerceAgentStreamable({
        authConfig: {...mockAuthConfig, accessToken: 'original-token'},
        configuration: mockConfiguration,
        server: mockServer,
        enforceAuthHeader: false,
      } as any);

      const postCall = mockApp.post.mock.calls.find(
        (call: any) => call[0] === '/mcp'
      );
      const handler = postCall[1];

      const mockReq = {
        headers: {},
        body: {},
      };
      const mockRes = {
        on: jest.fn(),
        status: jest.fn().mockReturnThis(),
        json: jest.fn().mockReturnThis(),
        headersSent: false,
      };

      await handler(mockReq, mockRes);
      expect(mockServer).toHaveBeenCalled();
      expect(mockRes.status).not.toHaveBeenCalledWith(401);
    });
  });
});
