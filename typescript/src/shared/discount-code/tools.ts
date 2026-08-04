import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {DiscountCodesHandler} from '@commercetools/tools-core';

const handler = new DiscountCodesHandler();

const tools: Record<string, Tool> = {
  read_discount_code: {
    method: handler.getToolDefinition('read').name,
    name: 'Read Discount Code',
    description: handler.getToolDefinition('read').description,
    parameters: handler.getToolDefinition('read')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'discount-code': {
        read: true,
      },
    },
  },
  create_discount_code: {
    method: handler.getToolDefinition('create').name,
    name: 'Create Discount Code',
    description: handler.getToolDefinition('create').description,
    parameters: handler.getToolDefinition('create')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'discount-code': {
        create: true,
      },
    },
  },
  update_discount_code: {
    method: handler.getToolDefinition('update').name,
    name: 'Update Discount Code',
    description: handler.getToolDefinition('update').description,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    actions: {
      'discount-code': {
        update: true,
      },
    },
  },
};

export const contextToDiscountCodeTools = (_context?: Context) => {
  return [
    tools.read_discount_code,
    tools.create_discount_code,
    tools.update_discount_code,
  ];
};
