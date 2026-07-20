import {z} from 'zod';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {TypesHandler} from '@commercetools/tools-core';

const handler = new TypesHandler();

const tools: Record<string, Tool> = {
  read_type: {
    name: 'Read Type',
    method: handler.getToolDefinition('read').name,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('read').description,
    actions: {
      types: {
        read: true,
      },
    },
  },
  create_type: {
    name: 'Create Type',
    method: handler.getToolDefinition('create').name,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('create').description,
    actions: {
      types: {
        create: true,
      },
    },
  },
  update_type: {
    name: 'Update Type',
    method: handler.getToolDefinition('update').name,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('update').description,
    actions: {
      types: {
        update: true,
      },
    },
  },
};

export const contextToTypeTools = (_context?: Context) => {
  return [tools.read_type, tools.create_type, tools.update_type];
};
