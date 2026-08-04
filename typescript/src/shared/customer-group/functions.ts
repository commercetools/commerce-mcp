import {ApiRoot} from '@commercetools/platform-sdk';
import * as admin from './admin.functions';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import {CustomerGroupUpdateAction} from './base.functions';
import {CustomerGroupsHandler} from '@commercetools/tools-core';

// Re-export the CustomerGroupUpdateAction type for use in tests
export type {CustomerGroupUpdateAction};

const handler = new CustomerGroupsHandler();

export const contextToCustomerGroupFunctionMapping = (
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
      [handler.getToolDefinition('read').name]: admin.readCustomerGroup,
      [handler.getToolDefinition('create').name]: admin.createCustomerGroup,
      [handler.getToolDefinition('update').name]: admin.updateCustomerGroup,
    };
  }

  return {};
};

// Legacy function exports to maintain backward compatibility
export const getCustomerGroup = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  return admin.readCustomerGroup(
    apiRoot,
    {...context, projectKey: context.projectKey},
    params
  );
};

export const createCustomerGroup = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  return admin.createCustomerGroup(
    apiRoot,
    {...context, projectKey: context.projectKey},
    params
  );
};

export const updateCustomerGroup = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  return admin.updateCustomerGroup(
    apiRoot,
    {...context, projectKey: context.projectKey},
    params
  );
};

// These functions are used directly by tests, so we need to export them
export const getCustomerGroupById = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  return admin.readCustomerGroupById(
    apiRoot,
    {...context, projectKey: context.projectKey},
    params
  );
};

export const getCustomerGroupByKey = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  return admin.readCustomerGroupByKey(
    apiRoot,
    {...context, projectKey: context.projectKey},
    params
  );
};

export const queryCustomerGroups = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  return admin.queryCustomerGroups(
    apiRoot,
    {...context, projectKey: context.projectKey},
    params
  );
};

export const updateCustomerGroupById = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  return admin.updateCustomerGroupById(
    apiRoot,
    {...context, projectKey: context.projectKey},
    params
  );
};

export const updateCustomerGroupByKey = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  return admin.updateCustomerGroupByKey(
    apiRoot,
    {...context, projectKey: context.projectKey},
    params
  );
};
