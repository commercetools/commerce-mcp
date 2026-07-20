import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {z} from 'zod';
import {SubscriptionsHandler} from '@commercetools/tools-core';

const handler = new SubscriptionsHandler();

const tools: Record<string, Tool> = {
  read_subscription: {
    name: 'Read Subscription',
    method: handler.getToolDefinition('read').name,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('read').description,
    actions: {
      subscriptions: {
        read: true,
      },
    },
  },
  create_subscription: {
    name: 'Create Subscription',
    method: handler.getToolDefinition('create').name,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('create').description,
    actions: {
      subscriptions: {
        create: true,
      },
    },
  },
  update_subscription: {
    name: 'Update Subscription',
    method: handler.getToolDefinition('update').name,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('update').description,
    actions: {
      subscriptions: {
        update: true,
      },
    },
  },
};

export const contextToSubscriptionTools = (_context?: Context) => {
  return [
    tools.read_subscription,
    tools.create_subscription,
    tools.update_subscription,
  ];
};
