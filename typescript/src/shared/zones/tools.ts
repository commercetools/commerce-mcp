import {z} from 'zod';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {ZonesHandler} from '@commercetools/tools-core';

const handler = new ZonesHandler();

const tools: Record<string, Tool> = {
  read_zone: {
    name: 'Read Zone',
    method: handler.getToolDefinition('read').name,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('read').description,
    actions: {
      zone: {
        read: true,
      },
    },
  },
  create_zone: {
    name: 'Create Zone',
    method: handler.getToolDefinition('create').name,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('create').description,
    actions: {
      zone: {
        create: true,
      },
    },
  },
  update_zone: {
    name: 'Update Zone',
    method: handler.getToolDefinition('update').name,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('update').description,
    actions: {
      zone: {
        update: true,
      },
    },
  },
};

export const contextToZoneTools = (_context?: Context) => {
  return [tools.read_zone, tools.create_zone, tools.update_zone];
};
