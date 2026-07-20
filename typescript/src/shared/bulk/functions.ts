import {ApiRoot} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import {bulkCreate, bulkUpdate} from './base.functions';
import {BulkHandler} from '@commercetools/tools-core';

const handler = new BulkHandler();

// Context mapping function for cart functions
export const contextToBulkFunctionMapping = (
  context?: Context
): Record<
  string,
  (
    apiRoot: ApiRoot,
    context: CommercetoolsFuncContext,
    params: any
  ) => Promise<any>
> => {
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('create').name]: bulkCreate,
      [handler.getToolDefinition('update').name]: bulkUpdate,
    };
  }
  return {};
};
