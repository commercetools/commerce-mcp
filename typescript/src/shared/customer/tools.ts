import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {CustomersHandler} from '@commercetools/tools-core';

const handler = new CustomersHandler();

const tools: Record<string, Tool> = {
  create_customer: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Customer',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      customer: {
        create: true,
      },
    },
  },
  read_customer: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Customer',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      customer: {
        read: true,
      },
    },
  },
  update_customer: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Customer',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      customer: {
        update: true,
      },
    },
  },
};

export const contextToCustomerTools = (context?: Context) => {
  if (context?.customerId) {
    return [tools.read_customer];
  }
  if (context?.storeKey) {
    return [tools.create_customer, tools.read_customer];
  }
  return [tools.create_customer, tools.read_customer, tools.update_customer];
};
