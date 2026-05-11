import {z} from 'zod';
import {ApiRoot, ApprovalFlowUpdateAction} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
import {
  readApprovalFlowById,
  queryApprovalFlows,
  updateApprovalFlowById,
} from './base.functions';
import {
  readApprovalFlowParameters,
  updateApprovalFlowParameters,
} from './parameters';

export const readApprovalFlow = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof readApprovalFlowParameters>
) => {
  if (!params.associateId) {
    throw new Error(
      'associateId is required for admin approval flow operations'
    );
  }
  if (!params.businessUnitKey) {
    throw new Error(
      'businessUnitKey is required for admin approval flow operations'
    );
  }

  try {
    if (params.id) {
      return await readApprovalFlowById(
        apiRoot,
        context.projectKey,
        params.associateId,
        params.businessUnitKey,
        params.id,
        params.expand
      );
    }

    return await queryApprovalFlows(
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
    throw new SDKError('Failed to read approval flow', error);
  }
};

export const updateApprovalFlow = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof updateApprovalFlowParameters>
) => {
  if (!params.associateId) {
    throw new Error(
      'associateId is required for admin approval flow operations'
    );
  }
  if (!params.businessUnitKey) {
    throw new Error(
      'businessUnitKey is required for admin approval flow operations'
    );
  }

  try {
    return await updateApprovalFlowById(
      apiRoot,
      context.projectKey,
      params.associateId,
      params.businessUnitKey,
      params.id,
      params.version,
      params.actions as ApprovalFlowUpdateAction[]
    );
  } catch (error: any) {
    throw new SDKError('Failed to update approval flow', error);
  }
};
