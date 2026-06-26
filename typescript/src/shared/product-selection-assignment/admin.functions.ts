import {z} from 'zod';
import {ApiRoot} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
import {
  queryProductSelectionAssignmentsById,
  queryProductSelectionAssignmentsByKey,
} from './base.functions';
import {readProductSelectionAssignmentsParameters} from './parameters';

export const readProductSelectionAssignments = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof readProductSelectionAssignmentsParameters>
) => {
  if (!params.productSelectionId && !params.productSelectionKey) {
    throw new Error(
      'Either productSelectionId or productSelectionKey must be provided'
    );
  }
  try {
    if (params.productSelectionId) {
      return await queryProductSelectionAssignmentsById(
        apiRoot,
        context.projectKey,
        params.productSelectionId,
        params.where,
        params.limit,
        params.offset,
        params.sort,
        params.expand
      );
    }
    return await queryProductSelectionAssignmentsByKey(
      apiRoot,
      context.projectKey,
      params.productSelectionKey!,
      params.where,
      params.limit,
      params.offset,
      params.sort,
      params.expand
    );
  } catch (error: any) {
    throw new SDKError('Failed to read product selection assignments', error);
  }
};
