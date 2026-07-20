import {z} from 'zod';
import {
  listProductsParameters,
  createProductParameters,
  updateProductParameters,
} from './parameters';
import {ApiRoot} from '@commercetools/platform-sdk';
import {Context, CommercetoolsFuncContext} from '../../types/configuration';
import * as admin from './admin.functions';
import {ProductsHandler} from '@commercetools/tools-core';

const handler = new ProductsHandler();

/**
 * Maps context to product functions
 */
export const contextToProductFunctionMapping = (
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
      [handler.getToolDefinition('read').name]: admin.listProducts,
      [handler.getToolDefinition('create').name]: admin.createProduct,
      [handler.getToolDefinition('update').name]: admin.updateProduct,
    };
  }
  return {
    [handler.getToolDefinition('read').name]: admin.listProducts,
  };
};

export const listProducts = (
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof listProductsParameters>
) => {
  return admin.listProducts(apiRoot, context, params);
};

export const createProduct = (
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof createProductParameters>
) => {
  return admin.createProduct(apiRoot, context, params);
};

export const updateProduct = (
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof updateProductParameters>
) => {
  return admin.updateProduct(apiRoot, context, params);
};
