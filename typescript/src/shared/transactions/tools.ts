import {z} from 'zod';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {TransactionsHandler} from '@commercetools/tools-core';

const handler = new TransactionsHandler();

const tools: Record<string, Tool> = {
  read_transaction: {
    name: 'Read Transaction',
    method: handler.getToolDefinition('read').name,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('read').description,
    actions: {
      transactions: {
        read: true,
      },
    },
  },
  create_transaction: {
    name: 'Create Transaction',
    method: handler.getToolDefinition('create').name,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('create').description,
    actions: {
      transactions: {
        create: true,
      },
    },
  },
};

export const contextToTransactionTools = (_context?: Context) => {
  return [tools.read_transaction, tools.create_transaction];
};
