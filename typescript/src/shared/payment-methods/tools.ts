import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {PaymentMethodsHandler} from '@commercetools/tools-core';

const handler = new PaymentMethodsHandler();

const tools: Record<string, Tool> = {
  read_payment_methods: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Payment Method',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'payment-methods': {
        read: true,
      },
    },
  },
  create_payment_methods: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Payment Method',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'payment-methods': {
        create: true,
      },
    },
  },
  update_payment_methods: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Payment Method',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'payment-methods': {
        update: true,
      },
    },
  },
};

export const contextToPaymentMethodTools = (_context?: Context) => {
  return [
    tools.read_payment_methods,
    tools.create_payment_methods,
    tools.update_payment_methods,
  ];
};
