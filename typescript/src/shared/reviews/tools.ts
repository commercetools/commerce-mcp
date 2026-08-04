import {z} from 'zod';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {ReviewsHandler} from '@commercetools/tools-core';

const handler = new ReviewsHandler();

const tools: Record<string, Tool> = {
  read_review: {
    name: 'Read Review',
    method: handler.getToolDefinition('read').name,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('read').description,
    actions: {
      review: {
        read: true,
      },
    },
  },
  create_review: {
    name: 'Create Review',
    method: handler.getToolDefinition('create').name,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('create').description,
    actions: {
      review: {
        create: true,
      },
    },
  },
  update_review: {
    name: 'Update Review',
    method: handler.getToolDefinition('update').name,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('update').description,
    actions: {
      review: {
        update: true,
      },
    },
  },
};

export const contextToReviewTools = (_context?: Context) => {
  return [tools.read_review, tools.create_review, tools.update_review];
};
