import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {CartDiscountsHandler} from '@commercetools/tools-core';

const handler = new CartDiscountsHandler();

const tools: Record<string, Tool> = {
  read_cart_discount: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Cart Discount',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'cart-discount': {
        read: true,
      },
    },
  },
  create_cart_discount: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Cart Discount',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'cart-discount': {
        create: true,
      },
    },
  },
  update_cart_discount: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Cart Discount',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'cart-discount': {
        update: true,
      },
    },
  },
};

export const contextToCartDiscountTools = (_context?: Context) => {
  return [
    tools.read_cart_discount,
    tools.create_cart_discount,
    tools.update_cart_discount,
  ];
};
