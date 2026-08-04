import {z} from 'zod';
import {
  readStandalonePriceParameters,
  createStandalonePriceParameters,
  updateStandalonePriceParameters,
} from './parameters';
import {
  ApiRoot,
  StandalonePriceDraft,
  StandalonePriceUpdateAction,
} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import * as admin from './admin.functions';
import {StandalonePricesHandler} from '@commercetools/tools-core';

const handler = new StandalonePricesHandler();

export const contextToStandalonePriceFunctionMapping = (
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
      [handler.getToolDefinition('read').name]: admin.readStandalonePrice,
      [handler.getToolDefinition('create').name]: admin.createStandalonePrice,
      [handler.getToolDefinition('update').name]: admin.updateStandalonePrice,
    };
  }

  return {};
};

// Re-exports for backward compatibility
export const readStandalonePrice = admin.readStandalonePrice;
export const createStandalonePrice = admin.createStandalonePrice;
export const updateStandalonePrice = admin.updateStandalonePrice;
