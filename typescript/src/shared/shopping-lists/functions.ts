/* eslint-disable require-await */
import {ApiRoot} from '@commercetools/platform-sdk';
import {z} from 'zod';
import {
  createShoppingListParameters,
  readShoppingListParameters,
  updateShoppingListParameters,
} from './parameters';
import * as admin from './admin.functions';
import * as customer from './customer.functions';
import * as store from './store.functions';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import {ShoppingListsHandler} from '@commercetools/tools-core';

const handler = new ShoppingListsHandler();

export const contextToShoppingListFunctionMapping = (
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
      [handler.getToolDefinition('read').name]: customer.readShoppingList,
      [handler.getToolDefinition('create').name]: customer.createShoppingList,
      [handler.getToolDefinition('update').name]: customer.updateShoppingList,
    };
  }
  if (context?.storeKey) {
    return {
      [handler.getToolDefinition('read').name]: store.readShoppingList,
      [handler.getToolDefinition('create').name]: store.createShoppingList,
      [handler.getToolDefinition('update').name]: store.updateShoppingList,
    };
  }
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('read').name]: admin.readShoppingList,
      [handler.getToolDefinition('create').name]: admin.createShoppingList,
      [handler.getToolDefinition('update').name]: admin.updateShoppingList,
    };
  }

  return {};
};

/**
 * Reads shopping lists based on provided parameters:
 * - If 'id' is provided, retrieves a specific shopping list by ID
 * - If 'key' is provided, retrieves a specific shopping list by key
 * - If neither is provided, lists shopping lists with optional filtering, sorting, and pagination
 */
export async function readShoppingList(
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof readShoppingListParameters>
) {
  return admin.readShoppingList(apiRoot, context, params);
}

/**
 * Creates a new shopping list in the commercetools platform
 */
export async function createShoppingList(
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof createShoppingListParameters>
) {
  return admin.createShoppingList(apiRoot, context, params);
}

/**
 * Updates an existing shopping list in the commercetools platform
 */
export async function updateShoppingList(
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof updateShoppingListParameters>
) {
  return admin.updateShoppingList(apiRoot, context, params);
}
