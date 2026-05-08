import {
  ApiRoot,
  RecurrencePolicyDraft,
  RecurrencePolicyUpdateAction,
} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';

export const readRecurrencePolicyById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  id: string,
  expand?: string[]
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .recurrencePolicies()
      .withId({ID: id})
      .get({queryArgs: {...(expand && {expand})}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to read recurrence policy by ID', error);
  }
};

export const readRecurrencePolicyByKey = async (
  apiRoot: ApiRoot,
  projectKey: string,
  key: string,
  expand?: string[]
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .recurrencePolicies()
      .withKey({key})
      .get({queryArgs: {...(expand && {expand})}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to read recurrence policy by key', error);
  }
};

export const queryRecurrencePolicies = async (
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
      .recurrencePolicies()
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
    throw new SDKError('Failed to query recurrence policies', error);
  }
};

export const createRecurrencePolicy = async (
  apiRoot: ApiRoot,
  projectKey: string,
  draft: RecurrencePolicyDraft
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .recurrencePolicies()
      .post({body: draft})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to create recurrence policy', error);
  }
};

export const updateRecurrencePolicyById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  id: string,
  version: number,
  actions: RecurrencePolicyUpdateAction[]
) => {
  try {
    const current = await readRecurrencePolicyById(apiRoot, projectKey, id);
    const response = await apiRoot
      .withProjectKey({projectKey})
      .recurrencePolicies()
      .withId({ID: id})
      .post({body: {version: current.version, actions}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to update recurrence policy by ID', error);
  }
};

export const updateRecurrencePolicyByKey = async (
  apiRoot: ApiRoot,
  projectKey: string,
  key: string,
  version: number,
  actions: RecurrencePolicyUpdateAction[]
) => {
  try {
    const current = await readRecurrencePolicyByKey(apiRoot, projectKey, key);
    const response = await apiRoot
      .withProjectKey({projectKey})
      .recurrencePolicies()
      .withKey({key})
      .post({body: {version: current.version, actions}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to update recurrence policy by key', error);
  }
};
