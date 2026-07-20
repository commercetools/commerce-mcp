import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {OrdersHandler} from '@commercetools/tools-core';

const handler = new OrdersHandler();

const tools: Record<string, Tool> = {
  read_order: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Order',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      order: {
        read: true,
      },
    },
  },
  create_order: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Order',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      order: {
        create: true,
      },
    },
  },
  update_order: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Order',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      order: {
        update: true,
      },
    },
  },
};

export const contextToOrderTools = (context?: Context) => {
  if (context?.customerId && context?.businessUnitKey) {
    return [tools.read_order, tools.create_order, tools.update_order];
  }

  if (context?.customerId) {
    return [tools.read_order];
  }

  return [tools.read_order, tools.create_order, tools.update_order];
};
