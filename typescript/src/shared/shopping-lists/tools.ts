import {z} from 'zod';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {ShoppingListsHandler} from '@commercetools/tools-core';

const handler = new ShoppingListsHandler();

const tools: Record<string, Tool> = {
  read_shopping_list: {
    name: 'Read Shopping List',
    method: handler.getToolDefinition('read').name,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('read').description,
    actions: {
      'shopping-lists': {
        read: true,
      },
    },
  },
  create_shopping_list: {
    name: 'Create Shopping List',
    method: handler.getToolDefinition('create').name,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('create').description,
    actions: {
      'shopping-lists': {
        create: true,
      },
    },
  },
  update_shopping_list: {
    name: 'Update Shopping List',
    method: handler.getToolDefinition('update').name,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('update').description,
    actions: {
      'shopping-lists': {
        update: true,
      },
    },
  },
};

export const contextToShoppingListTools = (_context?: Context) => {
  return [
    tools.read_shopping_list,
    tools.create_shopping_list,
    tools.update_shopping_list,
  ];
};
