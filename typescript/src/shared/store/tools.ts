import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {StoresHandler} from '@commercetools/tools-core';

const handler = new StoresHandler();

const tools: Record<string, Tool> = {
  read_store: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Store',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      store: {
        read: true,
      },
    },
  },
  create_store: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Store',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      store: {
        create: true,
      },
    },
  },
  update_store: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Store',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      store: {
        update: true,
      },
    },
  },
};

export const contextToStoreTools = (context?: Context) => {
  if (context?.storeKey) {
    return [tools.read_store];
  }
  return [tools.read_store, tools.create_store, tools.update_store];
};
