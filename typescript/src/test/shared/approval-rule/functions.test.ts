import {
  readApprovalRule,
  createApprovalRule,
  updateApprovalRule,
} from '../../../shared/approval-rule/functions';
import {contextToApprovalRuleFunctionMapping} from '../../../shared/approval-rule/functions';
import * as adminFunctions from '../../../shared/approval-rule/admin.functions';
import * as associateFunctions from '../../../shared/approval-rule/associate.functions';
import {readApprovalRule as readApprovalRuleAssociate} from '../../../shared/approval-rule/associate.functions';
import {ApiRoot} from '@commercetools/platform-sdk';
import {SDKError} from '../../../shared/errors/sdkError';

const mockExecute = jest.fn();
const mockGet = jest.fn().mockReturnValue({execute: mockExecute});
const mockPost = jest.fn().mockReturnValue({execute: mockExecute});
const mockWithId = jest.fn().mockReturnValue({get: mockGet, post: mockPost});
const mockWithKey = jest.fn().mockReturnValue({get: mockGet, post: mockPost});
const mockApprovalRules = jest.fn().mockReturnValue({
  withId: mockWithId,
  withKey: mockWithKey,
  get: mockGet,
  post: mockPost,
});
const mockInBusinessUnitKeyWithBusinessUnitKeyValue = jest
  .fn()
  .mockReturnValue({
    approvalRules: mockApprovalRules,
  });
const mockWithAssociateIdValue = jest.fn().mockReturnValue({
  inBusinessUnitKeyWithBusinessUnitKeyValue:
    mockInBusinessUnitKeyWithBusinessUnitKeyValue,
});
const mockAsAssociate = jest.fn().mockReturnValue({
  withAssociateIdValue: mockWithAssociateIdValue,
});
const mockWithProjectKey = jest
  .fn()
  .mockReturnValue({asAssociate: mockAsAssociate});

const mockApiRoot = {withProjectKey: mockWithProjectKey} as unknown as ApiRoot;

describe('Approval Rule Functions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('contextToApprovalRuleFunctionMapping', () => {
    it('returns associate functions when customerId and businessUnitKey are present', () => {
      const mapping = contextToApprovalRuleFunctionMapping({
        customerId: 'customer-1',
        businessUnitKey: 'bu-1',
      });
      expect(mapping).toHaveProperty('read_approval_rule');
      expect(mapping).toHaveProperty('create_approval_rule');
      expect(mapping).toHaveProperty('update_approval_rule');
      expect(mapping.read_approval_rule).toBe(
        associateFunctions.readApprovalRule
      );
      expect(mapping.create_approval_rule).toBe(
        associateFunctions.createApprovalRule
      );
      expect(mapping.update_approval_rule).toBe(
        associateFunctions.updateApprovalRule
      );
    });

    it('returns admin functions when isAdmin is true', () => {
      const mapping = contextToApprovalRuleFunctionMapping({isAdmin: true});
      expect(mapping).toHaveProperty('read_approval_rule');
      expect(mapping).toHaveProperty('create_approval_rule');
      expect(mapping).toHaveProperty('update_approval_rule');
      expect(mapping.read_approval_rule).toBe(adminFunctions.readApprovalRule);
      expect(mapping.create_approval_rule).toBe(
        adminFunctions.createApprovalRule
      );
      expect(mapping.update_approval_rule).toBe(
        adminFunctions.updateApprovalRule
      );
    });

    it('returns empty object when context is undefined', () => {
      expect(contextToApprovalRuleFunctionMapping(undefined)).toEqual({});
    });

    it('returns empty object when context has only customerId', () => {
      expect(contextToApprovalRuleFunctionMapping({customerId: 'c1'})).toEqual(
        {}
      );
    });
  });

  describe('readApprovalRule (associate context)', () => {
    const associateContext = {
      projectKey: 'test-project',
      customerId: 'associate-1',
      businessUnitKey: 'bu-key-1',
    };

    it('fetches by ID via associate path', async () => {
      const mockRule = {id: 'rule-1', version: 1};
      mockExecute.mockResolvedValueOnce({body: mockRule});

      const result = await readApprovalRule(mockApiRoot, associateContext, {
        id: 'rule-1',
      });

      expect(mockWithProjectKey).toHaveBeenCalledWith({
        projectKey: 'test-project',
      });
      expect(mockAsAssociate).toHaveBeenCalled();
      expect(mockWithAssociateIdValue).toHaveBeenCalledWith({
        associateId: 'associate-1',
      });
      expect(
        mockInBusinessUnitKeyWithBusinessUnitKeyValue
      ).toHaveBeenCalledWith({
        businessUnitKey: 'bu-key-1',
      });
      expect(mockApprovalRules).toHaveBeenCalled();
      expect(mockWithId).toHaveBeenCalledWith({ID: 'rule-1'});
      expect(result).toEqual(mockRule);
    });

    it('fetches by key via associate path', async () => {
      const mockRule = {id: 'rule-1', version: 1, key: 'high-value'};
      mockExecute.mockResolvedValueOnce({body: mockRule});

      const result = await readApprovalRule(mockApiRoot, associateContext, {
        key: 'high-value',
      });

      expect(mockWithKey).toHaveBeenCalledWith({key: 'high-value'});
      expect(result).toEqual(mockRule);
    });

    it('queries list', async () => {
      const mockResponse = {results: [], count: 0, limit: 10, offset: 0};
      mockExecute.mockResolvedValueOnce({body: mockResponse});

      const result = await readApprovalRule(mockApiRoot, associateContext, {
        where: ['status="Active"'],
        limit: 20,
      });

      expect(mockGet).toHaveBeenCalledWith({
        queryArgs: {where: ['status="Active"'], limit: 20},
      });
      expect(result).toEqual(mockResponse);
    });

    it('throws when customerId is missing from context', async () => {
      await expect(
        readApprovalRuleAssociate(
          mockApiRoot,
          {projectKey: 'test-project', businessUnitKey: 'bu-1'},
          {id: 'rule-1'}
        )
      ).rejects.toThrow('Associate ID (customerId) is required');
    });

    it('throws when businessUnitKey is missing from context', async () => {
      await expect(
        readApprovalRuleAssociate(
          mockApiRoot,
          {projectKey: 'test-project', customerId: 'c1'},
          {id: 'rule-1'}
        )
      ).rejects.toThrow('Business Unit key is required');
    });
  });

  describe('readApprovalRule (admin context)', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('fetches by ID using params for associateId and businessUnitKey', async () => {
      const mockRule = {id: 'rule-2', version: 1};
      mockExecute.mockResolvedValueOnce({body: mockRule});

      const result = await readApprovalRule(mockApiRoot, adminContext, {
        id: 'rule-2',
        customerId: 'admin-associate-1',
        businessUnitKey: 'admin-bu-key',
      });

      expect(mockWithAssociateIdValue).toHaveBeenCalledWith({
        associateId: 'admin-associate-1',
      });
      expect(
        mockInBusinessUnitKeyWithBusinessUnitKeyValue
      ).toHaveBeenCalledWith({
        businessUnitKey: 'admin-bu-key',
      });
      expect(result).toEqual(mockRule);
    });

    it('throws when customerId is missing from params', async () => {
      await expect(
        readApprovalRule(mockApiRoot, adminContext, {businessUnitKey: 'bu-1'})
      ).rejects.toThrow(
        'customerId is required for admin approval rule operations'
      );
    });

    it('throws when businessUnitKey is missing from params', async () => {
      await expect(
        readApprovalRule(mockApiRoot, adminContext, {customerId: 'a-1'})
      ).rejects.toThrow(
        'businessUnitKey is required for admin approval rule operations'
      );
    });
  });

  describe('createApprovalRule (associate context)', () => {
    const associateContext = {
      projectKey: 'test-project',
      customerId: 'associate-1',
      businessUnitKey: 'bu-key-1',
    };

    it('posts the draft to the associate endpoint', async () => {
      const mockCreated = {id: 'rule-3', version: 1};
      mockExecute.mockResolvedValueOnce({body: mockCreated});

      const result = await createApprovalRule(mockApiRoot, associateContext, {
        name: 'High Value Rule',
        predicate: 'totalPrice > "1000 EUR"',
        approvers: {tiers: []},
        requesters: [],
        status: 'Active',
      });

      expect(mockApprovalRules).toHaveBeenCalled();
      expect(mockPost).toHaveBeenCalledWith({
        body: expect.objectContaining({
          name: 'High Value Rule',
          predicate: 'totalPrice > "1000 EUR"',
          status: 'Active',
        }),
      });
      expect(result).toEqual(mockCreated);
    });
  });

  describe('updateApprovalRule (associate context)', () => {
    const associateContext = {
      projectKey: 'test-project',
      customerId: 'associate-1',
      businessUnitKey: 'bu-key-1',
    };

    it('updates by ID — fetches version first then posts', async () => {
      const mockCurrent = {id: 'rule-1', version: 2};
      const mockUpdated = {id: 'rule-1', version: 3};
      mockExecute
        .mockResolvedValueOnce({body: mockCurrent})
        .mockResolvedValueOnce({body: mockUpdated});

      const result = await updateApprovalRule(mockApiRoot, associateContext, {
        id: 'rule-1',
        version: 2,
        actions: [{action: 'setName', name: 'Updated Rule'}],
      });

      expect(mockWithId).toHaveBeenCalledWith({ID: 'rule-1'});
      expect(mockPost).toHaveBeenCalledWith({
        body: {
          version: 2,
          actions: [{action: 'setName', name: 'Updated Rule'}],
        },
      });
      expect(result).toEqual(mockUpdated);
    });
  });

  describe('updateApprovalRule (admin context)', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('updates using params for associateId and businessUnitKey', async () => {
      const mockCurrent = {id: 'rule-2', version: 1};
      const mockUpdated = {id: 'rule-2', version: 2};
      mockExecute
        .mockResolvedValueOnce({body: mockCurrent})
        .mockResolvedValueOnce({body: mockUpdated});

      const result = await updateApprovalRule(mockApiRoot, adminContext, {
        id: 'rule-2',
        version: 1,
        actions: [{action: 'setStatus', status: 'Inactive'}],
        customerId: 'admin-associate-1',
        businessUnitKey: 'admin-bu-key',
      });

      expect(mockWithAssociateIdValue).toHaveBeenCalledWith({
        associateId: 'admin-associate-1',
      });
      expect(mockPost).toHaveBeenCalledWith({
        body: {
          version: 1,
          actions: [{action: 'setStatus', status: 'Inactive'}],
        },
      });
      expect(result).toEqual(mockUpdated);
    });
  });

  describe('SDK error propagation', () => {
    it('wraps SDK errors in SDKError', async () => {
      mockExecute.mockRejectedValueOnce(new Error('Network error'));

      await expect(
        readApprovalRule(
          mockApiRoot,
          {
            projectKey: 'test-project',
            customerId: 'associate-1',
            businessUnitKey: 'bu-1',
          },
          {id: 'rule-1'}
        )
      ).rejects.toThrow(SDKError);
    });
  });
});
