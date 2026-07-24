import * as store from './store.functions';
import * as admin from './admin.functions';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import {ApiRoot} from '@commercetools/platform-sdk';
import {z} from 'zod';
import {
  BusinessUnitsHandler,
  IApiClientFactory,
} from '@commercetools/tools-core';
import {
  readBusinessUnitParameters,
  createBusinessUnitParameters,
  updateBusinessUnitParameters,
} from './parameters';

let handler;

// Context mapping function for business unit functions
export const contextToBusinessUnitFunctionMapping = (
  context?: Context,
  clientFactory?: IApiClientFactory
): Record<
  string,
  (
    apiRoot: ApiRoot,
    context: CommercetoolsFuncContext,
    params: any,
    getApiRoot?: any,
    clientFactory?: IApiClientFactory
  ) => Promise<any>
> => {
  handler = new BusinessUnitsHandler(clientFactory);
  if (context?.storeKey) {
    return {
      [handler.getToolDefinition('read').name]: store.readBusinessUnit,
      [handler.getToolDefinition('create').name]: store.createBusinessUnit,
      [handler.getToolDefinition('update').name]: store.updateBusinessUnit,
    };
  }
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('read').name]: admin.readBusinessUnit,
      [handler.getToolDefinition('create').name]: admin.createBusinessUnit,
      [handler.getToolDefinition('update').name]: admin.updateBusinessUnit,
    };
  }
  return {};
};

// Export the individual CRUD functions for direct use in tests
export const readBusinessUnit = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof readBusinessUnitParameters>
) => {
  if (context?.storeKey) {
    return store.readBusinessUnit(apiRoot, context, params);
  }
  return admin.readBusinessUnit(apiRoot, context, params);
};

export const createBusinessUnit = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof createBusinessUnitParameters>
) => {
  if (context?.storeKey) {
    return store.createBusinessUnit(apiRoot, context, params);
  }
  return admin.createBusinessUnit(apiRoot, context, params);
};

export const updateBusinessUnit = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof updateBusinessUnitParameters>
) => {
  if (context?.storeKey) {
    return store.updateBusinessUnit(apiRoot, context, params);
  }
  return admin.updateBusinessUnit(apiRoot, context, params);
};
