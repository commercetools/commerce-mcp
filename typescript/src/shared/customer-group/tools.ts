import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {CustomerGroupsHandler} from '@commercetools/tools-core';

const handler = new CustomerGroupsHandler();

const tools: Record<string, Tool> = {
  read_customer_group: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Customer Group',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'customer-group': {
        read: true,
      },
    },
  },
  create_customer_group: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Customer Group',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'customer-group': {
        create: true,
      },
    },
  },
  update_customer_group: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Customer Group',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'customer-group': {
        update: true,
      },
    },
  },
};

export const contextToCustomerGroupTools = (_context?: Context) => {
  return [
    tools.read_customer_group,
    tools.create_customer_group,
    tools.update_customer_group,
  ];
};
