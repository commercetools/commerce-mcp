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

/** Every `$ref` string anywhere in a schema. */
const refsIn = (schema: unknown): string[] => {
  const found: string[] = [];
  const walk = (node: unknown) => {
    if (Array.isArray(node)) return node.forEach(walk);
    if (node === null || typeof node !== 'object') return;
    for (const [key, value] of Object.entries(
      node as Record<string, unknown>
    )) {
      if (key === '$ref' && typeof value === 'string') found.push(value);
      walk(value);
    }
  };
  walk(schema);
  return found;
};

/** Resolves a local JSON pointer, or undefined if it dangles. */
const resolvePointer = (schema: unknown, ref: string): unknown => {
  if (ref === '#') return schema;
  let node: unknown = schema;
  for (const raw of ref.replace(/^#\//, '').split('/')) {
    const key = raw.replace(/~1/g, '/').replace(/~0/g, '~');
    if (node === null || typeof node !== 'object') return undefined;
    node = (node as Record<string, unknown>)[key];
    if (node === undefined) return undefined;
  }
  return node;
};

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

  it('drops additionalProperties on nested schemas too', () => {
    // Nested objects are inlined, so each arrives with its own copy; stripping
    // only the root would still reject a stray key inside an argument.
    const schema = toJsonSchema(
      z.object({
        outer: z.object({inner: z.object({id: z.string()})}),
        items: z.array(z.object({sku: z.string()})),
        choice: z.union([z.object({a: z.string()}), z.object({b: z.number()})]),
      })
    );

    expect(JSON.stringify(schema)).not.toContain(
      '"additionalProperties":false'
    );
  });

  it('keeps a schema-valued additionalProperties', () => {
    // On a record this describes the value type rather than forbidding keys,
    // so it must survive the strip.
    expect(toJsonSchema(z.object({attrs: z.record(z.string())}))).toEqual({
      type: 'object',
      properties: {
        attrs: {type: 'object', additionalProperties: {type: 'string'}},
      },
      required: ['attrs'],
    });
  });

  it('points a repeated subschema at its first occurrence', () => {
    const inner = z.object({id: z.string()});
    const schema = toJsonSchema(z.object({a: inner, b: inner}));

    // Deduplicated rather than inlined twice. Refs stay inside the schema,
    // so there is no `$defs` section for a client to look up separately.
    expect(schema).toMatchObject({
      properties: {b: {$ref: '#/properties/a'}},
    });
    expect(schema).not.toHaveProperty('$defs');
    expect(resolvePointer(schema, '#/properties/a')).toMatchObject({
      type: 'object',
    });
  });

  it('describes a recursive schema instead of dropping it', () => {
    // Recursion cannot be inlined. With `$refStrategy: 'none'` the generator
    // logged "Recursive reference detected ... Defaulting to any" and emitted
    // an empty schema, so the recursive branch carried no information at all.
    type Node = {value: string; children?: Node[]};
    const node: z.ZodType<Node> = z.lazy(() =>
      z.object({value: z.string(), children: z.array(node).optional()})
    );
    const schema = toJsonSchema(z.object({root: node}));

    const children = (
      (
        schema.properties as Record<
          string,
          {properties?: Record<string, {items?: unknown}>}
        >
      ).root.properties ?? {}
    ).children as {items?: {$ref?: string}};

    expect(children.items?.$ref).toBeTruthy();
    expect(resolvePointer(schema, children.items!.$ref!)).toBeDefined();
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

    it('generates every schema without discarding a recursive branch', () => {
      // The generator reports this on stdout rather than throwing, so the
      // only way to notice was reading the server log:
      //   "Recursive reference detected at ...! Defaulting to any"
      // It meant that branch shipped as `{}` — no schema at all.
      const noticed: string[] = [];
      const record = (...args: unknown[]) => {
        const first = String(args[0] ?? '');
        if (first.includes('Recursive reference')) noticed.push(first);
      };
      const {warn, log} = console;
      console.warn = record as typeof console.warn;
      console.log = record as typeof console.log;
      try {
        for (const tool of tools) toolInputJsonSchema(tool);
      } finally {
        console.warn = warn;
        console.log = log;
      }

      expect(noticed).toEqual([]);
    });

    it.each(tools.map((tool) => [tool.method, tool] as const))(
      '%s converts to a valid object schema',
      (_method, tool) => {
        const schema = toolInputJsonSchema(tool);

        expect(schema.type).toBe('object');
        expect(schema).not.toHaveProperty('$schema');
        expect(JSON.stringify(schema)).not.toContain(
          '"additionalProperties":false'
        );

        // Refs are allowed, but every one must be a local pointer that
        // actually resolves — a dangling ref is worse than an inlined copy.
        for (const ref of refsIn(schema)) {
          expect(ref.startsWith('#')).toBe(true);
          expect(resolvePointer(schema, ref)).toBeDefined();
        }
        for (const key of schema.required ?? []) {
          expect(Object.keys(schema.properties ?? {})).toContain(key);
        }
      }
    );
  });
});
