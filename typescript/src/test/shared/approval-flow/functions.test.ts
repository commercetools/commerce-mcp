import {readApprovalFlow, updateApprovalFlow} from '../../../shared/approval-flow/functions';
import {contextToApprovalFlowFunctionMapping} from '../../../shared/approval-flow/functions';
import * as adminFunctions from '../../../shared/approval-flow/admin.functions';
import * as associateFunctions from '../../../shared/approval-flow/associate.functions';
import {ApiRoot} from '@commercetools/platform-sdk';
import {SDKError} from '../../../shared/errors/sdkError';

const mockExecute = jest.fn();
const mockGet = jest.fn().mockReturnValue({execute: mockExecute});
const mockPost = jest.fn().mockReturnValue({execute: mockExecute});
const mockWithId = jest.fn().mockReturnValue({
  get: mockGet,
  post: mockPost,
});
const mockApprovalFlows = jest.fn().mockReturnValue({
  withId: mockWithId,
  get: mockGet,
});
const mockInBusinessUnitKeyWithBusinessUnitKeyValue = jest.fn().mockReturnValue({
  approvalFlows: mockApprovalFlows,
});
const mockWithAssociateIdValue = jest.fn().mockReturnValue({
  inBusinessUnitKeyWithBusinessUnitKeyValue:
    mockInBusinessUnitKeyWithBusinessUnitKeyValue,
});
const mockAsAssociate = jest.fn().mockReturnValue({
  withAssociateIdValue: mockWithAssociateIdValue,
});
const mockWithProjectKey = jest.fn().mockReturnValue({
  asAssociate: mockAsAssociate,
});

const mockApiRoot = {
  withProjectKey: mockWithProjectKey,
} as unknown as ApiRoot;

describe('Approval Flow Functions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('contextToApprovalFlowFunctionMapping', () => {
    it('returns associate functions when customerId and businessUnitKey are present', () => {
      const mapping = contextToApprovalFlowFunctionMapping({
        customerId: 'customer-1',
        businessUnitKey: 'bu-1',
      });
      expect(mapping).toHaveProperty('read_approval_flow');
      expect(mapping).toHaveProperty('update_approval_flow');
      expect(mapping.read_approval_flow).toBe(associateFunctions.readApprovalFlow);
      expect(mapping.update_approval_flow).toBe(
        associateFunctions.updateApprovalFlow
      );
    });

    it('returns admin functions when isAdmin is true', () => {
      const mapping = contextToApprovalFlowFunctionMapping({isAdmin: true});
      expect(mapping).toHaveProperty('read_approval_flow');
      expect(mapping).toHaveProperty('update_approval_flow');
      expect(mapping.read_approval_flow).toBe(adminFunctions.readApprovalFlow);
      expect(mapping.update_approval_flow).toBe(adminFunctions.updateApprovalFlow);
    });

    it('returns empty object when context is undefined', () => {
      expect(contextToApprovalFlowFunctionMapping(undefined)).toEqual({});
    });

    it('returns empty object when context has only customerId (no businessUnitKey)', () => {
      expect(
        contextToApprovalFlowFunctionMapping({customerId: 'customer-1'})
      ).toEqual({});
    });

    it('returns empty object when context has no relevant fields', () => {
      expect(contextToApprovalFlowFunctionMapping({storeKey: 'some-store'})).toEqual(
        {}
      );
    });
  });

  describe('readApprovalFlow (associate context)', () => {
    const associateContext = {
      projectKey: 'test-project',
      customerId: 'associate-1',
      businessUnitKey: 'bu-key-1',
    };

    it('calls the associate approval-flows endpoint with ID', async () => {
      const mockFlow = {id: 'flow-1', version: 1, status: 'Pending'};
      mockExecute.mockResolvedValueOnce({body: mockFlow});

      const result = await readApprovalFlow(mockApiRoot, associateContext, {
        id: 'flow-1',
      });

      expect(mockWithProjectKey).toHaveBeenCalledWith({
        projectKey: 'test-project',
      });
      expect(mockAsAssociate).toHaveBeenCalled();
      expect(mockWithAssociateIdValue).toHaveBeenCalledWith({
        associateId: 'associate-1',
      });
      expect(mockInBusinessUnitKeyWithBusinessUnitKeyValue).toHaveBeenCalledWith({
        businessUnitKey: 'bu-key-1',
      });
      expect(mockApprovalFlows).toHaveBeenCalled();
      expect(mockWithId).toHaveBeenCalledWith({ID: 'flow-1'});
      expect(result).toEqual(mockFlow);
    });

    it('calls the associate approval-flows list endpoint when no ID is given', async () => {
      const mockResponse = {results: [], count: 0, limit: 10, offset: 0};
      mockExecute.mockResolvedValueOnce({body: mockResponse});

      const result = await readApprovalFlow(mockApiRoot, associateContext, {
        where: ['status="Pending"'],
        limit: 20,
      });

      expect(mockApprovalFlows).toHaveBeenCalled();
      expect(mockGet).toHaveBeenCalledWith({
        queryArgs: {
          where: ['status="Pending"'],
          limit: 20,
        },
      });
      expect(result).toEqual(mockResponse);
    });

    it('throws when customerId is missing from context', async () => {
      await expect(
        readApprovalFlow(
          mockApiRoot,
          {projectKey: 'test-project', businessUnitKey: 'bu-1'},
          {}
        )
      ).rejects.toThrow('Associate ID (customerId) is required');
    });

    it('throws when businessUnitKey is missing from context', async () => {
      await expect(
        readApprovalFlow(
          mockApiRoot,
          {projectKey: 'test-project', customerId: 'customer-1'},
          {}
        )
      ).rejects.toThrow('Business Unit key is required');
    });
  });

  describe('readApprovalFlow (admin context)', () => {
    const adminContext = {
      projectKey: 'test-project',
      isAdmin: true,
    };

    it('calls the approval-flows endpoint using params for admin', async () => {
      const mockFlow = {id: 'flow-2', version: 1, status: 'Approved'};
      mockExecute.mockResolvedValueOnce({body: mockFlow});

      const result = await readApprovalFlow(mockApiRoot, adminContext, {
        id: 'flow-2',
        associateId: 'admin-associate-1',
        businessUnitKey: 'admin-bu-key',
      });

      expect(mockWithAssociateIdValue).toHaveBeenCalledWith({
        associateId: 'admin-associate-1',
      });
      expect(mockInBusinessUnitKeyWithBusinessUnitKeyValue).toHaveBeenCalledWith({
        businessUnitKey: 'admin-bu-key',
      });
      expect(result).toEqual(mockFlow);
    });

    it('throws when associateId is missing from params', async () => {
      await expect(
        readApprovalFlow(mockApiRoot, adminContext, {
          businessUnitKey: 'bu-1',
        })
      ).rejects.toThrow('associateId is required for admin approval flow operations');
    });

    it('throws when businessUnitKey is missing from params', async () => {
      await expect(
        readApprovalFlow(mockApiRoot, adminContext, {
          associateId: 'associate-1',
        })
      ).rejects.toThrow(
        'businessUnitKey is required for admin approval flow operations'
      );
    });
  });

  describe('updateApprovalFlow (associate context)', () => {
    const associateContext = {
      projectKey: 'test-project',
      customerId: 'associate-1',
      businessUnitKey: 'bu-key-1',
    };

    it('calls the associate approval-flows POST endpoint', async () => {
      const mockUpdated = {id: 'flow-1', version: 2, status: 'Approved'};
      mockExecute.mockResolvedValueOnce({body: mockUpdated});

      const result = await updateApprovalFlow(mockApiRoot, associateContext, {
        id: 'flow-1',
        version: 1,
        actions: [{action: 'approve'}],
      });

      expect(mockWithId).toHaveBeenCalledWith({ID: 'flow-1'});
      expect(mockPost).toHaveBeenCalledWith({
        body: {
          version: 1,
          actions: [{action: 'approve'}],
        },
      });
      expect(result).toEqual(mockUpdated);
    });
  });

  describe('updateApprovalFlow (admin context)', () => {
    const adminContext = {
      projectKey: 'test-project',
      isAdmin: true,
    };

    it('calls the approval-flows POST endpoint using params for admin', async () => {
      const mockUpdated = {id: 'flow-2', version: 2, status: 'Rejected'};
      mockExecute.mockResolvedValueOnce({body: mockUpdated});

      const result = await updateApprovalFlow(mockApiRoot, adminContext, {
        id: 'flow-2',
        version: 1,
        actions: [{action: 'reject', reason: 'Over budget'}],
        associateId: 'admin-associate-1',
        businessUnitKey: 'admin-bu-key',
      });

      expect(mockWithAssociateIdValue).toHaveBeenCalledWith({
        associateId: 'admin-associate-1',
      });
      expect(mockPost).toHaveBeenCalledWith({
        body: {
          version: 1,
          actions: [{action: 'reject', reason: 'Over budget'}],
        },
      });
      expect(result).toEqual(mockUpdated);
    });
  });

  describe('SDK error propagation', () => {
    it('wraps SDK errors in SDKError for associate read', async () => {
      mockExecute.mockRejectedValueOnce(new Error('Network error'));

      await expect(
        readApprovalFlow(
          mockApiRoot,
          {
            projectKey: 'test-project',
            customerId: 'associate-1',
            businessUnitKey: 'bu-1',
          },
          {id: 'flow-1'}
        )
      ).rejects.toThrow(SDKError);
    });
  });
});
