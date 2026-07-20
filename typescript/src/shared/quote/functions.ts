import * as customer from './customer.functions';
import * as store from './store.functions';
import * as associate from './associate.functions';
import * as admin from './admin.functions';
import {ApiRoot} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import {QuotesHandler} from '@commercetools/tools-core';

const handler = new QuotesHandler();

export const contextToQuoteFunctionMapping = (
  context?: Context
): Record<
  string,
  (
    apiRoot: ApiRoot,
    context: CommercetoolsFuncContext,
    params: any
  ) => Promise<any>
> => {
  if (context?.customerId && context?.businessUnitKey) {
    return {
      [handler.getToolDefinition('read').name]: associate.readQuote,
      [handler.getToolDefinition('update').name]: associate.updateQuote,
    };
  }
  if (context?.customerId) {
    return {
      [handler.getToolDefinition('read').name]: customer.readQuote,
      [handler.getToolDefinition('update').name]: customer.updateQuote,
    };
  }
  if (context?.storeKey) {
    return {
      [handler.getToolDefinition('read').name]: store.readQuote,
      [handler.getToolDefinition('create').name]: store.createQuote,
      [handler.getToolDefinition('update').name]: store.updateQuote,
    };
  }
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('read').name]: admin.readQuote,
      [handler.getToolDefinition('create').name]: admin.createQuote,
      [handler.getToolDefinition('update').name]: admin.updateQuote,
    };
  }
  return {};
};
