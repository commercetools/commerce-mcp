import {
  listAvailableToolsPrompt,
  injectToolsPrompt,
  executeToolPrompt,
} from './prompts';

import {
  listAvailableToolsParameters,
  injectToolsParameters,
  executeToolParameters,
} from './parameters';
import {Tool} from '../../types/tools';

const getTools = (resources: string[]): Record<string, Tool> => {
  return {
    list_available_tools: {
      method: 'list_available_tools',
      name: 'List Available Tools',
      description: listAvailableToolsPrompt(resources),
      parameters: listAvailableToolsParameters(resources),
      actions: {},
    },
    inject_tools: {
      method: 'inject_tools',
      name: 'Inject Tools',
      description: injectToolsPrompt,
      parameters: injectToolsParameters,
      actions: {},
    },
    execute_tool: {
      method: 'execute_tool',
      name: 'Execute Tool',
      description: executeToolPrompt,
      parameters: executeToolParameters,
      actions: {},
    },
  };
};

/**
 * The tools this module registers itself, as opposed to ones from the
 * `@commercetools/tools-core` catalogue.
 *
 * Derived from {@link getTools} rather than written out, so adding a tool
 * there cannot leave this behind. The resource list is irrelevant to the
 * method names, so an empty one is enough.
 */
export const RESOURCE_SYSTEM_TOOL_METHODS: ReadonlySet<string> = new Set(
  Object.keys(getTools([]))
);

export const contextToToolsResourceBasedToolSystem = (resources: string[]) => {
  const tools = getTools(resources);

  return {
    listAvailableTools: tools.list_available_tools,
    injectTools: tools.inject_tools,
    executeTool: tools.execute_tool,
  };
};
