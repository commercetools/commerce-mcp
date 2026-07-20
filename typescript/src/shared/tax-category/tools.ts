import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {z} from 'zod';
import {TaxCategoriesHandler} from '@commercetools/tools-core';

const handler = new TaxCategoriesHandler();

const tools: Record<string, Tool> = {
  read_tax_category: {
    name: 'Read Tax Category',
    method: handler.getToolDefinition('read').name,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('read').description,
    actions: {
      'tax-category': {
        read: true,
      },
    },
  },
  create_tax_category: {
    name: 'Create Tax Category',
    method: handler.getToolDefinition('create').name,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('create').description,
    actions: {
      'tax-category': {
        create: true,
      },
    },
  },
  update_tax_category: {
    name: 'Update Tax Category',
    method: handler.getToolDefinition('update').name,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('update').description,
    actions: {
      'tax-category': {
        update: true,
      },
    },
  },
};

export const contextToTaxCategoryTools = (_context?: Context) => {
  return [
    tools.read_tax_category,
    tools.create_tax_category,
    tools.update_tax_category,
  ];
};
