import * as store from './store.functions';
import * as admin from './admin.functions';
import {Context, CommercetoolsFuncContext} from '../../types/configuration';
import {ApiRoot} from '@commercetools/platform-sdk';
import {z} from 'zod';
import {
  readStoreParameters,
  createStoreParameters,
  updateStoreParameters,
} from './parameters';
import {StoresHandler} from '@commercetools/tools-core';

const handler = new StoresHandler();

export const contextToStoreFunctionMapping = (
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
      [handler.getToolDefinition('read').name]: store.readStore,
      [handler.getToolDefinition('update').name]: store.updateStore,
    };
  }
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('read').name]: admin.readStore,
      [handler.getToolDefinition('create').name]: admin.createStore,
      [handler.getToolDefinition('update').name]: admin.updateStore,
    };
  }
  return {};
};

// Export the individual CRUD functions for direct use in tests
export const readStore = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof readStoreParameters>
) => {
  if (context?.storeKey) {
    return store.readStore(apiRoot, context, params);
  }
  return admin.readStore(apiRoot, context, params);
};

export const createStore = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof createStoreParameters>
) => {
  return admin.createStore(apiRoot, context, params);
};

export const updateStore = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof updateStoreParameters>
) => {
  return admin.updateStore(apiRoot, context, params);
};
