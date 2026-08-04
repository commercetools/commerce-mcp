import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {BusinessUnitsHandler} from '@commercetools/tools-core';

const handler = new BusinessUnitsHandler();

const tools: Record<string, Tool> = {
  read_business_unit: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Business Unit',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'business-unit': {
        read: true,
      },
    },
  },
  create_business_unit: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Business Unit',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'business-unit': {
        create: true,
      },
    },
  },
  update_business_unit: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Business Unit',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'business-unit': {
        update: true,
      },
    },
  },
};

export const contextToBusinessUnitTools = (_context?: Context) => {
  return [
    tools.read_business_unit,
    tools.create_business_unit,
    tools.update_business_unit,
  ];
};
