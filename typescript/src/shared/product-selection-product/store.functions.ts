import {z} from 'zod';
import {ApiRoot} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
import {
  queryProductSelectionProductsById,
  queryProductSelectionProductsByKey,
} from './base.functions';
import {readProductSelectionProductParameters} from './parameters';

export const readProductSelectionProduct = async (
  apiRoot: ApiRoot,
  context: {projectKey: string},
  params: z.infer<typeof readProductSelectionProductParameters>
) => {
  if (!params.productSelectionId && !params.productSelectionKey) {
    throw new Error(
      'Either productSelectionId or productSelectionKey must be provided'
    );
  }
  try {
    if (params.productSelectionId) {
      return await queryProductSelectionProductsById(
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
    return await queryProductSelectionProductsByKey(
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
    throw new SDKError('Failed to read product selection products as store', error);
  }
};
