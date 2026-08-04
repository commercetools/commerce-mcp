import {Context} from '../../types/configuration';
import {Tool} from '../../types/tools';
import {z} from 'zod';
import {StagedQuotesHandler} from '@commercetools/tools-core';

const handler = new StagedQuotesHandler();

const tools: Record<string, Tool> = {
  read_staged_quote: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Staged Quote',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'staged-quote': {
        read: true,
      },
    },
  },
  create_staged_quote: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Staged Quote',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'staged-quote': {
        create: true,
      },
    },
  },
  update_staged_quote: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Staged Quote',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'staged-quote': {
        update: true,
      },
    },
  },
};

export const contextToStagedQuoteTools = (_context?: Context) => {
  return [
    tools.read_staged_quote,
    tools.create_staged_quote,
    tools.update_staged_quote,
  ];
};
