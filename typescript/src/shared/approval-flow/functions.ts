import * as admin from './admin.functions';
import * as associate from './associate.functions';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import {ApiRoot} from '@commercetools/platform-sdk';
import {z} from 'zod';
import {
  readApprovalFlowParameters,
  updateApprovalFlowParameters,
} from './parameters';

export const contextToApprovalFlowFunctionMapping = (
  context?: Context
): Record<
  string,
  (
    apiRoot: ApiRoot,
    context: CommercetoolsFuncContext,
    params: any
  ) => Promise<any>
> => {
  if (context?.customerId && context?.businessUnitKey) {
    return {
      read_approval_flow: associate.readApprovalFlow,
      update_approval_flow: associate.updateApprovalFlow,
    };
  }
  if (context?.isAdmin) {
    return {
      read_approval_flow: admin.readApprovalFlow,
      update_approval_flow: admin.updateApprovalFlow,
    };
  }
  return {};
};

export const readApprovalFlow = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof readApprovalFlowParameters>
) => {
  if (context?.customerId && context?.businessUnitKey) {
    return associate.readApprovalFlow(apiRoot, context, params);
  }
  return admin.readApprovalFlow(apiRoot, context, params);
};

export const updateApprovalFlow = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof updateApprovalFlowParameters>
) => {
  if (context?.customerId && context?.businessUnitKey) {
    return associate.updateApprovalFlow(apiRoot, context, params);
  }
  return admin.updateApprovalFlow(apiRoot, context, params);
};
