import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {QuotesHandler} from '@commercetools/tools-core';

const handler = new QuotesHandler();

const tools: Record<string, Tool> = {
  read_quote: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Quote',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      quote: {
        read: true,
      },
    },
  },
  create_quote: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Quote',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      quote: {
        create: true,
      },
    },
  },
  update_quote: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Quote',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      quote: {
        update: true,
      },
    },
  },
};

export const contextToQuoteTools = (context?: Context) => {
  // Associate quote tools when both customerId and businessUnitKey are present
  if (context?.customerId && context?.businessUnitKey) {
    return [tools.read_quote, tools.update_quote];
  }
  if (context?.customerId) {
    return [tools.read_quote, tools.update_quote];
  }

  return [tools.read_quote, tools.create_quote, tools.update_quote];
};
