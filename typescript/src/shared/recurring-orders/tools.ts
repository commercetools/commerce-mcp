import {z} from 'zod';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {RecurringOrdersHandler} from '@commercetools/tools-core';

const handler = new RecurringOrdersHandler();

const tools: Record<string, Tool> = {
  read_recurring_orders: {
    name: 'Read Recurring Orders',
    method: handler.getToolDefinition('read').name,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('read').description,
    actions: {
      'recurring-orders': {
        read: true,
      },
    },
  },
  create_recurring_orders: {
    name: 'Create Recurring Orders',
    method: handler.getToolDefinition('create').name,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('create').description,
    actions: {
      'recurring-orders': {
        create: true,
      },
    },
  },
  update_recurring_orders: {
    name: 'Update Recurring Orders',
    method: handler.getToolDefinition('update').name,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('update').description,
    actions: {
      'recurring-orders': {
        update: true,
      },
    },
  },
};

export const contextToRecurringOrderTools = (context?: Context) => {
  if (context?.customerId) {
    return [tools.read_recurring_orders];
  }
  return [
    tools.read_recurring_orders,
    tools.create_recurring_orders,
    tools.update_recurring_orders,
  ];
};
