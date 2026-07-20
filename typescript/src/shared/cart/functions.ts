import * as customer from './customer.functions';
import * as store from './store.functions';
import * as admin from './admin.functions';
import * as associate from './as-associate.functions';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import {ApiRoot} from '@commercetools/platform-sdk';
import {z} from 'zod';
import {CartsHandler} from '@commercetools/tools-core';
import {
  readCartParameters,
  createCartParameters,
  updateCartParameters,
  replicateCartParameters,
} from './parameters';

const handler = new CartsHandler();

// Context mapping function for cart functions
export const contextToCartFunctionMapping = (
  context?: Context
): Record<
  string,
  (
    apiRoot: ApiRoot,
    context: CommercetoolsFuncContext,
    params: any
  ) => Promise<any>
> => {
  // Associate cart functions when both customerId and businessUnitKey are present
  if (context?.customerId && context?.businessUnitKey) {
    return {
      [handler.getToolDefinition('read').name]: associate.readCart,
      [handler.getToolDefinition('create').name]: associate.createCart,
      [handler.getToolDefinition('update').name]: associate.updateCart,
      [handler.getToolDefinition('replicate').name]: associate.replicateCart,
    };
  }
  if (context?.customerId) {
    return {
      [handler.getToolDefinition('read').name]: customer.readCart,
      [handler.getToolDefinition('create').name]: customer.createCart,
      [handler.getToolDefinition('update').name]: customer.updateCart,
      [handler.getToolDefinition('replicate').name]: customer.replicateCart,
    };
  }
  if (context?.storeKey) {
    return {
      [handler.getToolDefinition('read').name]: store.readCart,
      [handler.getToolDefinition('create').name]: store.createCart,
      [handler.getToolDefinition('update').name]: store.updateCart,
      [handler.getToolDefinition('replicate').name]: store.replicateCart,
    };
  }
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('read').name]: admin.readCart,
      [handler.getToolDefinition('create').name]: admin.createCart,
      [handler.getToolDefinition('update').name]: admin.updateCart,
      [handler.getToolDefinition('replicate').name]: admin.replicateCart,
    };
  }
  return {};
};

// Export the individual CRUD functions for direct use in tests
export const readCart = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof readCartParameters>
) => {
  if (context?.customerId && context?.businessUnitKey) {
    return associate.readCart(apiRoot, context, params);
  }
  if (context?.customerId) {
    return customer.readCart(apiRoot, context, params);
  }
  if (context?.storeKey) {
    return store.readCart(apiRoot, context, params);
  }
  return admin.readCart(apiRoot, context, params);
};

export const createCart = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof createCartParameters>
) => {
  if (context?.customerId && context?.businessUnitKey) {
    return associate.createCart(apiRoot, context, params);
  }
  if (context?.customerId) {
    return customer.createCart(apiRoot, context, params);
  }
  if (context?.storeKey || (params?.store?.key && !context?.customerId)) {
    return store.createCart(apiRoot, context, params);
  }
  return admin.createCart(apiRoot, context, params);
};

export const updateCart = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof updateCartParameters>
) => {
  if (context?.customerId && context?.businessUnitKey) {
    return associate.updateCart(apiRoot, context, params);
  }
  if (context?.customerId) {
    return customer.updateCart(apiRoot, context, params);
  }
  if (context?.storeKey) {
    return store.updateCart(apiRoot, context, params);
  }
  return admin.updateCart(apiRoot, context, params);
};

export const replicateCart = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof replicateCartParameters>
) => {
  if (context?.customerId && context?.businessUnitKey) {
    return associate.replicateCart(apiRoot, context, params);
  }
  if (context?.customerId) {
    return customer.replicateCart(apiRoot, context, params);
  }
  if (context?.storeKey || params?.storeKey) {
    return store.replicateCart(apiRoot, context, params);
  }
  return admin.replicateCart(apiRoot, context, params);
};
