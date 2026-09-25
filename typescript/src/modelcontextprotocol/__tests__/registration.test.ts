import CommercetoolsCommerceAgent from '../agent';
import {SERVER_VERSION} from '../../shared/version';

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
