import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {ChannelsHandler} from '@commercetools/tools-core';

const handler = new ChannelsHandler();

const tools: Record<string, Tool> = {
  read_channel: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Channel',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      channel: {
        read: true,
      },
    },
  },
  create_channel: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Channel',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      channel: {
        create: true,
      },
    },
  },
  update_channel: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Channel',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      channel: {
        update: true,
      },
    },
  },
};

export const contextToChannelTools = (_context?: Context) => {
  return [tools.read_channel, tools.create_channel, tools.update_channel];
};
