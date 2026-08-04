import * as store from './store.functions';
import * as admin from './admin.functions';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import {ApiRoot} from '@commercetools/platform-sdk';
import {z} from 'zod';
import {
  readStagedQuoteParameters,
  createStagedQuoteParameters,
  updateStagedQuoteParameters,
} from './parameters';
import {StagedQuotesHandler} from '@commercetools/tools-core';

const handler = new StagedQuotesHandler();

// Context mapping function for staged quote functions
export const contextToStagedQuoteFunctionMapping = (
  context?: Context
): Record<
  string,
  (
    apiRoot: ApiRoot,
    context: CommercetoolsFuncContext,
    params: any
  ) => Promise<any>
> => {
  if (context?.storeKey) {
    return {
      [handler.getToolDefinition('read').name]: store.readStagedQuote,
      [handler.getToolDefinition('create').name]: store.createStagedQuote,
      [handler.getToolDefinition('update').name]: store.updateStagedQuote,
    };
  }
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('read').name]: admin.readStagedQuote,
      [handler.getToolDefinition('create').name]: admin.createStagedQuote,
      [handler.getToolDefinition('update').name]: admin.updateStagedQuote,
    };
  }
  return {};
};

// Export the individual CRUD functions for direct use in tests
export const readStagedQuote = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof readStagedQuoteParameters>
) => {
  if (context?.storeKey) {
    return store.readStagedQuote(apiRoot, context, params);
  }
  return admin.readStagedQuote(apiRoot, context, params);
};

export const createStagedQuote = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof createStagedQuoteParameters>
) => {
  if (context?.storeKey) {
    return store.createStagedQuote(apiRoot, context, params);
  }
  return admin.createStagedQuote(apiRoot, context, params);
};

export const updateStagedQuote = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof updateStagedQuoteParameters>
) => {
  if (context?.storeKey) {
    return store.updateStagedQuote(apiRoot, context, params);
  }
  return admin.updateStagedQuote(apiRoot, context, params);
};
