import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {CartsHandler} from '@commercetools/tools-core';

const handler = new CartsHandler();

const tools: Record<string, Tool> = {
  read_cart: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Cart',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      cart: {
        read: true,
      },
    },
  },
  create_cart: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Cart',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      cart: {
        create: true,
      },
    },
  },
  replicate_cart: {
    method: handler.getToolDefinition('replicate').name,
    name: 'Replicate Cart',
    description: handler.getToolDefinition('replicate').description,
    parameters: handler.getToolDefinition('replicate')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      cart: {
        create: true,
      },
    },
  },
  update_cart: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Cart',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      cart: {
        update: true,
      },
    },
  },
};

export const contextToCartTools = (context?: Context) => {
  // Associate cart tools when both customerId and businessUnitKey are present
  if (context?.customerId && context?.businessUnitKey) {
    return [
      tools.read_cart,
      tools.create_cart,
      tools.update_cart,
      tools.replicate_cart,
    ];
  }
  if (context?.customerId) {
    return [
      tools.read_cart,
      tools.update_cart,
      tools.replicate_cart,
      tools.create_cart,
    ];
  }
  if (context?.storeKey) {
    return [
      tools.read_cart,
      tools.create_cart,
      tools.update_cart,
      tools.replicate_cart,
    ];
  }
  return [
    tools.read_cart,
    tools.create_cart,
    tools.replicate_cart,
    tools.update_cart,
  ];
};
