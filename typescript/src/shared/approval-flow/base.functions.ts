import {ApiRoot, ApprovalFlowUpdateAction} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';

const getApprovalFlowsBuilder = (
  apiRoot: ApiRoot,
  projectKey: string,
  associateId: string,
  businessUnitKey: string
) =>
  apiRoot
    .withProjectKey({projectKey})
    .asAssociate()
    .withAssociateIdValue({associateId})
    .inBusinessUnitKeyWithBusinessUnitKeyValue({businessUnitKey})
    .approvalFlows();

export const readApprovalFlowById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  associateId: string,
  businessUnitKey: string,
  id: string,
  expand?: string[]
) => {
  try {
    const response = await getApprovalFlowsBuilder(
      apiRoot,
      projectKey,
      associateId,
      businessUnitKey
    )
      .withId({ID: id})
      .get({
        queryArgs: {
          ...(expand && {expand}),
        },
      })
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to read approval flow by ID', error);
  }
};

export const queryApprovalFlows = async (
  apiRoot: ApiRoot,
  projectKey: string,
  associateId: string,
  businessUnitKey: string,
  where?: string[],
  limit?: number,
  offset?: number,
  sort?: string[],
  expand?: string[]
) => {
  try {
    const response = await getApprovalFlowsBuilder(
      apiRoot,
      projectKey,
      associateId,
      businessUnitKey
    )
      .get({
        queryArgs: {
          ...(where && {where}),
          limit: limit ?? 10,
          ...(offset !== undefined && {offset}),
          ...(sort && {sort}),
          ...(expand && {expand}),
        },
      })
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to query approval flows', error);
  }
};

export const updateApprovalFlowById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  associateId: string,
  businessUnitKey: string,
  id: string,
  version: number,
  actions: ApprovalFlowUpdateAction[]
) => {
  try {
    const response = await getApprovalFlowsBuilder(
      apiRoot,
      projectKey,
      associateId,
      businessUnitKey
    )
      .withId({ID: id})
      .post({
        body: {
          version,
          actions,
        },
      })
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to update approval flow by ID', error);
  }
};
