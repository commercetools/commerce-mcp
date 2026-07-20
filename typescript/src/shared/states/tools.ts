import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {z} from 'zod';
import {StatesHandler} from '@commercetools/tools-core';

const handler = new StatesHandler();

const tools: Record<string, Tool> = {
  read_state: {
    method: handler.getToolDefinition('read').name,
    name: 'Read State',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {states: {read: true}},
  },
  create_state: {
    method: handler.getToolDefinition('create').name,
    name: 'Create State',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {states: {create: true}},
  },
  update_state: {
    method: handler.getToolDefinition('update').name,
    name: 'Update State',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {states: {update: true}},
  },
};

export const contextToStateTools = (context?: Context) => {
  if (context?.isAdmin) {
    return [tools.read_state, tools.create_state, tools.update_state];
  }
  return [];
};
