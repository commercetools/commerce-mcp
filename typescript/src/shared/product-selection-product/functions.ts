import {ApiRoot} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import * as admin from './admin.functions';
import * as store from './store.functions';

export const contextToProductSelectionProductFunctionMapping = (
  context?: Context
): Record<
  string,
  (
    apiRoot: ApiRoot,
    context: CommercetoolsFuncContext,
    params: any
  ) => Promise<any>
> => {
  if (context?.storeKey) {
    return {
      read_product_selection_product: store.readProductSelectionProduct,
    };
  }
  if (context?.isAdmin) {
    return {
      read_product_selection_product: admin.readProductSelectionProduct,
    };
  }
  return {};
};

export const readProductSelectionProduct = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  if (context?.storeKey) {
    return store.readProductSelectionProduct(apiRoot, context, params);
  }
  return admin.readProductSelectionProduct(apiRoot, context, params);
};
