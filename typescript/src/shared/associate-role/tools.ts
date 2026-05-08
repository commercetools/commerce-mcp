import {
  readAssociateRolePrompt,
  createAssociateRolePrompt,
  updateAssociateRolePrompt,
} from './prompts';
import {
  readAssociateRoleParameters,
  createAssociateRoleParameters,
  updateAssociateRoleParameters,
} from './parameters';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {z} from 'zod';

const tools: Record<string, Tool> = {
  read_associate_role: {
    method: 'read_associate_role',
    name: 'Read Associate Role',
    description: readAssociateRolePrompt,
    parameters: readAssociateRoleParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {'associate-role': {read: true}},
  },
  create_associate_role: {
    method: 'create_associate_role',
    name: 'Create Associate Role',
    description: createAssociateRolePrompt,
    parameters: createAssociateRoleParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {'associate-role': {create: true}},
  },
  update_associate_role: {
    method: 'update_associate_role',
    name: 'Update Associate Role',
    description: updateAssociateRolePrompt,
    parameters: updateAssociateRoleParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {'associate-role': {update: true}},
  },
};

export const contextToAssociateRoleTools = (context?: Context) => {
  if (context?.customerId && context?.businessUnitKey) {
    return [tools.read_associate_role];
  }
  if (context?.isAdmin) {
    return [
      tools.read_associate_role,
      tools.create_associate_role,
      tools.update_associate_role,
    ];
  }
  return [];
};
