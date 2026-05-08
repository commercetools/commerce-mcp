import {
  readOrderEditPrompt,
  createOrderEditPrompt,
  updateOrderEditPrompt,
  applyOrderEditPrompt,
} from './prompts';
import {
  readOrderEditParameters,
  createOrderEditParameters,
  updateOrderEditParameters,
  applyOrderEditParameters,
} from './parameters';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {z} from 'zod';

const tools: Record<string, Tool> = {
  read_order_edit: {
    method: 'read_order_edit',
    name: 'Read Order Edit',
    description: readOrderEditPrompt,
    parameters: readOrderEditParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {'order-edit': {read: true}},
  },
  create_order_edit: {
    method: 'create_order_edit',
    name: 'Create Order Edit',
    description: createOrderEditPrompt,
    parameters: createOrderEditParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {'order-edit': {create: true}},
  },
  update_order_edit: {
    method: 'update_order_edit',
    name: 'Update Order Edit',
    description: updateOrderEditPrompt,
    parameters: updateOrderEditParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {'order-edit': {update: true}},
  },
  apply_order_edit: {
    method: 'apply_order_edit',
    name: 'Apply Order Edit',
    description: applyOrderEditPrompt,
    parameters: applyOrderEditParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {'order-edit': {update: true}},
  },
};

export const contextToOrderEditTools = (context?: Context) => {
  if (context?.isAdmin) {
    return [
      tools.read_order_edit,
      tools.create_order_edit,
      tools.update_order_edit,
      tools.apply_order_edit,
    ];
  }
  return [];
};
