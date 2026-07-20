import {ApiRoot} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import * as admin from './admin.functions';
import {StatesHandler} from '@commercetools/tools-core';

const handler = new StatesHandler();

export const contextToStateFunctionMapping = (
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
      [handler.getToolDefinition('read').name]: admin.readState,
      [handler.getToolDefinition('create').name]: admin.createState,
      [handler.getToolDefinition('update').name]: admin.updateState,
    };
  }
  return {};
};

export const readState = (apiRoot: ApiRoot, context: any, params: any) =>
  admin.readState(apiRoot, context, params);

export const createState = (apiRoot: ApiRoot, context: any, params: any) =>
  admin.createState(apiRoot, context, params);

export const updateState = (apiRoot: ApiRoot, context: any, params: any) =>
  admin.updateState(apiRoot, context, params);
