import {ApiRoot} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import * as admin from './admin.functions';
import * as associate from './associate.functions';

export const contextToAssociateRoleFunctionMapping = (
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
      read_associate_role: associate.readAssociateRole,
    };
  }
  if (context?.isAdmin) {
    return {
      read_associate_role: admin.readAssociateRole,
      create_associate_role: admin.createAssociateRole,
      update_associate_role: admin.updateAssociateRole,
    };
  }
  return {};
};

export const readAssociateRole = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => {
  if (context?.customerId && context?.businessUnitKey) {
    return associate.readAssociateRole(apiRoot, context, params);
  }
  return admin.readAssociateRole(apiRoot, context, params);
};

export const createAssociateRole = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => admin.createAssociateRole(apiRoot, context, params);

export const updateAssociateRole = (
  apiRoot: ApiRoot,
  context: any,
  params: any
) => admin.updateAssociateRole(apiRoot, context, params);
