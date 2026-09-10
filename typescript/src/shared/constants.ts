export const DYNAMIC_TOOL_LOADING_THRESHOLD = 30;

/**
 * Bind to loopback unless told otherwise. A server listening on every
 * interface is reachable by anything on the same network, which is rarely
 * what someone starting a local MCP server intends.
 */
export const DEFAULT_HOST = '127.0.0.1';

/**
 * Hostnames a loopback-bound server legitimately answers for. Anything else
 * in the `Host` header means the request was addressed somewhere else and
 * only reached us through DNS rebinding or a proxy we were not told about.
 */
export const LOOPBACK_HOSTNAMES = ['localhost', '127.0.0.1', '[::1]'];

/** The address that means "every IPv4 interface" to the OS. */
export const ALL_INTERFACES_HOST = '0.0.0.0';

/**
 * `*` and an empty value are the shorthands people reach for when they mean
 * "listen everywhere", but Node hands the value to `dns.lookup()`, so a
 * literal `*` fails to resolve and the bind never happens. Translate those
 * into the address the OS actually understands.
 */
export function normalizeBindHost(host?: string): string {
  const trimmed = (host ?? '').trim();
  if (trimmed === '' || trimmed === '*') return ALL_INTERFACES_HOST;
  return trimmed;
}
