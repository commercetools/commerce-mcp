import {ApiRoot} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import * as admin from './admin.functions';

export const contextToRecurrencePolicyFunctionMapping = (
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
      read_recurrence_policy: admin.readRecurrencePolicy,
      create_recurrence_policy: admin.createRecurrencePolicy,
      update_recurrence_policy: admin.updateRecurrencePolicy,
    };
  }
  return {};
};

export const readRecurrencePolicy = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => admin.readRecurrencePolicy(apiRoot, context, params);

export const createRecurrencePolicy = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => admin.createRecurrencePolicy(apiRoot, context, params);

export const updateRecurrencePolicy = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => admin.updateRecurrencePolicy(apiRoot, context, params);
