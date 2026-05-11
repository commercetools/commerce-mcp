import {z} from 'zod';
import {ApiRoot, ApprovalFlowUpdateAction} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
import {CommercetoolsFuncContext} from '../../types/configuration';
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
  context: CommercetoolsFuncContext,
  params: z.infer<typeof readApprovalFlowParameters>
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
      return await readApprovalFlowById(
        apiRoot,
        context.projectKey,
        context.customerId,
        context.businessUnitKey,
        params.id,
        params.expand
      );
    }

    return await queryApprovalFlows(
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
    throw new SDKError('Failed to read approval flow as associate', error);
  }
};

export const updateApprovalFlow = async (
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof updateApprovalFlowParameters>
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
    return await updateApprovalFlowById(
      apiRoot,
      context.projectKey,
      context.customerId,
      context.businessUnitKey,
      params.id,
      params.version,
      params.actions as ApprovalFlowUpdateAction[]
    );
  } catch (error: any) {
    throw new SDKError('Failed to update approval flow as associate', error);
  }
};
