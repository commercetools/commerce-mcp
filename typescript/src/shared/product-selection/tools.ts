import {z} from 'zod';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {ProductSelectionsHandler} from '@commercetools/tools-core';

const handler = new ProductSelectionsHandler();

const tools: Record<string, Tool> = {
  read_product_selection: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Product Selection',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-selection': {
        read: true,
      },
    },
  },
  create_product_selection: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Product Selection',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-selection': {
        create: true,
      },
    },
  },
  update_product_selection: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Product Selection',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-selection': {
        update: true,
      },
    },
  },
};

export const contextToProductSelectionTools = (_context?: Context) => {
  return [
    tools.read_product_selection,
    tools.create_product_selection,
    tools.update_product_selection,
  ];
};
