import {z} from 'zod';
import {toJsonSchema, toolInputJsonSchema} from '../json-schema';
import {contextToTools} from '../tools';
import {contextToBulkTools} from '../bulk/tools';
import type {Tool} from '../../types/tools';

/** Every tool the server can expose, admin context so nothing is filtered out. */
const allTools = (): Tool[] => [
  ...contextToTools({isAdmin: true}),
  ...contextToBulkTools({isAdmin: true}),
];

describe('toJsonSchema', () => {
  it('converts fields, descriptions and required keys', () => {
    const schema = toJsonSchema(
      z.object({
        limit: z.number().optional().describe('page size'),
        where: z.string(),
      })
    );

    expect(schema).toEqual({
      type: 'object',
      properties: {
        limit: {type: 'number', description: 'page size'},
        where: {type: 'string'},
      },
      required: ['where'],
    });
  });

  it('omits $schema so the protocol default dialect applies', () => {
    expect(toJsonSchema(z.object({a: z.string()}))).not.toHaveProperty(
      '$schema'
    );
  });

  it('leaves additionalProperties unset, keeping stray arguments non-fatal', () => {
    // zod strips unknown keys; rendering that as `additionalProperties: false`
    // would start rejecting calls that succeed today.
    expect(toJsonSchema(z.object({a: z.string()}))).not.toHaveProperty(
      'additionalProperties'
    );
  });

  it('inlines nested schemas rather than emitting $ref', () => {
    const inner = z.object({id: z.string()});
    const schema = toJsonSchema(z.object({a: inner, b: inner}));

    expect(JSON.stringify(schema)).not.toContain('$ref');
    expect(JSON.stringify(schema)).not.toContain('$defs');
  });
});

describe('toolInputJsonSchema', () => {
  it('rejects a tool whose parameters are not an object schema', () => {
    const broken = {
      method: 'broken_tool',
      parameters: z.string() as never,
    } as unknown as Tool;

    expect(() => toolInputJsonSchema(broken)).toThrow(
      'Tool "broken_tool" must declare object parameters, got string'
    );
  });

  describe('every registered tool', () => {
    const tools = allTools();

    it('covers the whole tool surface', () => {
      expect(tools.length).toBeGreaterThanOrEqual(100);
    });

    it.each(tools.map((tool) => [tool.method, tool] as const))(
      '%s converts to a valid object schema',
      (_method, tool) => {
        const schema = toolInputJsonSchema(tool);

        expect(schema.type).toBe('object');
        expect(schema).not.toHaveProperty('$schema');
        expect(JSON.stringify(schema)).not.toContain('$ref');
        for (const key of schema.required ?? []) {
          expect(Object.keys(schema.properties ?? {})).toContain(key);
        }
      }
    );
  });
});
