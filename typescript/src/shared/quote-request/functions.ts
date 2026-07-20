import * as customer from './customer.functions';
import * as store from './store.functions';
import * as admin from './admin.functions';
import * as associate from './associate.functions';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import {ApiRoot} from '@commercetools/platform-sdk';
import {z} from 'zod';
import {
  readQuoteRequestParameters,
  createQuoteRequestParameters,
  updateQuoteRequestParameters,
} from './parameters';
import {QuoteRequestsHandler} from '@commercetools/tools-core';

const handler = new QuoteRequestsHandler();

// Context mapping function for quote request functions
export const contextToQuoteRequestFunctionMapping = (
  context?: Context
): Record<
  string,
  (
    apiRoot: ApiRoot,
    context: CommercetoolsFuncContext,
    params: any
  ) => Promise<any>
> => {
  // Associate operations (when both customerId and businessUnitKey are present)
  if (context?.customerId && context?.businessUnitKey) {
    return {
      [handler.getToolDefinition('read').name]: associate.readQuoteRequest,
      [handler.getToolDefinition('create').name]: associate.createQuoteRequest,
      [handler.getToolDefinition('update').name]: associate.updateQuoteRequest,
    };
  }
  if (context?.customerId) {
    return {
      [handler.getToolDefinition('read').name]: customer.readQuoteRequest,
      [handler.getToolDefinition('update').name]: customer.updateQuoteRequest,
    };
  }
  if (context?.storeKey) {
    return {
      [handler.getToolDefinition('read').name]: store.readQuoteRequest,
      [handler.getToolDefinition('create').name]: store.createQuoteRequest,
      [handler.getToolDefinition('update').name]: store.updateQuoteRequest,
    };
  }
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('read').name]: admin.readQuoteRequest,
      [handler.getToolDefinition('create').name]: admin.createQuoteRequest,
      [handler.getToolDefinition('update').name]: admin.updateQuoteRequest,
    };
  }
  return {};
};

// Export the individual CRUD functions for direct use in tests
export const readQuoteRequest = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof readQuoteRequestParameters>
) => {
  // Associate operations (when both customerId and businessUnitKey are present)
  if (context?.customerId && context?.businessUnitKey) {
    return associate.readQuoteRequest(apiRoot, context, params);
  }
  if (context?.customerId) {
    return customer.readQuoteRequest(apiRoot, context, params);
  }
  if (context?.storeKey) {
    return store.readQuoteRequest(apiRoot, context, params);
  }
  return admin.readQuoteRequest(apiRoot, context, params);
};

export const createQuoteRequest = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof createQuoteRequestParameters>
) => {
  // Associate operations (when both customerId and businessUnitKey are present)
  if (context?.customerId && context?.businessUnitKey) {
    return associate.createQuoteRequest(apiRoot, context, params);
  }
  if (context?.storeKey) {
    return store.createQuoteRequest(apiRoot, context, params);
  }
  return admin.createQuoteRequest(apiRoot, context, params);
};

export const updateQuoteRequest = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof updateQuoteRequestParameters>
) => {
  // Associate operations (when both customerId and businessUnitKey are present)
  if (context?.customerId && context?.businessUnitKey) {
    return associate.updateQuoteRequest(apiRoot, context, params);
  }
  if (context?.customerId) {
    return customer.updateQuoteRequest(apiRoot, context, params);
  }
  if (context?.storeKey) {
    return store.updateQuoteRequest(apiRoot, context, params);
  }
  return admin.updateQuoteRequest(apiRoot, context, params);
};
