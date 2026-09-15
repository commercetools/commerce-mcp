/**
 * SDK v2 (2026-07-28) serving both protocol eras from one `/mcp` endpoint,
 * wired the way commerce-mcp is wired today: an Express app we own, a
 * per-request server instance carrying the caller's credentials, and a
 * mandatory bearer token.
 *
 * Tools are registered from JSON Schema via `fromJsonSchema`, which is how we
 * intend to feed our zod-3 schemas (DEVX-883) without a zod 4 upgrade.
 */
import {createMcpExpressApp} from '@modelcontextprotocol/express';
import {toNodeHandler} from '@modelcontextprotocol/node';
import {createMcpHandler, McpServer, fromJsonSchema} from '@modelcontextprotocol/server';

const MODERN = '2026-07-28';
const LEGACY = '2025-11-25';

/** Bound the request body rather than accepting whatever is posted. */
const JSON_BODY_LIMIT = '1mb';

/** Stand-ins for two real commercetools tools, shaped like ours. */
const TOOLS = [
  {
    method: 'read_carts',
    title: 'Read carts',
    description: 'Query carts in the project',
    input: {
      type: 'object',
      properties: {
        limit: {type: 'number', description: 'page size'},
        offset: {type: 'number'},
        where: {type: 'string', description: 'query predicate'},
      },
    },
    output: {
      type: 'object',
      properties: {
        results: {type: 'array', items: {type: 'object'}},
        total: {type: 'number'},
        limit: {type: 'number'},
        offset: {type: 'number'},
      },
      required: ['results', 'total'],
    },
    readOnly: true,
    run: ({limit = 20, offset = 0}) => ({results: [], total: 0, limit, offset}),
  },
  {
    method: 'read_project',
    title: 'Read project',
    description: 'Read the project settings',
    input: {type: 'object', properties: {}},
    output: {
      type: 'object',
      properties: {key: {type: 'string'}, name: {type: 'string'}},
      required: ['key'],
    },
    readOnly: true,
    run: () => ({key: 'example-project', name: 'Example'}),
  },
];

/** One server per request, built from that request's credentials. */
function buildServer(accessToken) {
  const server = new McpServer(
    {
      name: 'Commercetools',
      version: '4.1.0',
      description: 'An MCP server that provides access to commercetools APIs',
    },
    {
      // Opt in to the modern era; without this the SDK serves 2025 only.
      supportedProtocolVersions: [MODERN, LEGACY],
      instructions: 'Query and manage commercetools projects.',
      cacheHints: {'tools/list': {ttlMs: 60_000, cacheScope: 'public'}},
    }
  );

  for (const tool of TOOLS) {
    server.registerTool(
      tool.method,
      {
        title: tool.title,
        description: tool.description,
        inputSchema: fromJsonSchema(tool.input),
        outputSchema: fromJsonSchema(tool.output),
        annotations: {readOnlyHint: tool.readOnly},
      },
      async (args) => {
        const result = tool.run(args ?? {});
        return {
          // `accessToken` is what the real handler forwards to the API.
          content: [{type: 'text', text: JSON.stringify({...result, tokenSeen: Boolean(accessToken)})}],
          structuredContent: result,
        };
      }
    );
  }

  return server;
}

const bearer = (req) => {
  const [scheme, ...rest] = (req.headers.authorization ?? '').trim().split(/\s+/);
  if (scheme?.toLowerCase() !== 'bearer') return undefined;
  const token = rest.join(' ').trim();
  return token.length > 0 ? token : undefined;
};

/**
 * The MCP handler on its own, for driving protocol-level assertions without
 * an HTTP client. `buildApp` mounts this behind Express.
 */
export function buildHandler() {
  return createMcpHandler((ctx) => buildServer(ctx.authInfo?.token), {
    legacy: 'stateless',
    responseMode: 'auto',
    onerror: (e) => console.error('[mcp]', e.message),
  });
}

export function buildApp({host = '127.0.0.1', allowedHosts} = {}) {
  // Applies DNS-rebinding protection for loopback hosts on our behalf.
  const app = createMcpExpressApp({
    host,
    jsonLimit: JSON_BODY_LIMIT,
    ...(allowedHosts && {allowedHosts}),
  });

  const handler = buildHandler();

  /**
   * The SDK's own Node adapter converts the request, calls the handler and
   * writes the response — including SSE backpressure. Hand-rolling that
   * bridge means client input flows through our own `res.send`, which is both
   * more code and a reflected-XSS shape; `toNodeHandler` keeps the response
   * entirely inside the SDK.
   *
   * Registered for every method: it answers GET/DELETE with 405, which is the
   * correct 2026-07-28 behaviour. Routing only POST would 404 instead.
   */
  const mcp = toNodeHandler(handler, {
    onerror: (error) => console.error('[mcp:adapter]', error.message),
  });

  app.all('/mcp', (req, res) => {
    const token = bearer(req);
    if (!token) {
      return res.status(401).json({
        jsonrpc: '2.0',
        error: {
          code: -32001,
          message: 'Unauthorized: A valid Authorization Bearer token is required',
        },
        id: null,
      });
    }

    // `req.auth` is the adapter's documented hand-off to the handler's
    // pass-through `authInfo`; it never inspects headers or verifies tokens.
    req.auth = {token, clientId: 'example', scopes: []};

    return mcp(req, res, req.body);
  });

  return app;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const port = Number(process.env.PORT ?? 8899);
  const host = process.env.HOST ?? '127.0.0.1';
  buildApp({host}).listen(port, host, () => console.error(`example listening on ${host}:${port}`));
}
