import {z} from 'zod';
import {ApiRoot, AssociateRoleDraft, AssociateRoleUpdateAction} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
import {
  readAssociateRoleById,
  readAssociateRoleByKey,
  queryAssociateRoles,
  createAssociateRole as createBase,
  updateAssociateRoleById,
  updateAssociateRoleByKey,
} from './base.functions';
import {
  readAssociateRoleParameters,
  createAssociateRoleParameters,
  updateAssociateRoleParameters,
} from './parameters';

export const readAssociateRole = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof readAssociateRoleParameters>
) => {
  try {
    if (params.id) {
      return await readAssociateRoleById(apiRoot, context.projectKey, params.id, params.expand);
    }
    if (params.key) {
      return await readAssociateRoleByKey(apiRoot, context.projectKey, params.key, params.expand);
    }
    return await queryAssociateRoles(
      apiRoot,
      context.projectKey,
      params.where,
      params.limit,
      params.offset,
      params.sort,
      params.expand
    );
  } catch (error: any) {
    throw new SDKError('Failed to read associate role', error);
  }
};

export const createAssociateRole = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof createAssociateRoleParameters>
) => {
  try {
    return await createBase(apiRoot, context.projectKey, params as AssociateRoleDraft);
  } catch (error: any) {
    throw new SDKError('Failed to create associate role', error);
  }
};

export const updateAssociateRole = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof updateAssociateRoleParameters>
) => {
  try {
    if (params.id) {
      return await updateAssociateRoleById(
        apiRoot,
        context.projectKey,
        params.id,
        params.version,
        params.actions as AssociateRoleUpdateAction[]
      );
    }
    if (params.key) {
      return await updateAssociateRoleByKey(
        apiRoot,
        context.projectKey,
        params.key,
        params.version,
        params.actions as AssociateRoleUpdateAction[]
      );
    }
    throw new Error('Either id or key must be provided to update an associate role');
  } catch (error: any) {
    throw new SDKError('Failed to update associate role', error);
  }
};
