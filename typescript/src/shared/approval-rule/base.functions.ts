import {ApiRoot, ApprovalRuleDraft, ApprovalRuleUpdateAction} from '@commercetools/platform-sdk';
import {SDKError} from '../errors/sdkError';

const getApprovalRulesBuilder = (
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
    .approvalRules();

export const readApprovalRuleById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  associateId: string,
  businessUnitKey: string,
  id: string,
  expand?: string[]
) => {
  try {
    const response = await getApprovalRulesBuilder(
      apiRoot,
      projectKey,
      associateId,
      businessUnitKey
    )
      .withId({ID: id})
      .get({queryArgs: {...(expand && {expand})}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to read approval rule by ID', error);
  }
};

export const readApprovalRuleByKey = async (
  apiRoot: ApiRoot,
  projectKey: string,
  associateId: string,
  businessUnitKey: string,
  key: string,
  expand?: string[]
) => {
  try {
    const response = await getApprovalRulesBuilder(
      apiRoot,
      projectKey,
      associateId,
      businessUnitKey
    )
      .withKey({key})
      .get({queryArgs: {...(expand && {expand})}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to read approval rule by key', error);
  }
};

export const queryApprovalRules = async (
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
    const response = await getApprovalRulesBuilder(
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
    throw new SDKError('Failed to query approval rules', error);
  }
};

export const createApprovalRule = async (
  apiRoot: ApiRoot,
  projectKey: string,
  associateId: string,
  businessUnitKey: string,
  draft: ApprovalRuleDraft
) => {
  try {
    const response = await getApprovalRulesBuilder(
      apiRoot,
      projectKey,
      associateId,
      businessUnitKey
    )
      .post({body: draft})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to create approval rule', error);
  }
};

export const updateApprovalRuleById = async (
  apiRoot: ApiRoot,
  projectKey: string,
  associateId: string,
  businessUnitKey: string,
  id: string,
  version: number,
  actions: ApprovalRuleUpdateAction[]
) => {
  try {
    const current = await readApprovalRuleById(
      apiRoot,
      projectKey,
      associateId,
      businessUnitKey,
      id
    );
    const response = await getApprovalRulesBuilder(
      apiRoot,
      projectKey,
      associateId,
      businessUnitKey
    )
      .withId({ID: id})
      .post({body: {version: current.version, actions}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to update approval rule by ID', error);
  }
};

export const updateApprovalRuleByKey = async (
  apiRoot: ApiRoot,
  projectKey: string,
  associateId: string,
  businessUnitKey: string,
  key: string,
  version: number,
  actions: ApprovalRuleUpdateAction[]
) => {
  try {
    const current = await readApprovalRuleByKey(
      apiRoot,
      projectKey,
      associateId,
      businessUnitKey,
      key
    );
    const response = await getApprovalRulesBuilder(
      apiRoot,
      projectKey,
      associateId,
      businessUnitKey
    )
      .withKey({key})
      .post({body: {version: current.version, actions}})
      .execute();
    return response.body;
  } catch (error: any) {
    throw new SDKError('Failed to update approval rule by key', error);
  }
};
