import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {ProductTypesHandler} from '@commercetools/tools-core';

const handler = new ProductTypesHandler();

const tools: Record<string, Tool> = {
  read_product_type: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Product Type',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-type': {
        read: true,
      },
    },
  },
  create_product_type: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Product Type',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-type': {
        create: true,
      },
    },
  },
  update_product_type: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Product Type',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-type': {
        update: true,
      },
    },
  },
};

export const contextToProductTypeTools = (_context?: Context) => {
  return [
    tools.read_product_type,
    tools.create_product_type,
    tools.update_product_type,
  ];
};
