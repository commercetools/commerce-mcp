import {z} from 'zod';
import CommercetoolsCommerceAgent from '../agent';
import {SERVER_VERSION} from '../../shared/version';
import {SUPPORTED_PROTOCOL_VERSIONS} from '@modelcontextprotocol/server';

jest.mock('../../shared/api');

const build = () =>
  (
    CommercetoolsCommerceAgent as unknown as {
      create: (o: unknown) => Promise<unknown>;
    }
  ).create({
    authConfig: {
      type: 'auth_token',
      accessToken: 't',
      projectKey: 'p',
      authUrl: 'https://auth.example',
      apiUrl: 'https://api.example',
    },
    configuration: {
      actions: {cart: {read: true, create: true, update: true}},
      context: {},
    },
  });

type Registered = {
  title?: string;
  annotations?: Record<string, unknown>;
};

const registered = (agent: unknown) =>
  (agent as {_registeredTools: Record<string, Registered>})._registeredTools;

describe('server identity (DEVX-885)', () => {
  it('reports the real package version, not the old hardcoded 0.4.0', async () => {
    const agent = await build();
    const info = (agent as {server: {_serverInfo: Record<string, unknown>}})
      .server._serverInfo;

    expect(info.version).toBe(SERVER_VERSION);
    expect(info.version).not.toBe('0.4.0');
    expect(info.description).toBeTruthy();
  });

  it('ships usage instructions', async () => {
    const agent = await build();
    expect(
      (agent as {server: {_instructions?: string}}).server._instructions
    ).toBeTruthy();
  });
});

describe('protocol versions', () => {
  it('keeps every 2025-era revision the SDK supports, plus the 2026 one', async () => {
    // Advertising only the newest legacy revision looks equivalent but is
    // not: the handshake then counter-offers `2025-11-25` to a client that
    // asked for an older one, and a client that does not recognise that
    // version disconnects rather than downgrading. `mcp-remote` did exactly
    // that — "Server's protocol version is not supported: 2025-11-25".
    const agent = await build();
    const advertised = (
      agent as {server: {_supportedProtocolVersions: string[]}}
    ).server._supportedProtocolVersions;

    expect(advertised).toContain('2026-07-28');
    for (const legacy of SUPPORTED_PROTOCOL_VERSIONS) {
      expect(advertised).toContain(legacy);
    }
  });
});

describe('unknown-verb fallback', () => {
  const buildWithThreshold = () =>
    (
      CommercetoolsCommerceAgent as unknown as {
        create: (o: unknown) => Promise<unknown>;
      }
    ).create({
      authConfig: {
        type: 'auth_token',
        accessToken: 't',
        projectKey: 'p',
        authUrl: 'https://auth.example',
        apiUrl: 'https://api.example',
      },
      // Force the resource-based system on, so the meta-tools register.
      configuration: {
        actions: {cart: {read: true, create: true, update: true}},
        context: {dynamicToolLoadingThreshold: 1},
      },
    });

  it('stays quiet about the meta-tools it registers itself', async () => {
    // They are never in the catalogue, so the conservative fallback is
    // expected for them; saying so on every start is noise.
    const {error} = console;
    const lines: string[] = [];
    console.error = ((...a: unknown[]) => {
      lines.push(String(a[0]));
    }) as typeof console.error;
    try {
      await buildWithThreshold();
    } finally {
      console.error = error;
    }

    expect(lines.filter((l) => l.includes('no known verb'))).toEqual([]);
  });

  it('still warns for a tool it did not register', async () => {
    const {error} = console;
    const lines: string[] = [];
    console.error = ((...a: unknown[]) => {
      lines.push(String(a[0]));
    }) as typeof console.error;
    try {
      await (
        CommercetoolsCommerceAgent as unknown as {
          create: (o: unknown) => Promise<unknown>;
        }
      ).create({
        authConfig: {
          type: 'auth_token',
          accessToken: 't',
          projectKey: 'p',
          authUrl: 'https://auth.example',
          apiUrl: 'https://api.example',
        },
        configuration: {
          actions: {cart: {read: true}},
          context: {},
          customTools: [
            {
              name: 'Custom Thing',
              method: 'custom_thing',
              description: 'a tool we did not ship',
              parameters: z.object({k: z.string()}),
              execute: jest.fn(),
            },
          ],
        },
      });
    } finally {
      console.error = error;
    }

    expect(
      lines.filter((l) => l.includes('no known verb for "custom_thing"'))
    ).toHaveLength(1);
  });
});

describe('tool annotations (DEVX-885)', () => {
  it('gives every tool a title', async () => {
    const tools = registered(await build());
    const names = Object.keys(tools);

    expect(names.length).toBeGreaterThan(0);
    for (const name of names) {
      expect(tools[name].title).toBeTruthy();
    }
  });

  it.each([
    ['read_carts', {readOnlyHint: true, destructiveHint: false}],
    ['create_carts', {readOnlyHint: false, destructiveHint: false}],
    // `update` overwrites existing resource state, so it is the destructive verb.
    ['update_carts', {readOnlyHint: false, destructiveHint: true}],
  ])('derives %s annotations from its verb', async (name, expected) => {
    const tools = registered(await build());
    expect(tools[name].annotations).toMatchObject(expected);
  });

  it('marks tools open-world, since they reach a live remote project', async () => {
    // The catalogue reports false; we override it deliberately.
    const tools = registered(await build());
    expect(tools.read_carts.annotations).toMatchObject({openWorldHint: true});
  });

  it('titles a tool the way the catalogue does', async () => {
    const tools = registered(await build());
    expect(tools.read_carts.title).toBe('Read Carts');
    // MCP carries the title twice; both come from the same value.
    expect(tools.read_carts.annotations).toMatchObject({title: 'Read Carts'});
  });
});
