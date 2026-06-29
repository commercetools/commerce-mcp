import {
  ApiRoot,
  OrderEditDraft,
  OrderEditUpdateAction,
  OrderEditApply,
} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';

export const readOrderEditById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  id: string,
  expand?: string[]
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .orders()
      .edits()
      .withId({ID: id})
      .get({queryArgs: {...(expand && {expand})}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to read order edit by ID', error);
  }
};

export const readOrderEditByKey = async (
  apiRoot: ApiRoot,
  projectKey: string,
  key: string,
  expand?: string[]
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .orders()
      .edits()
      .withKey({key})
      .get({queryArgs: {...(expand && {expand})}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to read order edit by key', error);
  }
};

export const queryOrderEdits = async (
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
      .orders()
      .edits()
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
    throw new SDKError('Failed to query order edits', error);
  }
};

export const createOrderEdit = async (
  apiRoot: ApiRoot,
  projectKey: string,
  draft: OrderEditDraft
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .orders()
      .edits()
      .post({body: draft})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to create order edit', error);
  }
};

export const updateOrderEditById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  id: string,
  version: number,
  actions: OrderEditUpdateAction[],
  dryRun?: boolean
) => {
  try {
    const current = await readOrderEditById(apiRoot, projectKey, id);
    const response = await apiRoot
      .withProjectKey({projectKey})
      .orders()
      .edits()
      .withId({ID: id})
      .post({
        body: {
          version: current.version,
          actions,
          ...(dryRun !== undefined && {dryRun}),
        },
      })
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to update order edit by ID', error);
  }
};

export const updateOrderEditByKey = async (
  apiRoot: ApiRoot,
  projectKey: string,
  key: string,
  version: number,
  actions: OrderEditUpdateAction[],
  dryRun?: boolean
) => {
  try {
    const current = await readOrderEditByKey(apiRoot, projectKey, key);
    const response = await apiRoot
      .withProjectKey({projectKey})
      .orders()
      .edits()
      .withKey({key})
      .post({
        body: {
          version: current.version,
          actions,
          ...(dryRun !== undefined && {dryRun}),
        },
      })
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to update order edit by key', error);
  }
};

export const applyOrderEdit = async (
  apiRoot: ApiRoot,
  projectKey: string,
  id: string,
  editVersion: number,
  resourceVersion: number
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .orders()
      .edits()
      .withId({ID: id})
      .apply()
      .post({
        body: {editVersion, resourceVersion} as OrderEditApply,
      })
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to apply order edit', error);
  }
};
