import {z} from 'zod';
import {
  ApiRoot,
  OrderEditDraft,
  OrderEditUpdateAction,
} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
import {
  readOrderEditById,
  readOrderEditByKey,
  queryOrderEdits,
  createOrderEdit as createBase,
  updateOrderEditById,
  updateOrderEditByKey,
  applyOrderEdit as applyBase,
} from './base.functions';
import {
  readOrderEditParameters,
  createOrderEditParameters,
  updateOrderEditParameters,
  applyOrderEditParameters,
} from './parameters';

export const readOrderEdit = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof readOrderEditParameters>
) => {
  try {
    if (params.id) {
      return await readOrderEditById(
        apiRoot,
        context.projectKey,
        params.id,
        params.expand
      );
    }
    if (params.key) {
      return await readOrderEditByKey(
        apiRoot,
        context.projectKey,
        params.key,
        params.expand
      );
    }
    return await queryOrderEdits(
      apiRoot,
      context.projectKey,
      params.where,
      params.limit,
      params.offset,
      params.sort,
      params.expand
    );
  } catch (error: any) {
    throw new SDKError('Failed to read order edit', error);
  }
};

export const createOrderEdit = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof createOrderEditParameters>
) => {
  try {
    return await createBase(
      apiRoot,
      context.projectKey,
      params as OrderEditDraft
    );
  } catch (error: any) {
    throw new SDKError('Failed to create order edit', error);
  }
};

export const updateOrderEdit = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof updateOrderEditParameters>
) => {
  try {
    if (params.id) {
      return await updateOrderEditById(
        apiRoot,
        context.projectKey,
        params.id,
        params.version,
        params.actions as OrderEditUpdateAction[],
        params.dryRun
      );
    }
    if (params.key) {
      return await updateOrderEditByKey(
        apiRoot,
        context.projectKey,
        params.key,
        params.version,
        params.actions as OrderEditUpdateAction[],
        params.dryRun
      );
    }
    throw new Error(
      'Either id or key must be provided to update an order edit'
    );
  } catch (error: any) {
    throw new SDKError('Failed to update order edit', error);
  }
};

export const applyOrderEdit = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof applyOrderEditParameters>
) => {
  try {
    return await applyBase(
      apiRoot,
      context.projectKey,
      params.id,
      params.editVersion,
      params.resourceVersion
    );
  } catch (error: any) {
    throw new SDKError('Failed to apply order edit', error);
  }
};
