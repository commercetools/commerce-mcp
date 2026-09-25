import {fromJsonSchema} from '@modelcontextprotocol/server';
import {z} from 'zod';
import {toJsonSchema, toolInputJsonSchema} from '../json-schema';
import {contextToTools} from '../tools';
import {contextToBulkTools} from '../bulk/tools';
import type {Tool} from '../../types/tools';

const allTools = (): Tool[] => [
  ...contextToTools({isAdmin: true}),
  ...contextToBulkTools({isAdmin: true}),
];

/** Every numeric bound in a schema, wherever it appears. */
const numericBounds = (schema: unknown): unknown[] => {
  const found: unknown[] = [];
  const walk = (node: unknown) => {
    if (Array.isArray(node)) return node.forEach(walk);
    if (node === null || typeof node !== 'object') return;
    for (const [key, value] of Object.entries(
      node as Record<string, unknown>
    )) {
      if (key === 'exclusiveMinimum' || key === 'exclusiveMaximum')
        found.push(value);
      walk(value);
    }
  };
  walk(schema);
  return found;
};

describe('JSON Schema dialect', () => {
  it('spells exclusive bounds as numbers, not draft-4 booleans', () => {
    // zod-to-json-schema's `jsonSchema2019-09` target emits
    // `{minimum: 0, exclusiveMinimum: true}` — the draft-4 form. Every
    // draft-6-or-later validator, including the one the MCP SDK uses,
    // rejects that with `exclusiveMinimum value must be ["number"]`.
    const schema = toJsonSchema(
      z.object({qty: z.number().positive(), big: z.number().gt(5)})
    );

    expect(schema).toMatchObject({
      properties: {
        qty: {exclusiveMinimum: 0},
        big: {exclusiveMinimum: 5},
      },
    });
    expect(JSON.stringify(schema)).not.toContain('"exclusiveMinimum":true');
  });

  describe('every registered tool', () => {
    const tools = allTools();

    it('covers the whole tool surface', () => {
      expect(tools.length).toBeGreaterThanOrEqual(100);
    });

    it.each(tools.map((tool) => [tool.method, tool] as const))(
      '%s is accepted by the MCP SDK validator',
      (_method, tool) => {
        // The failure this guards against only appears when a client
        // connects and the SDK compiles the schema, so assert it directly.
        const bridged = fromJsonSchema(toolInputJsonSchema(tool) as never);
        expect(() =>
          (
            bridged as unknown as {
              '~standard': {validate: (v: unknown) => unknown};
            }
          )['~standard'].validate({})
        ).not.toThrow();

        for (const bound of numericBounds(toolInputJsonSchema(tool))) {
          expect(typeof bound).toBe('number');
        }
      }
    );
  });
});
