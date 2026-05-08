import {ApiRoot} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import * as admin from './admin.functions';

export const contextToOrderEditFunctionMapping = (
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
      read_order_edit: admin.readOrderEdit,
      create_order_edit: admin.createOrderEdit,
      update_order_edit: admin.updateOrderEdit,
      apply_order_edit: admin.applyOrderEdit,
    };
  }
  return {};
};

export const readOrderEdit = (apiRoot: ApiRoot, context: any, params: any) =>
  admin.readOrderEdit(apiRoot, context, params);

export const createOrderEdit = (apiRoot: ApiRoot, context: any, params: any) =>
  admin.createOrderEdit(apiRoot, context, params);

export const updateOrderEdit = (apiRoot: ApiRoot, context: any, params: any) =>
  admin.updateOrderEdit(apiRoot, context, params);

export const applyOrderEdit = (apiRoot: ApiRoot, context: any, params: any) =>
  admin.applyOrderEdit(apiRoot, context, params);
