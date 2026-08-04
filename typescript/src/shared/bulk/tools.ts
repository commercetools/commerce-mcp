import {z} from 'zod';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {BulkHandler} from '@commercetools/tools-core';

const handler = new BulkHandler();

const tools: Record<string, Tool> = {
  bulk_create: {
    method: handler.getToolDefinition('create').name,
    name: 'Bulk Create',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      bulk: {
        create: true,
      },
    },
  },
  bulk_update: {
    method: handler.getToolDefinition('update').name,
    name: 'Bulk Update',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      bulk: {
        update: true,
      },
    },
  },
};

export const contextToBulkTools = (_context?: Context) => {
  return [tools.bulk_create, tools.bulk_update];
};
