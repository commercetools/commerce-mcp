import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {StandalonePricesHandler} from '@commercetools/tools-core';

const handler = new StandalonePricesHandler();

const tools: Record<string, Tool> = {
  read_standalone_price: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Standalone Price',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'standalone-price': {
        read: true,
      },
    },
  },
  create_standalone_price: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Standalone Price',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'standalone-price': {
        create: true,
      },
    },
  },
  update_standalone_price: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Standalone Price',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'standalone-price': {
        update: true,
      },
    },
  },
};

export const contextToStandalonePriceTools = (_context?: Context) => {
  return [
    tools.read_standalone_price,
    tools.create_standalone_price,
    tools.update_standalone_price,
  ];
};
