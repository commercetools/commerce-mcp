import {z} from 'zod';
import {
  readCategoryParameters,
  createCategoryParameters,
  updateCategoryParameters,
} from './parameters';
import {ApiRoot} from '@commercetools/platform-sdk';
import * as admin from './admin.functions';
import * as customer from './customer.functions';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import {CategoriesHandler} from '@commercetools/tools-core';

const handler = new CategoriesHandler();

// Context mapping function for category functions
export const contextToCategoryFunctionMapping = (
  context?: Context
): Record<
  string,
  (
    apiRoot: ApiRoot,
    context: CommercetoolsFuncContext,
    params: any
  ) => Promise<any>
> => {
  if (context?.customerId) {
    return {
      [handler.getToolDefinition('read').name]: customer.readCategory,
    };
  }
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('read').name]: admin.readCategory,
      [handler.getToolDefinition('create').name]: admin.createCategory,
      [handler.getToolDefinition('update').name]: admin.updateCategory,
    };
  }
  return {
    [handler.getToolDefinition('read').name]: customer.readCategory,
  };
};

// Export the individual CRUD functions for direct use
export const readCategory = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof readCategoryParameters>
) => {
  if (context?.customerId) {
    return customer.readCategory(apiRoot, context, params);
  }
  return admin.readCategory(apiRoot, context, params);
};

export const createCategory = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof createCategoryParameters>
) => {
  return admin.createCategory(apiRoot, context, params);
};

export const updateCategory = (
  apiRoot: ApiRoot,
  context: any,
  params: z.infer<typeof updateCategoryParameters>
) => {
  return admin.updateCategory(apiRoot, context, params);
};
