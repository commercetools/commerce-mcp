import {
  readRecurrencePolicyPrompt,
  createRecurrencePolicyPrompt,
  updateRecurrencePolicyPrompt,
} from './prompts';
import {
  readRecurrencePolicyParameters,
  createRecurrencePolicyParameters,
  updateRecurrencePolicyParameters,
} from './parameters';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {z} from 'zod';

const tools: Record<string, Tool> = {
  read_recurrence_policy: {
    method: 'read_recurrence_policy',
    name: 'Read Recurrence Policy',
    description: readRecurrencePolicyPrompt,
    parameters: readRecurrencePolicyParameters as unknown as z.ZodObject<
      any,
      any,
      any,
      any
    >,
    actions: {
      'recurrence-policy': {read: true},
    },
  },
  create_recurrence_policy: {
    method: 'create_recurrence_policy',
    name: 'Create Recurrence Policy',
    description: createRecurrencePolicyPrompt,
    parameters: createRecurrencePolicyParameters as unknown as z.ZodObject<
      any,
      any,
      any,
      any
    >,
    actions: {
      'recurrence-policy': {create: true},
    },
  },
  update_recurrence_policy: {
    method: 'update_recurrence_policy',
    name: 'Update Recurrence Policy',
    description: updateRecurrencePolicyPrompt,
    parameters: updateRecurrencePolicyParameters as unknown as z.ZodObject<
      any,
      any,
      any,
      any
    >,
    actions: {
      'recurrence-policy': {update: true},
    },
  },
};

export const contextToRecurrencePolicyTools = (context?: Context) => {
  if (context?.isAdmin) {
    return [
      tools.read_recurrence_policy,
      tools.create_recurrence_policy,
      tools.update_recurrence_policy,
    ];
  }
  return [];
};
