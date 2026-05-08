import {ApiRoot, AssociateRoleDraft, AssociateRoleUpdateAction} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';

export const readAssociateRoleById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  id: string,
  expand?: string[]
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .associateRoles()
      .withId({ID: id})
      .get({queryArgs: {...(expand && {expand})}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to read associate role by ID', error);
  }
};

export const readAssociateRoleByKey = async (
  apiRoot: ApiRoot,
  projectKey: string,
  key: string,
  expand?: string[]
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .associateRoles()
      .withKey({key})
      .get({queryArgs: {...(expand && {expand})}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to read associate role by key', error);
  }
};

export const queryAssociateRoles = async (
  apiRoot: ApiRoot,
  projectKey: string,
  where?: string[],
  limit?: number,
  offset?: number,
  sort?: string[],
  expand?: string[]
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .associateRoles()
      .get({
        queryArgs: {
          ...(where && {where}),
          limit: limit ?? 10,
          ...(offset !== undefined && {offset}),
          ...(sort && {sort}),
          ...(expand && {expand}),
        },
      })
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to query associate roles', error);
  }
};

export const createAssociateRole = async (
  apiRoot: ApiRoot,
  projectKey: string,
  draft: AssociateRoleDraft
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .associateRoles()
      .post({body: draft})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to create associate role', error);
  }
};

export const updateAssociateRoleById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  id: string,
  version: number,
  actions: AssociateRoleUpdateAction[]
) => {
  try {
    const current = await readAssociateRoleById(apiRoot, projectKey, id);
    const response = await apiRoot
      .withProjectKey({projectKey})
      .associateRoles()
      .withId({ID: id})
      .post({body: {version: current.version, actions}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to update associate role by ID', error);
  }
};

export const updateAssociateRoleByKey = async (
  apiRoot: ApiRoot,
  projectKey: string,
  key: string,
  version: number,
  actions: AssociateRoleUpdateAction[]
) => {
  try {
    const current = await readAssociateRoleByKey(apiRoot, projectKey, key);
    const response = await apiRoot
      .withProjectKey({projectKey})
      .associateRoles()
      .withKey({key})
      .post({body: {version: current.version, actions}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to update associate role by key', error);
  }
};
