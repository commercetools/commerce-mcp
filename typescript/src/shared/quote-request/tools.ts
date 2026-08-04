import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {QuoteRequestsHandler} from '@commercetools/tools-core';

const handler = new QuoteRequestsHandler();

const tools: Record<string, Tool> = {
  read_quote_request: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Quote Request',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'quote-request': {
        read: true,
      },
    },
  },
  create_quote_request: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Quote Request',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'quote-request': {
        create: true,
      },
    },
  },
  update_quote_request: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Quote Request',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'quote-request': {
        update: true,
      },
    },
  },
};

export const contextToQuoteRequestTools = (context?: Context) => {
  if (context?.customerId) {
    return [tools.read_quote_request, tools.update_quote_request];
  }

  return [
    tools.read_quote_request,
    tools.create_quote_request,
    tools.update_quote_request,
  ];
};
