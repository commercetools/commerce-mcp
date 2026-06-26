import {ApiRoot} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import * as admin from './admin.functions';
import * as store from './store.functions';

export const contextToProductSelectionAssignmentFunctionMapping = (
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
      read_product_selection_assignments: store.readProductSelectionAssignments,
    };
  }
  if (context?.isAdmin) {
    return {
      read_product_selection_assignments: admin.readProductSelectionAssignments,
    };
  }
  return {};
};

export const readProductSelectionAssignments = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  if (context?.storeKey) {
    return store.readProductSelectionAssignments(apiRoot, context, params);
  }
  return admin.readProductSelectionAssignments(apiRoot, context, params);
};
