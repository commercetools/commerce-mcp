import {ApiRoot} from '@commercetools/platform-sdk';
import {z} from 'zod';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import * as admin from './admin.functions';
import {
  createCartDiscountParameters,
  readCartDiscountParameters,
  updateCartDiscountParameters,
} from './parameters';
import * as store from './store.functions';
import {CartDiscountsHandler} from '@commercetools/tools-core';

const handler = new CartDiscountsHandler();

// Context mapping function for cart-discount functions
export const contextToCartDiscountFunctionMapping = (
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
      [handler.getToolDefinition('read').name]: store.readCartDiscount,
      [handler.getToolDefinition('create').name]: store.createCartDiscount,
      [handler.getToolDefinition('update').name]: store.updateCartDiscount,
    };
  }
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('read').name]: admin.readCartDiscount,
      [handler.getToolDefinition('create').name]: admin.createCartDiscount,
      [handler.getToolDefinition('update').name]: admin.updateCartDiscount,
    };
  }
  return {};
};

// Export the individual CRUD functions for direct use
export const readCartDiscount = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof readCartDiscountParameters>
) => {
  if (context?.storeKey) {
    return store.readCartDiscount(apiRoot, context, params);
  }
  return admin.readCartDiscount(apiRoot, context, params);
};

export const createCartDiscount = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof createCartDiscountParameters>
) => {
  if (context?.storeKey) {
    return store.createCartDiscount(apiRoot, context, params);
  }
  return admin.createCartDiscount(apiRoot, context, params);
};

export const updateCartDiscount = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof updateCartDiscountParameters>
) => {
  if (context?.storeKey) {
    return store.updateCartDiscount(apiRoot, context, params);
  }
  return admin.updateCartDiscount(apiRoot, context, params);
};
