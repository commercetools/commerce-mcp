import {readApprovalFlowPrompt, updateApprovalFlowPrompt} from './prompts';
import {
  readApprovalFlowParameters,
  updateApprovalFlowParameters,
} from './parameters';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {z} from 'zod';

const tools: Record<string, Tool> = {
  read_approval_flow: {
    method: 'read_approval_flow',
    name: 'Read Approval Flow',
    description: readApprovalFlowPrompt,
    parameters: readApprovalFlowParameters as unknown as z.ZodObject<
      any,
      any,
      any,
      any
    >,
    actions: {
      'approval-flow': {
        read: true,
      },
    },
  },
  update_approval_flow: {
    method: 'update_approval_flow',
    name: 'Update Approval Flow',
    description: updateApprovalFlowPrompt,
    parameters: updateApprovalFlowParameters as unknown as z.ZodObject<
      any,
      any,
      any,
      any
    >,
    actions: {
      'approval-flow': {
        update: true,
      },
    },
  },
};

export const contextToApprovalFlowTools = (context?: Context) => {
  if (context?.isAdmin || (context?.customerId && context?.businessUnitKey)) {
    return [tools.read_approval_flow, tools.update_approval_flow];
  }
  return [];
};
