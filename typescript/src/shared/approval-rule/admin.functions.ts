import {z} from 'zod';
import {ApiRoot, ApprovalRuleDraft, ApprovalRuleUpdateAction} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
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
  context: {projectKey: string},
  params: z.infer<typeof readApprovalRuleParameters>
) => {
  if (!params.associateId) {
    throw new Error('associateId is required for admin approval rule operations');
  }
  if (!params.businessUnitKey) {
    throw new Error('businessUnitKey is required for admin approval rule operations');
  }

  try {
    if (params.id) {
      return await readApprovalRuleById(
        apiRoot,
        context.projectKey,
        params.associateId,
        params.businessUnitKey,
        params.id,
        params.expand
      );
    }
    if (params.key) {
      return await readApprovalRuleByKey(
        apiRoot,
        context.projectKey,
        params.associateId,
        params.businessUnitKey,
        params.key,
        params.expand
      );
    }
    return await queryApprovalRules(
      apiRoot,
      context.projectKey,
      params.associateId,
      params.businessUnitKey,
      params.where,
      params.limit,
      params.offset,
      params.sort,
      params.expand
    );
  } catch (error: any) {
    throw new SDKError('Failed to read approval rule', error);
  }
};

export const createApprovalRule = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof createApprovalRuleParameters>
) => {
  if (!params.associateId) {
    throw new Error('associateId is required for admin approval rule operations');
  }
  if (!params.businessUnitKey) {
    throw new Error('businessUnitKey is required for admin approval rule operations');
  }

  try {
    const {associateId, businessUnitKey, ...draft} = params;
    return await createBase(
      apiRoot,
      context.projectKey,
      associateId,
      businessUnitKey,
      draft as ApprovalRuleDraft
    );
  } catch (error: any) {
    throw new SDKError('Failed to create approval rule', error);
  }
};

export const updateApprovalRule = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof updateApprovalRuleParameters>
) => {
  if (!params.associateId) {
    throw new Error('associateId is required for admin approval rule operations');
  }
  if (!params.businessUnitKey) {
    throw new Error('businessUnitKey is required for admin approval rule operations');
  }

  try {
    if (params.id) {
      return await updateApprovalRuleById(
        apiRoot,
        context.projectKey,
        params.associateId,
        params.businessUnitKey,
        params.id,
        params.version,
        params.actions as ApprovalRuleUpdateAction[]
      );
    }
    if (params.key) {
      return await updateApprovalRuleByKey(
        apiRoot,
        context.projectKey,
        params.associateId,
        params.businessUnitKey,
        params.key,
        params.version,
        params.actions as ApprovalRuleUpdateAction[]
      );
    }
    throw new Error('Either id or key must be provided to update an approval rule');
  } catch (error: any) {
    throw new SDKError('Failed to update approval rule', error);
  }
};
