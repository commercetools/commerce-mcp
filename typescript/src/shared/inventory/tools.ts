import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {InventoryHandler} from '@commercetools/tools-core';

const handler = new InventoryHandler();

const tools: Record<string, Tool> = {
  read_inventory: {
    name: 'Read Inventory',
    method: handler.getToolDefinition('read').name,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('read').description,
    actions: {
      inventory: {
        read: true,
      },
    },
  },
  create_inventory: {
    name: 'Create Inventory',
    method: handler.getToolDefinition('create').name,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('create').description,
    actions: {
      inventory: {
        create: true,
      },
    },
  },
  update_inventory: {
    name: 'Update Inventory',
    method: handler.getToolDefinition('update').name,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('update').description,
    actions: {
      inventory: {
        update: true,
      },
    },
  },
};

export const contextToInventoryTools = (_context?: Context) => {
  return [tools.read_inventory, tools.create_inventory, tools.update_inventory];
};
