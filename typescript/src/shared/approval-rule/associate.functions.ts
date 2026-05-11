import {z} from 'zod';
import {
  ApiRoot,
  ApprovalRuleDraft,
  ApprovalRuleUpdateAction,
} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
import {CommercetoolsFuncContext} from '../../types/configuration';
import {
  readApprovalRuleById,
  readApprovalRuleByKey,
  queryApprovalRules,
  createApprovalRule as createBase,
  updateApprovalRuleById,
  updateApprovalRuleByKey,
} from './base.functions';
import {
  readApprovalRuleParameters,
  createApprovalRuleParameters,
  updateApprovalRuleParameters,
} from './parameters';

export const readApprovalRule = async (
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof readApprovalRuleParameters>
) => {
  if (!context.customerId) {
    throw new Error(
      'Associate ID (customerId) is required for associate operations'
    );
  }
  if (!context.businessUnitKey) {
    throw new Error('Business Unit key is required for associate operations');
  }

  try {
    if (params.id) {
      return await readApprovalRuleById(
        apiRoot,
        context.projectKey,
        context.customerId,
        context.businessUnitKey,
        params.id,
        params.expand
      );
    }
    if (params.key) {
      return await readApprovalRuleByKey(
        apiRoot,
        context.projectKey,
        context.customerId,
        context.businessUnitKey,
        params.key,
        params.expand
      );
    }
    return await queryApprovalRules(
      apiRoot,
      context.projectKey,
      context.customerId,
      context.businessUnitKey,
      params.where,
      params.limit,
      params.offset,
      params.sort,
      params.expand
    );
  } catch (error: any) {
    throw new SDKError('Failed to read approval rule as associate', error);
  }
};

export const createApprovalRule = async (
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof createApprovalRuleParameters>
) => {
  if (!context.customerId) {
    throw new Error(
      'Associate ID (customerId) is required for associate operations'
    );
  }
  if (!context.businessUnitKey) {
    throw new Error('Business Unit key is required for associate operations');
  }

  try {
    const {associateId: _a, businessUnitKey: _b, ...draft} = params;
    return await createBase(
      apiRoot,
      context.projectKey,
      context.customerId,
      context.businessUnitKey,
      draft as ApprovalRuleDraft
    );
  } catch (error: any) {
    throw new SDKError('Failed to create approval rule as associate', error);
  }
};

export const updateApprovalRule = async (
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof updateApprovalRuleParameters>
) => {
  if (!context.customerId) {
    throw new Error(
      'Associate ID (customerId) is required for associate operations'
    );
  }
  if (!context.businessUnitKey) {
    throw new Error('Business Unit key is required for associate operations');
  }

  try {
    if (params.id) {
      return await updateApprovalRuleById(
        apiRoot,
        context.projectKey,
        context.customerId,
        context.businessUnitKey,
        params.id,
        params.version,
        params.actions as ApprovalRuleUpdateAction[]
      );
    }
    if (params.key) {
      return await updateApprovalRuleByKey(
        apiRoot,
        context.projectKey,
        context.customerId,
        context.businessUnitKey,
        params.key,
        params.version,
        params.actions as ApprovalRuleUpdateAction[]
      );
    }
    throw new Error(
      'Either id or key must be provided to update an approval rule'
    );
  } catch (error: any) {
    throw new SDKError('Failed to update approval rule as associate', error);
  }
};
