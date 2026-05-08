import {z} from 'zod';
import {ApiRoot, RecurrencePolicyDraft, RecurrencePolicyUpdateAction} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
import {
  readRecurrencePolicyById,
  readRecurrencePolicyByKey,
  queryRecurrencePolicies,
  createRecurrencePolicy as createBase,
  updateRecurrencePolicyById,
  updateRecurrencePolicyByKey,
} from './base.functions';
import {
  readRecurrencePolicyParameters,
  createRecurrencePolicyParameters,
  updateRecurrencePolicyParameters,
} from './parameters';

export const readRecurrencePolicy = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof readRecurrencePolicyParameters>
) => {
  try {
    if (params.id) {
      return await readRecurrencePolicyById(apiRoot, context.projectKey, params.id, params.expand);
    }
    if (params.key) {
      return await readRecurrencePolicyByKey(apiRoot, context.projectKey, params.key, params.expand);
    }
    return await queryRecurrencePolicies(
      apiRoot,
      context.projectKey,
      params.where,
      params.limit,
      params.offset,
      params.sort,
      params.expand
    );
  } catch (error: any) {
    throw new SDKError('Failed to read recurrence policy', error);
  }
};

export const createRecurrencePolicy = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof createRecurrencePolicyParameters>
) => {
  try {
    return await createBase(apiRoot, context.projectKey, params as RecurrencePolicyDraft);
  } catch (error: any) {
    throw new SDKError('Failed to create recurrence policy', error);
  }
};

export const updateRecurrencePolicy = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof updateRecurrencePolicyParameters>
) => {
  try {
    if (params.id) {
      return await updateRecurrencePolicyById(
        apiRoot,
        context.projectKey,
        params.id,
        params.version,
        params.actions as RecurrencePolicyUpdateAction[]
      );
    }
    if (params.key) {
      return await updateRecurrencePolicyByKey(
        apiRoot,
        context.projectKey,
        params.key,
        params.version,
        params.actions as RecurrencePolicyUpdateAction[]
      );
    }
    throw new Error('Either id or key must be provided to update a recurrence policy');
  } catch (error: any) {
    throw new SDKError('Failed to update recurrence policy', error);
  }
};
