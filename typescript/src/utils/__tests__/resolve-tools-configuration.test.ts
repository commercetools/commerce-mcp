import {ACCEPTED_TOOLS} from '../accepted-tools';
import {
  applyResolvedToolsToConfiguration,
  resolveToolsForConfiguration,
} from '../resolve-tools-configuration';
import type {Configuration} from '../../types/configuration';

describe('resolveToolsForConfiguration', () => {
  it('lone all without isAdmin is empty explicit', () => {
    expect(resolveToolsForConfiguration(['all'], false)).toEqual({
      mode: 'explicit',
      explicitTools: [],
    });
  });

  it('read_all without isAdmin is read_all', () => {
    expect(resolveToolsForConfiguration(['read_all'], false)).toEqual({
      mode: 'read_all',
      explicitTools: [],
    });
  });

  it('all,read_all without isAdmin is read_all', () => {
    expect(resolveToolsForConfiguration(['all', 'read_all'], false)).toEqual({
      mode: 'read_all',
      explicitTools: [],
    });
  });

  it('explicit underscore method names pass through', () => {
    expect(
      resolveToolsForConfiguration(['read_products', 'create_products'], false)
    ).toEqual({
      mode: 'explicit',
      explicitTools: ['read_products', 'create_products'],
    });
  });
});

describe('applyResolvedToolsToConfiguration', () => {
  it('all_expand fills actions from accepted tool list', () => {
    const configuration: Configuration = {actions: {}, context: {}};
    applyResolvedToolsToConfiguration(
      configuration,
      {mode: 'all_expand', explicitTools: []},
      ACCEPTED_TOOLS
    );
    expect(configuration.actions?.products?.read).toBe(true);
    expect(configuration.actions?.products?.create).toBe(true);
  });

  it('read_all fills only read actions', () => {
    const configuration: Configuration = {actions: {}, context: {}};
    applyResolvedToolsToConfiguration(
      configuration,
      {mode: 'read_all', explicitTools: []},
      ACCEPTED_TOOLS
    );
    expect(configuration.actions?.products?.read).toBe(true);
    expect(configuration.actions?.products?.create).toBeUndefined();
  });

  it('maps underscore method names to namespace/action actions', () => {
    const configuration: Configuration = {actions: {}, context: {}};
    applyResolvedToolsToConfiguration(configuration, {
      mode: 'explicit',
      explicitTools: ['read_customers', 'update_carts'],
    });
    expect(configuration.actions?.customer?.read).toBe(true);
    expect(configuration.actions?.cart?.update).toBe(true);
  });

  it('honors custom acceptedTools array', () => {
    const configuration: Configuration = {actions: {}, context: {}};
    applyResolvedToolsToConfiguration(
      configuration,
      {mode: 'explicit', explicitTools: ['read_products']},
      ['read_products', 'create_products']
    );
    expect(configuration.actions?.products?.read).toBe(true);
    expect(configuration.actions?.products?.create).toBeUndefined();
  });
});
