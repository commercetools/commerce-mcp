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
 * - `additionalProperties` is dropped. zod object schemas *strip* unknown keys,
 *   but the generator renders that as `additionalProperties: false`, which
 *   turns a stray argument from something ignored into a validation failure.
 *   Models pass stray arguments; keep today's lenient behaviour.
 */
export function toJsonSchema(schema: ZodTypeAny): Record<string, unknown> {
  const converted = zodToJsonSchema(schema, {
    // 2020-12 is MCP's default dialect and the closest target the generator
    // offers; with `$schema` stripped the difference is not observable for
    // the shapes our tools use.
    target: 'jsonSchema2019-09',
    // Inline everything: no `$defs`, so clients never have to resolve `$ref`.
    $refStrategy: 'none',
  }) as Record<string, unknown>;

  const {
    $schema: _schema,
    additionalProperties: _additional,
    ...rest
  } = converted;

  return rest;
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
