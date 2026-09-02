export const DYNAMIC_TOOL_LOADING_THRESHOLD = 30;

/**
 * Bind to loopback unless told otherwise. A server listening on every
 * interface is reachable by anything on the same network, which is rarely
 * what someone starting a local MCP server intends.
 */
export const DEFAULT_HOST = '127.0.0.1';
