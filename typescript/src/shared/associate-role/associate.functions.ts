import {z} from 'zod';
import {ApiRoot} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
import {CommercetoolsFuncContext} from '../../types/configuration';
import {
  readAssociateRoleById,
  readAssociateRoleByKey,
  queryAssociateRoles,
} from './base.functions';
import {readAssociateRoleParameters} from './parameters';

export const readAssociateRole = async (
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
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
    throw new SDKError('Failed to read associate role as associate', error);
  }
};
