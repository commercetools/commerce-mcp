import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {ExtensionsHandler} from '@commercetools/tools-core';

const handler = new ExtensionsHandler();

const tools: Record<string, Tool> = {
  read_extension: {
    name: 'Read Extension',
    method: handler.getToolDefinition('read').name,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('read').description,
    actions: {
      extensions: {
        read: true,
      },
    },
  },
  create_extension: {
    name: 'Create Extension',
    method: handler.getToolDefinition('create').name,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('create').description,
    actions: {
      extensions: {
        create: true,
      },
    },
  },
  update_extension: {
    name: 'Update Extension',
    method: handler.getToolDefinition('update').name,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('update').description,
    actions: {
      extensions: {
        update: true,
      },
    },
  },
};

export const contextToExtensionTools = (_context?: Context) => {
  return [tools.read_extension, tools.create_extension, tools.update_extension];
};
