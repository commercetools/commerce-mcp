import {z} from 'zod';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {ProductSearchHandler} from '@commercetools/tools-core';

const handler = new ProductSearchHandler();

const tools: Record<string, Tool> = {
  search_products: {
    method: handler.getToolDefinition('read').name,
    name: 'Search Products',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'product-search': {
        read: true,
      },
    },
  },
};

export const contextToProductSearchTools = (context?: Context) => {
  return [tools.search_products];
};
