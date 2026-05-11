import {ApiRoot} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import * as admin from './admin.functions';
import * as associate from './associate.functions';

export const contextToApprovalRuleFunctionMapping = (
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
      read_approval_rule: associate.readApprovalRule,
      create_approval_rule: associate.createApprovalRule,
      update_approval_rule: associate.updateApprovalRule,
    };
  }
  if (context?.isAdmin) {
    return {
      read_approval_rule: admin.readApprovalRule,
      create_approval_rule: admin.createApprovalRule,
      update_approval_rule: admin.updateApprovalRule,
    };
  }
  return {};
};

export const readApprovalRule = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  if (context?.customerId && context?.businessUnitKey) {
    return associate.readApprovalRule(apiRoot, context, params);
  }
  return admin.readApprovalRule(apiRoot, context, params);
};

export const createApprovalRule = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  if (context?.customerId && context?.businessUnitKey) {
    return associate.createApprovalRule(apiRoot, context, params);
  }
  return admin.createApprovalRule(apiRoot, context, params);
};

export const updateApprovalRule = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  if (context?.customerId && context?.businessUnitKey) {
    return associate.updateApprovalRule(apiRoot, context, params);
  }
  return admin.updateApprovalRule(apiRoot, context, params);
};
