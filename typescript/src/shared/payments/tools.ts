import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {PaymentsHandler} from '@commercetools/tools-core';

const handler = new PaymentsHandler();

const tools: Record<string, Tool> = {
  read_payments: {
    name: 'Read Payment',
    method: handler.getToolDefinition('read').name,
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      payments: {
        read: true,
      },
    },
  },
  create_payments: {
    name: 'Create Payment',
    method: handler.getToolDefinition('create').name,
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      payments: {
        create: true,
      },
    },
  },
  update_payments: {
    name: 'Update Payment',
    method: handler.getToolDefinition('update').name,
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      payments: {
        update: true,
      },
    },
  },
};

export const contextToPaymentTools = (_context?: Context) => {
  return [tools.read_payments, tools.create_payments, tools.update_payments];
};
