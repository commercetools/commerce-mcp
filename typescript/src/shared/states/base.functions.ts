import {
  ApiRoot,
  StateDraft,
  StateUpdateAction,
} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';

export const readStateById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  id: string,
  expand?: string[]
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .states()
      .withId({ID: id})
      .get({queryArgs: {...(expand && {expand})}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to read state by ID', error);
  }
};

export const readStateByKey = async (
  apiRoot: ApiRoot,
  projectKey: string,
  key: string,
  expand?: string[]
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .states()
      .withKey({key})
      .get({queryArgs: {...(expand && {expand})}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to read state by key', error);
  }
};

export const queryStates = async (
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
      .states()
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
    throw new SDKError('Failed to query states', error);
  }
};

export const createState = async (
  apiRoot: ApiRoot,
  projectKey: string,
  draft: StateDraft
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .states()
      .post({body: draft})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to create state', error);
  }
};

export const updateStateById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  id: string,
  version: number,
  actions: StateUpdateAction[]
) => {
  try {
    const current = await readStateById(apiRoot, projectKey, id);
    const response = await apiRoot
      .withProjectKey({projectKey})
      .states()
      .withId({ID: id})
      .post({body: {version: current.version, actions}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to update state by ID', error);
  }
};

export const updateStateByKey = async (
  apiRoot: ApiRoot,
  projectKey: string,
  key: string,
  version: number,
  actions: StateUpdateAction[]
) => {
  try {
    const current = await readStateByKey(apiRoot, projectKey, key);
    const response = await apiRoot
      .withProjectKey({projectKey})
      .states()
      .withKey({key})
      .post({body: {version: current.version, actions}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to update state by key', error);
  }
};
