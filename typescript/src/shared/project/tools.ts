import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {ProjectHandler} from '@commercetools/tools-core';

const handler = new ProjectHandler();

const tools: Record<string, Tool> = {
  read_project: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Project',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      project: {
        read: true,
      },
    },
  },
  update_project: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Project',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      project: {
        update: true,
      },
    },
  },
};

export const contextToProjectTools = (_context?: Context) => {
  return [tools.read_project, tools.update_project];
};
