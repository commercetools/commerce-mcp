import {z} from 'zod';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {ProductDiscountsHandler} from '@commercetools/tools-core';

const handler = new ProductDiscountsHandler();

const tools: Record<string, Tool> = {
  read_product_discount: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Product Discount',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-discount': {
        read: true,
      },
    },
  },
  create_product_discount: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Product Discount',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-discount': {
        create: true,
      },
    },
  },
  update_product_discount: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Product Discount',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-discount': {
        update: true,
      },
    },
  },
};

export const contextToProductDiscountTools = (_context?: Context) => {
  return [
    tools.read_product_discount,
    tools.create_product_discount,
    tools.update_product_discount,
  ];
};
