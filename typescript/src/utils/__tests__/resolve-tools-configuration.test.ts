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

  it('all.read without isAdmin is all_read', () => {
    expect(resolveToolsForConfiguration(['all.read'], false)).toEqual({
      mode: 'all_read',
      explicitTools: [],
    });
  });

  it('all,all.read without isAdmin is all_read', () => {
    expect(resolveToolsForConfiguration(['all', 'all.read'], false)).toEqual({
      mode: 'all_read',
      explicitTools: [],
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

  it('honors custom acceptedTools array', () => {
    const configuration: Configuration = {actions: {}, context: {}};
    applyResolvedToolsToConfiguration(
      configuration,
      {mode: 'explicit', explicitTools: ['products.read']},
      ['products.read', 'products.create']
    );
    expect(configuration.actions?.products?.read).toBe(true);
    expect(configuration.actions?.products?.create).toBeUndefined();
  });
});
