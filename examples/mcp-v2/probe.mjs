/**
 * Smoke check for the example: one endpoint, two protocol eras.
 *
 * Drives the MCP handler directly with web-standard `Request` objects — no
 * HTTP client, no socket. The two guarantees that live in Express middleware
 * rather than in the handler (bearer auth, DNS-rebinding `Host` validation)
 * are listed as manual checks in README.md.
 */
import {buildHandler} from './server.mjs';

const MODERN = '2026-07-28';
const TOKEN = 'example-token';
const ENDPOINT = new URL('/mcp', 'http://mcp.localhost');

const META = {
  'io.modelcontextprotocol/protocolVersion': MODERN,
  'io.modelcontextprotocol/clientCapabilities': {},
  'io.modelcontextprotocol/clientInfo': {name: 'mcp-v2-example-probe', version: '1.0.0'},
};

const handler = buildHandler();

/** Posts a JSON-RPC body with the headers the modern era requires. */
async function rpc(body, {token = TOKEN, method = body.method} = {}) {
  const headers = new Headers({
    accept: 'application/json, text/event-stream',
    'content-type': 'application/json',
  });
  if (token) headers.set('authorization', `Bearer ${token}`);
  // SEP-2243: modern POSTs must name their method in the headers too.
  if (method) headers.set('mcp-method', method);
  if (body.params?.name) headers.set('mcp-name', body.params.name);

  const response = await handler.fetch(
    new Request(ENDPOINT, {method: 'POST', headers, body: JSON.stringify(body)}),
    {authInfo: token ? {token, clientId: 'example', scopes: []} : undefined}
  );

  const text = await response.text();
  let payload = text;
  try {
    payload = JSON.parse(text);
  } catch {
    const frames = text
      .split('\n')
      .filter((line) => line.startsWith('data:'))
      .map((line) => line.slice(5).trim());
    try {
      payload = JSON.parse(frames.at(-1));
    } catch {
      payload = text;
    }
  }

  return {status: response.status, payload};
}

const modern = (method, params = {}) =>
  rpc({jsonrpc: '2.0', id: Date.now(), method, params: {...params, _meta: META}});

const checks = [];
const check = (name, ok, detail) => checks.push({name, ok: Boolean(ok), detail});

// --- modern era (2026-07-28)
const discover = await modern('server/discover');
check(
  'modern: server/discover advertises 2026-07-28',
  discover.payload?.result?.supportedVersions?.includes(MODERN),
  JSON.stringify(discover.payload?.result?.supportedVersions)
);

const list = await modern('tools/list');
const tool = list.payload?.result?.tools?.find((t) => t.name === 'read_carts');
check(
  'modern: tools/list carries title + JSON Schema + annotations',
  tool?.title && tool?.inputSchema?.type === 'object' && tool?.annotations?.readOnlyHint,
  tool && `${tool.name} title=${tool.title} readOnly=${tool.annotations?.readOnlyHint}`
);
check(
  'modern: tools/list is a CacheableResult (SEP-2549)',
  list.payload?.result?.ttlMs === 60_000 && list.payload?.result?.cacheScope === 'public',
  `ttlMs=${list.payload?.result?.ttlMs} cacheScope=${list.payload?.result?.cacheScope}`
);
check(
  'modern: results carry resultType (SEP-2322)',
  list.payload?.result?.resultType === 'complete',
  list.payload?.result?.resultType
);

const call = await modern('tools/call', {name: 'read_carts', arguments: {limit: 3}});
check(
  'modern: tools/call returns structuredContent',
  call.payload?.result?.structuredContent?.limit === 3,
  JSON.stringify(call.payload?.result?.structuredContent)
);
check(
  'modern: per-request auth reached the tool',
  JSON.parse(call.payload?.result?.content?.[0]?.text ?? '{}').tokenSeen === true
);

const badVersion = await rpc({
  jsonrpc: '2.0',
  id: 9,
  method: 'tools/list',
  params: {_meta: {...META, 'io.modelcontextprotocol/protocolVersion': '1999-01-01'}},
});
check(
  'modern: unknown version -> -32022 UnsupportedProtocolVersion',
  badVersion.payload?.error?.code === -32022,
  badVersion.payload?.error?.message
);

const noHeader = await rpc(
  {jsonrpc: '2.0', id: 10, method: 'tools/list', params: {_meta: META}},
  {method: ''}
);
check(
  'modern: missing Mcp-Method -> -32020 HeaderMismatch',
  noHeader.payload?.error?.code === -32020,
  noHeader.payload?.error?.message
);

// --- legacy era (<= 2025-11-25): existing clients must keep working
const init = await rpc({
  jsonrpc: '2.0',
  id: 20,
  method: 'initialize',
  params: {
    protocolVersion: '2025-06-18',
    capabilities: {},
    clientInfo: {name: 'legacy', version: '1'},
  },
});
check(
  'legacy: initialize still negotiates',
  init.payload?.result?.protocolVersion === LEGACY,
  init.payload?.result?.protocolVersion
);

const legacyCall = await rpc({
  jsonrpc: '2.0',
  id: 21,
  method: 'tools/call',
  params: {name: 'read_project', arguments: {}},
});
check(
  'legacy: tools/call works without any _meta envelope',
  legacyCall.payload?.result?.structuredContent?.key === 'example-project',
  JSON.stringify(legacyCall.payload?.result?.structuredContent)
);

// The handler answers non-POST with 405 — the 2026-07-28 removal of the GET
// endpoint.
const getRes = await handler.fetch(new Request(ENDPOINT, {method: 'GET'}));
check(
  'GET /mcp -> 405 (endpoint removed in 2026-07-28)',
  getRes.status === 405,
  `HTTP ${getRes.status}`
);

const width = Math.max(...checks.map((c) => c.name.length));
for (const {name, ok, detail} of checks) {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name.padEnd(width)}  ${detail ?? ''}`);
}
const failed = checks.filter((c) => !c.ok).length;
console.log(`\n${checks.length - failed}/${checks.length} checks passed`);
process.exit(failed === 0 ? 0 : 1);
