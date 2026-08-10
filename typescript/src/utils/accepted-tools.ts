import {listAllToolMethods} from '../shared/bridge';

/**
 * Canonical list of selectable tool method names for the MCP CLI `--tools`
 * argument and configuration resolution.
 *
 * Names are underscore-based method ids (e.g. `read_customers`,
 * `create_cart_discounts`) — the dot-notation `namespace.action` form is no
 * longer supported. The list is derived from the tool registry so it stays in
 * sync with the tools actually exposed.
 */
export const ACCEPTED_TOOLS: readonly string[] = listAllToolMethods();
