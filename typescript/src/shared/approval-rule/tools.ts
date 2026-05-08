import {
  readApprovalRulePrompt,
  createApprovalRulePrompt,
  updateApprovalRulePrompt,
} from './prompts';
import {
  readApprovalRuleParameters,
  createApprovalRuleParameters,
  updateApprovalRuleParameters,
} from './parameters';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {z} from 'zod';

const tools: Record<string, Tool> = {
  read_approval_rule: {
    method: 'read_approval_rule',
    name: 'Read Approval Rule',
    description: readApprovalRulePrompt,
    parameters: readApprovalRuleParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {'approval-rule': {read: true}},
  },
  create_approval_rule: {
    method: 'create_approval_rule',
    name: 'Create Approval Rule',
    description: createApprovalRulePrompt,
    parameters: createApprovalRuleParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {'approval-rule': {create: true}},
  },
  update_approval_rule: {
    method: 'update_approval_rule',
    name: 'Update Approval Rule',
    description: updateApprovalRulePrompt,
    parameters: updateApprovalRuleParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {'approval-rule': {update: true}},
  },
};

export const contextToApprovalRuleTools = (context?: Context) => {
  if (context?.isAdmin || (context?.customerId && context?.businessUnitKey)) {
    return [tools.read_approval_rule, tools.create_approval_rule, tools.update_approval_rule];
  }
  return [];
};
