import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {ProductTailoringHandler} from '@commercetools/tools-core';

const handler = new ProductTailoringHandler();

/**
 * Context-based tool mapping for product tailoring
 */
const tools: Record<string, Tool> = {
  read_product_tailoring: {
    name: 'Read product tailoring',
    method: handler.getToolDefinition('read').name,
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-tailoring': {
        read: true,
      },
    },
  },
  create_product_tailoring: {
    name: 'Create product tailoring',
    method: handler.getToolDefinition('create').name,
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-tailoring': {
        create: true,
      },
    },
  },
  update_product_tailoring: {
    name: 'Update product tailoring',
    method: handler.getToolDefinition('update').name,
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-tailoring': {
        update: true,
      },
    },
  },
};

export const contextToProductTailoringTools = (_context?: Context) => {
  return [
    tools.read_product_tailoring,
    tools.create_product_tailoring,
    tools.update_product_tailoring,
  ];
};
