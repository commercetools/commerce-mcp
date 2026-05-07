import type {Configuration} from '../types/configuration';
import type {AvailableNamespaces} from '../types/tools';
import {ACCEPTED_TOOLS} from './accepted-tools';

export type ToolResolutionMode = 'explicit' | 'all_read' | 'all_expand';

export type ToolsConfigurationResolution = {
  mode: ToolResolutionMode;
  explicitTools: string[];
};

/**
 * Resolves CLI `--tools` into a mode and explicit tool ids for building
 * {@link Configuration.actions}.
 *
 * - `all.read` → always expands to every accepted `*.read` action (never
 *   requires `isAdmin`).
 * - `all` → expands to every accepted tool only when `isAdmin` is true; if
 *   `all` is the only token and `isAdmin` is false, actions stay empty.
 * - If both `all` and other tokens appear without admin, only the non-`all`
 *   tokens apply (`all` is ignored). Same when mixing explicit tools with
 *   `all.read`: only the explicit tools apply.
 * - If only `all` and `all.read` appear (no explicit tools) and `isAdmin` is
 *   false, `all.read` still applies → full read expansion (`all_read`).
 */
export function resolveToolsForConfiguration(
  selectedTools: string[],
  isAdmin: boolean
): ToolsConfigurationResolution {
  const normalized = selectedTools
    .map((tool) => tool.trim())
    .filter((tool) => tool.length > 0);

  const hasAll = normalized.includes('all');
  const hasAllRead = normalized.includes('all.read');

  const explicitNamed = normalized.filter(
    (tool) => tool !== 'all' && tool !== 'all.read'
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

    return {mode: 'all_read', explicitTools: []};
  }

  if (hasAll) {
    if (!isAdmin) {
      return {mode: 'explicit', explicitTools: []};
    }

    return {mode: 'all_expand', explicitTools: []};
  }

  if (hasAllRead) {
    return {mode: 'all_read', explicitTools: []};
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

  if (mode === 'all_expand') {
    acceptedTools.forEach((tool) => {
      const [namespace, action] = tool.split('.');
      configuration.actions![namespace as AvailableNamespaces] = {
        ...configuration.actions![namespace as AvailableNamespaces],
        [action]: true,
      };
    });
    return;
  }

  if (mode === 'all_read') {
    acceptedTools.forEach((tool) => {
      const [namespace, action] = tool.split('.');
      if (action === 'read') {
        configuration.actions![namespace as AvailableNamespaces] = {
          ...configuration.actions![namespace as AvailableNamespaces],
          [action]: true,
        };
      }
    });

    return;
  }

  explicitTools.forEach((tool) => {
    const [namespace, action] = tool.split('.');
    configuration.actions![namespace as AvailableNamespaces] = {
      ...(configuration.actions![namespace as AvailableNamespaces] || {}),
      [action]: true,
    };
  });
}
