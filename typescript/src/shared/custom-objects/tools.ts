import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {CustomObjectsHandler} from '@commercetools/tools-core';

const handler = new CustomObjectsHandler();

const tools: Record<string, Tool> = {
  read_custom_object: {
    name: 'Read Custom Object',
    method: handler.getToolDefinition('read').name,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('read').description,
    actions: {
      'custom-objects': {
        read: true,
      },
    },
  },
  create_custom_object: {
    name: 'Create Custom Object',
    method: handler.getToolDefinition('create').name,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('create').description,
    actions: {
      'custom-objects': {
        create: true,
      },
    },
  },
  update_custom_object: {
    name: 'Update Custom Object',
    method: handler.getToolDefinition('update').name,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('update').description,
    actions: {
      'custom-objects': {
        update: true,
      },
    },
  },
};

export const contextToCustomObjectTools = (_context?: Context) => {
  return [
    tools.read_custom_object,
    tools.create_custom_object,
    tools.update_custom_object,
  ];
};
