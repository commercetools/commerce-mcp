import {ApiRoot} from '@commercetools/platform-sdk';
import {z} from 'zod';
import {
  createSubscriptionParameters,
  readSubscriptionParameters,
  updateSubscriptionParameters,
} from './parameters';
import * as admin from './admin.functions';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import {SubscriptionsHandler} from '@commercetools/tools-core';

const handler = new SubscriptionsHandler();

export const contextToSubscriptionFunctionMapping = (
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
      [handler.getToolDefinition('read').name]: admin.readSubscription,
      [handler.getToolDefinition('create').name]: admin.createSubscription,
      [handler.getToolDefinition('update').name]: admin.updateSubscription,
    };
  }

  return {};
};

/**
 * Reads subscriptions based on provided parameters:
 * - If 'id' is provided, retrieves a specific subscription by ID
 * - If 'key' is provided, retrieves a specific subscription by key
 * - If neither 'id' nor 'key' is provided, lists subscriptions with optional filtering
 */
export function readSubscription(
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof readSubscriptionParameters>
) {
  return admin.readSubscription(apiRoot, context, params);
}

/**
 * Creates a new subscription
 */
export function createSubscription(
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof createSubscriptionParameters>
) {
  return admin.createSubscription(apiRoot, context, params);
}

/**
 * Updates a subscription based on provided parameters:
 * - If 'id' is provided, updates the subscription by ID
 * - If 'key' is provided, updates the subscription by key
 * - One of either 'id' or 'key' must be provided
 */
export function updateSubscription(
  apiRoot: ApiRoot,
  context: CommercetoolsFuncContext,
  params: z.infer<typeof updateSubscriptionParameters>
) {
  return admin.updateSubscription(apiRoot, context, params);
}
