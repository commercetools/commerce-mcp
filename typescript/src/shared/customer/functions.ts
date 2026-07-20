import {ApiRoot} from '@commercetools/platform-sdk';
import {Context, CommercetoolsFuncContext} from '../../types/configuration';
import * as admin from './admin.functions';
import * as customer from './customer.functions';
import * as store from './store.functions';
import {CustomersHandler} from '@commercetools/tools-core';

const handler = new CustomersHandler();

// Context-to-function mapping
export const contextToCustomerFunctionMapping = (
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
      [handler.getToolDefinition('read').name]: customer.readCustomerProfile,
    };
  }
  if (context?.storeKey) {
    return {
      [handler.getToolDefinition('read').name]: store.readCustomerInStore,
      [handler.getToolDefinition('create').name]: store.createCustomerInStore,
      [handler.getToolDefinition('update').name]: store.updateCustomerInStore,
    };
  }
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('read').name]: admin.readCustomer,
      [handler.getToolDefinition('create').name]: admin.createCustomerAsAdmin,
      [handler.getToolDefinition('update').name]: admin.updateCustomerAsAdmin,
    };
  }
  return {};
};

// Re-export functions from admin for backward compatibility
export const createCustomer = admin.createCustomerAsAdmin;
export const getCustomerById = admin.readCustomer;
export const updateCustomer = admin.updateCustomerAsAdmin;
