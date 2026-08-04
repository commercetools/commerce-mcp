import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {CategoriesHandler} from '@commercetools/tools-core';

const handler = new CategoriesHandler();

const tools: Record<string, Tool> = {
  read_category: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Category',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      category: {
        read: true,
      },
    },
  },
  create_category: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Category',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      category: {
        create: true,
      },
    },
  },
  update_category: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Category',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      category: {
        update: true,
      },
    },
  },
};

export const contextToCategoryTools = (_context?: Context) => {
  return [tools.read_category, tools.create_category, tools.update_category];
};
