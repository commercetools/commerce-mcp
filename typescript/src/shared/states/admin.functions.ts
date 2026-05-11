import {z} from 'zod';
import {
  ApiRoot,
  StateDraft,
  StateUpdateAction,
} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
import {
  readStateById,
  readStateByKey,
  queryStates,
  createState as createBase,
  updateStateById,
  updateStateByKey,
} from './base.functions';
import {
  readStateParameters,
  createStateParameters,
  updateStateParameters,
} from './parameters';

export const readState = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof readStateParameters>
) => {
  try {
    if (params.id) {
      return await readStateById(
        apiRoot,
        context.projectKey,
        params.id,
        params.expand
      );
    }
    if (params.key) {
      return await readStateByKey(
        apiRoot,
        context.projectKey,
        params.key,
        params.expand
      );
    }
    return await queryStates(
      apiRoot,
      context.projectKey,
      params.where,
      params.limit,
      params.offset,
      params.sort,
      params.expand
    );
  } catch (error: any) {
    throw new SDKError('Failed to read state', error);
  }
};

export const createState = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof createStateParameters>
) => {
  try {
    return await createBase(apiRoot, context.projectKey, params as StateDraft);
  } catch (error: any) {
    throw new SDKError('Failed to create state', error);
  }
};

export const updateState = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof updateStateParameters>
) => {
  try {
    if (params.id) {
      return await updateStateById(
        apiRoot,
        context.projectKey,
        params.id,
        params.version,
        params.actions as StateUpdateAction[]
      );
    }
    if (params.key) {
      return await updateStateByKey(
        apiRoot,
        context.projectKey,
        params.key,
        params.version,
        params.actions as StateUpdateAction[]
      );
    }
    throw new Error('Either id or key must be provided to update a state');
  } catch (error: any) {
    throw new SDKError('Failed to update state', error);
  }
};
