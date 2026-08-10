import {Context} from '../types/configuration';
import {buildResourceTools} from './bridge';

/**
 * Per-resource tool map for the given context, produced from the
 * `@commercetools/tools-core` handlers via the bridge. The keys are the
 * commerce-mcp resource namespaces (used by the resource-based tool system and
 * for scope/action filtering).
 */
export const contextToResourceTools = (context?: Context) =>
  buildResourceTools(context);

export const contextToTools = (context?: Context) => {
  const resourceTools = contextToResourceTools(context);

  return Object.values(resourceTools).flat();
};
