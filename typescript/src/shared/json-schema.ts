import type {ZodTypeAny} from 'zod';
import {zodToJsonSchema} from 'zod-to-json-schema';
import type {Tool} from '../types/tools';

/** A JSON Schema object suitable for an MCP tool's `inputSchema`. */
export type JsonSchemaObject = {
  type: 'object';
  properties?: Record<string, unknown>;
  required?: string[];
  [keyword: string]: unknown;
};

/**
 * Keywords whose values are arbitrary data rather than subschemas. Recursing
 * into them could strip an `additionalProperties` that belongs to a literal
 * value instead of being a constraint.
 */
const OPAQUE_KEYWORDS = new Set(['enum', 'const', 'default', 'examples']);

/**
 * Drops `additionalProperties: false` wherever it appears. `$refStrategy:
 * 'none'` inlines nested objects, so they arrive carrying their own copy and
 * the root alone is not enough.
 */
function allowUnknownKeys(node: unknown): unknown {
  if (Array.isArray(node)) return node.map(allowUnknownKeys);
  if (node === null || typeof node !== 'object') return node;

  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(node as Record<string, unknown>)) {
    if (key === 'additionalProperties' && value === false) continue;
    result[key] = OPAQUE_KEYWORDS.has(key) ? value : allowUnknownKeys(value);
  }
  return result;
}

/**
 * Converts a zod schema to JSON Schema for MCP tool registration.
 *
 * Our tool parameters come from `@commercetools/tools-core`, which is on
 * zod 3, while the MCP SDK wants a validator that can produce JSON Schema
 * (zod 4, ArkType, Valibot) or raw JSON Schema via `fromJsonSchema`. Going
 * through JSON Schema lets us stay on zod 3 and keeps the wire format the one
 * the protocol actually speaks.
 *
 * Two deliberate adjustments to the generator's output:
 *
 * - `$schema` is dropped. MCP declares JSON Schema 2020-12 as the default
 *   dialect, so declaring an older one on every tool would be wrong; omitting
 *   it lets the dialect be inherited.
 * - `additionalProperties: false` is dropped, at every level. zod object schemas
 *   *strip* unknown keys, but the generator renders that as
 *   `additionalProperties: false`, which turns a stray argument from something
 *   ignored into a validation failure. Models pass stray arguments; keep
 *   today's lenient behaviour. A schema-valued `additionalProperties` is kept:
 *   on a `z.record` it describes the value type rather than forbidding keys.
 */
export function toJsonSchema(schema: ZodTypeAny): Record<string, unknown> {
  const converted = zodToJsonSchema(schema, {
    // MCP's default dialect is 2020-12. The generator has no 2020-12 target,
    // and its `jsonSchema2019-09` one is the wrong choice despite the closer
    // name: for `.positive()` / `.gt()` it emits the draft-4 spelling
    // `{minimum: n, exclusiveMinimum: true}`, which every draft-6-or-later
    // validator rejects with `exclusiveMinimum value must be ["number"]`.
    // `jsonSchema7` emits the numeric `{exclusiveMinimum: n}` that 2020-12
    // also expects, and matches 2020-12 on every other keyword our tools use.
    target: 'jsonSchema7',
    // Inline everything: no `$defs`, so clients never have to resolve `$ref`.
    $refStrategy: 'none',
  }) as Record<string, unknown>;

  const {$schema: _schema, ...rest} = converted;

  return allowUnknownKeys(rest) as Record<string, unknown>;
}

/**
 * The JSON Schema for a tool's arguments. Throws rather than emitting
 * something the protocol would reject, so a bad schema fails the build instead
 * of a client's `tools/list`.
 */
export function toolInputJsonSchema(tool: Tool): JsonSchemaObject {
  const converted = toJsonSchema(tool.parameters);

  if (converted.type !== 'object') {
    throw new Error(
      `Tool "${tool.method}" must declare object parameters, got ${String(converted.type)}`
    );
  }

  const schema = converted as JsonSchemaObject;
  const missing = (schema.required ?? []).filter(
    (key) => !Object.prototype.hasOwnProperty.call(schema.properties ?? {}, key)
  );
  if (missing.length > 0) {
    throw new Error(
      `Tool "${tool.method}" requires properties it does not declare: ${missing.join(', ')}`
    );
  }

  return schema;
}
