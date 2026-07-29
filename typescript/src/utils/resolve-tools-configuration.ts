import type {Configuration} from '../types/configuration';
import type {AvailableNamespaces} from '../types/tools';
import {ACCEPTED_TOOLS} from './accepted-tools';
import {resolveMethodToAction} from '../shared/core-bridge';

export type ToolResolutionMode = 'explicit' | 'read_all' | 'all_expand';

export type ToolsConfigurationResolution = {
  mode: ToolResolutionMode;
  explicitTools: string[];
};

/**
 * Resolves CLI `--tools` into a mode and explicit tool ids for building
 * {@link Configuration.actions}.
 *
 * Tool ids are underscore-based method names (e.g. `read_customers`,
 * `create_cart_discounts`). The legacy dot-notation `namespace.action` form is
 * no longer supported.
 *
 * - `read_all` → always expands to every accepted read tool (never requires
 *   `isAdmin`).
 * - `all` → expands to every accepted tool only when `isAdmin` is true; if
 *   `all` is the only token and `isAdmin` is false, actions stay empty.
 * - If both `all` and other tokens appear without admin, only the non-`all`
 *   tokens apply (`all` is ignored). Same when mixing explicit tools with
 *   `read_all`: only the explicit tools apply.
 * - If only `all` and `read_all` appear (no explicit tools) and `isAdmin` is
 *   false, `read_all` still applies → full read expansion (`read_all`).
 */
export function resolveToolsForConfiguration(
  selectedTools: string[],
  isAdmin: boolean
): ToolsConfigurationResolution {
  const normalized = selectedTools
    .map((tool) => tool.trim())
    .filter((tool) => tool.length > 0);

  const hasAll = normalized.includes('all');
  const hasAllRead = normalized.includes('read_all');

  const explicitNamed = normalized.filter(
    (tool) => tool !== 'all' && tool !== 'read_all'
  );

  if (explicitNamed.length > 0) {
    return {mode: 'explicit', explicitTools: explicitNamed};
  }

  if (normalized.length === 0) {
    return {mode: 'explicit', explicitTools: []};
  }

  if (hasAll && hasAllRead) {
    if (isAdmin) {
      return {mode: 'all_expand', explicitTools: []};
    }

    return {mode: 'read_all', explicitTools: []};
  }

  if (hasAll) {
    if (!isAdmin) {
      return {mode: 'explicit', explicitTools: []};
    }

    return {mode: 'all_expand', explicitTools: []};
  }

  if (hasAllRead) {
    return {mode: 'read_all', explicitTools: []};
  }

  return {mode: 'explicit', explicitTools: normalized};
}

export function applyResolvedToolsToConfiguration(
  configuration: Configuration,
  resolution: ToolsConfigurationResolution,
  acceptedTools: readonly string[] = ACCEPTED_TOOLS
): void {
  configuration.actions = {};
  const {mode, explicitTools} = resolution;

  const setAction = (method: string): void => {
    const resolved = resolveMethodToAction(method);
    if (!resolved) return;
    const {namespace, action} = resolved;
    configuration.actions![namespace as AvailableNamespaces] = {
      ...configuration.actions![namespace as AvailableNamespaces],
      [action]: true,
    };
  };

  if (mode === 'all_expand') {
    acceptedTools.forEach(setAction);
    return;
  }

  if (mode === 'read_all') {
    acceptedTools.forEach((method) => {
      if (resolveMethodToAction(method)?.action === 'read') {
        setAction(method);
      }
    });
    return;
  }

  explicitTools.forEach(setAction);
}
