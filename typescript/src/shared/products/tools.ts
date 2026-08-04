import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {ProductsHandler} from '@commercetools/tools-core';

const handler = new ProductsHandler();

const tools: Record<string, Tool> = {
  list_products: {
    method: handler.getToolDefinition('read').name,
    name: 'List Products',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      products: {
        read: true,
      },
    },
  },
  create_product: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Product',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      products: {
        create: true,
      },
    },
  },
  update_product: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Product',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      products: {
        update: true,
      },
    },
  },
};

export const contextToProductsTools = (_context?: Context) => {
  return [tools.list_products, tools.create_product, tools.update_product];
};
