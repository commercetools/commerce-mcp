/**
 * The version reported as the MCP server's identity.
 *
 * Kept as a constant rather than imported from `package.json`: the package is
 * built to both CommonJS and ESM, and a JSON import under `module: NodeNext`
 * needs an import attribute that only one of those two outputs accepts.
 *
 * `__tests__/version.test.ts` asserts this matches `package.json`, so the two
 * cannot drift the way the previous hardcoded `0.4.0` did.
 */
export const SERVER_VERSION = '4.1.0';
