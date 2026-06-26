import {ApiRoot} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';

export const queryProductSelectionAssignmentsById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  productSelectionId: string,
  where?: string[],
  limit?: number,
  offset?: number,
  sort?: string[],
  expand?: string[]
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .productSelections()
      .withId({ID: productSelectionId})
      .products()
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
    throw new SDKError(
      'Failed to query product selection assignments by ID',
      error
    );
  }
};

export const queryProductSelectionAssignmentsByKey = async (
  apiRoot: ApiRoot,
  projectKey: string,
  productSelectionKey: string,
  where?: string[],
  limit?: number,
  offset?: number,
  sort?: string[],
  expand?: string[]
) => {
  try {
    const response = await apiRoot
      .withProjectKey({projectKey})
      .productSelections()
      .withKey({key: productSelectionKey})
      .products()
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
    throw new SDKError(
      'Failed to query product selection assignments by key',
      error
    );
  }
};
