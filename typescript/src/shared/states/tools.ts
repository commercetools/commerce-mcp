import {readStatePrompt, createStatePrompt, updateStatePrompt} from './prompts';
import {
  readStateParameters,
  createStateParameters,
  updateStateParameters,
} from './parameters';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {z} from 'zod';

const tools: Record<string, Tool> = {
  read_state: {
    method: 'read_state',
    name: 'Read State',
    description: readStatePrompt,
    parameters: readStateParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {states: {read: true}},
  },
  create_state: {
    method: 'create_state',
    name: 'Create State',
    description: createStatePrompt,
    parameters: createStateParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {states: {create: true}},
  },
  update_state: {
    method: 'update_state',
    name: 'Update State',
    description: updateStatePrompt,
    parameters: updateStateParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {states: {update: true}},
  },
};

export const contextToStateTools = (context?: Context) => {
  if (context?.isAdmin) {
    return [tools.read_state, tools.create_state, tools.update_state];
  }
  return [];
};
