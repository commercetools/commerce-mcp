import {ApiRoot} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import * as admin from './admin.functions';

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
      read_state: admin.readState,
      create_state: admin.createState,
      update_state: admin.updateState,
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
