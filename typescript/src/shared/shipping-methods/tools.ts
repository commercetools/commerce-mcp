import {z} from 'zod';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {ShippingMethodsHandler} from '@commercetools/tools-core';

const handler = new ShippingMethodsHandler();

const tools: Record<string, Tool> = {
  read_shipping_methods: {
    name: 'Read Shipping Method',
    method: handler.getToolDefinition('read').name,
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'shipping-methods': {
        read: true,
      },
    },
  },
  create_shipping_methods: {
    name: 'Create Shipping Method',
    method: handler.getToolDefinition('create').name,
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'shipping-methods': {
        create: true,
      },
    },
  },
  update_shipping_methods: {
    name: 'Update Shipping Method',
    method: handler.getToolDefinition('update').name,
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'shipping-methods': {
        update: true,
      },
    },
  },
};

export const contextToShippingMethodTools = (context?: Context) => {
  if (context?.customerId) {
    return [tools.read_shipping_methods];
  }
  return [
    tools.read_shipping_methods,
    tools.create_shipping_methods,
    tools.update_shipping_methods,
  ];
};
