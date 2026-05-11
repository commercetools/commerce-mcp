import {
  readAssociateRole,
  createAssociateRole,
  updateAssociateRole,
} from '../../../shared/associate-role/functions';
import {contextToAssociateRoleFunctionMapping} from '../../../shared/associate-role/functions';
import * as adminFunctions from '../../../shared/associate-role/admin.functions';
import * as associateFunctions from '../../../shared/associate-role/associate.functions';
import {ApiRoot} from '@commercetools/platform-sdk';
import {SDKError} from '../../../shared/errors/sdkError';

const mockExecute = jest.fn();
const mockGet = jest.fn().mockReturnValue({execute: mockExecute});
const mockPost = jest.fn().mockReturnValue({execute: mockExecute});
const mockWithId = jest.fn().mockReturnValue({get: mockGet, post: mockPost});
const mockWithKey = jest.fn().mockReturnValue({get: mockGet, post: mockPost});
const mockAssociateRoles = jest.fn().mockReturnValue({
  withId: mockWithId,
  withKey: mockWithKey,
  get: mockGet,
  post: mockPost,
});
const mockWithProjectKey = jest
  .fn()
  .mockReturnValue({associateRoles: mockAssociateRoles});

const mockApiRoot = {withProjectKey: mockWithProjectKey} as unknown as ApiRoot;

describe('Associate Role Functions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('contextToAssociateRoleFunctionMapping', () => {
    it('returns only read function for associate context', () => {
      const mapping = contextToAssociateRoleFunctionMapping({
        customerId: 'customer-1',
        businessUnitKey: 'bu-1',
      });
      expect(mapping).toHaveProperty('read_associate_role');
      expect(mapping).not.toHaveProperty('create_associate_role');
      expect(mapping).not.toHaveProperty('update_associate_role');
      expect(mapping.read_associate_role).toBe(
        associateFunctions.readAssociateRole
      );
    });

    it('returns all functions for admin context', () => {
      const mapping = contextToAssociateRoleFunctionMapping({isAdmin: true});
      expect(mapping).toHaveProperty('read_associate_role');
      expect(mapping).toHaveProperty('create_associate_role');
      expect(mapping).toHaveProperty('update_associate_role');
      expect(mapping.read_associate_role).toBe(
        adminFunctions.readAssociateRole
      );
      expect(mapping.create_associate_role).toBe(
        adminFunctions.createAssociateRole
      );
      expect(mapping.update_associate_role).toBe(
        adminFunctions.updateAssociateRole
      );
    });

    it('returns empty object when context is undefined', () => {
      expect(contextToAssociateRoleFunctionMapping(undefined)).toEqual({});
    });

    it('returns empty object when context has only customerId', () => {
      expect(contextToAssociateRoleFunctionMapping({customerId: 'c1'})).toEqual(
        {}
      );
    });
  });

  describe('readAssociateRole (admin context)', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('fetches by ID', async () => {
      const mockRole = {id: 'role-1', version: 1, key: 'buyer'};
      mockExecute.mockResolvedValueOnce({body: mockRole});

      const result = await readAssociateRole(mockApiRoot, adminContext, {
        id: 'role-1',
      });

      expect(mockWithProjectKey).toHaveBeenCalledWith({
        projectKey: 'test-project',
      });
      expect(mockAssociateRoles).toHaveBeenCalled();
      expect(mockWithId).toHaveBeenCalledWith({ID: 'role-1'});
      expect(result).toEqual(mockRole);
    });

    it('fetches by key', async () => {
      const mockRole = {id: 'role-1', version: 1, key: 'buyer'};
      mockExecute.mockResolvedValueOnce({body: mockRole});

      const result = await readAssociateRole(mockApiRoot, adminContext, {
        key: 'buyer',
      });

      expect(mockWithKey).toHaveBeenCalledWith({key: 'buyer'});
      expect(result).toEqual(mockRole);
    });

    it('queries list', async () => {
      const mockResponse = {results: [], count: 0, limit: 10, offset: 0};
      mockExecute.mockResolvedValueOnce({body: mockResponse});

      const result = await readAssociateRole(mockApiRoot, adminContext, {
        limit: 5,
      });

      expect(mockGet).toHaveBeenCalledWith({queryArgs: {limit: 5}});
      expect(result).toEqual(mockResponse);
    });
  });

  describe('readAssociateRole (associate context)', () => {
    const associateContext = {
      projectKey: 'test-project',
      customerId: 'associate-1',
      businessUnitKey: 'bu-key-1',
    };

    it('fetches by ID via the same admin SDK path', async () => {
      const mockRole = {id: 'role-1', version: 1, key: 'buyer'};
      mockExecute.mockResolvedValueOnce({body: mockRole});

      const result = await readAssociateRole(mockApiRoot, associateContext, {
        id: 'role-1',
      });

      expect(mockAssociateRoles).toHaveBeenCalled();
      expect(mockWithId).toHaveBeenCalledWith({ID: 'role-1'});
      expect(result).toEqual(mockRole);
    });
  });

  describe('createAssociateRole', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('posts the draft to the endpoint', async () => {
      const mockCreated = {id: 'role-2', version: 1, key: 'manager'};
      mockExecute.mockResolvedValueOnce({body: mockCreated});

      const result = await createAssociateRole(mockApiRoot, adminContext, {
        key: 'manager',
        buyerAssignable: false,
        name: 'Manager',
      });

      expect(mockPost).toHaveBeenCalledWith({
        body: {key: 'manager', buyerAssignable: false, name: 'Manager'},
      });
      expect(result).toEqual(mockCreated);
    });
  });

  describe('updateAssociateRole', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('updates by ID — fetches version first then posts', async () => {
      const mockCurrent = {id: 'role-1', version: 1};
      const mockUpdated = {id: 'role-1', version: 2};
      mockExecute
        .mockResolvedValueOnce({body: mockCurrent})
        .mockResolvedValueOnce({body: mockUpdated});

      const result = await updateAssociateRole(mockApiRoot, adminContext, {
        id: 'role-1',
        version: 1,
        actions: [{action: 'setName', name: 'Senior Manager'}],
      });

      expect(mockWithId).toHaveBeenCalledWith({ID: 'role-1'});
      expect(mockPost).toHaveBeenCalledWith({
        body: {
          version: 1,
          actions: [{action: 'setName', name: 'Senior Manager'}],
        },
      });
      expect(result).toEqual(mockUpdated);
    });

    it('updates by key — fetches version first then posts', async () => {
      const mockCurrent = {id: 'role-1', version: 2, key: 'buyer'};
      const mockUpdated = {id: 'role-1', version: 3, key: 'buyer'};
      mockExecute
        .mockResolvedValueOnce({body: mockCurrent})
        .mockResolvedValueOnce({body: mockUpdated});

      const result = await updateAssociateRole(mockApiRoot, adminContext, {
        key: 'buyer',
        version: 2,
        actions: [{action: 'changeBuyerAssignable', buyerAssignable: true}],
      });

      expect(mockWithKey).toHaveBeenCalledWith({key: 'buyer'});
      expect(result).toEqual(mockUpdated);
    });

    it('throws when neither id nor key is provided', async () => {
      await expect(
        updateAssociateRole(mockApiRoot, adminContext, {
          version: 1,
          actions: [{action: 'setName', name: 'x'}],
        })
      ).rejects.toThrow('Either id or key must be provided');
    });
  });

  describe('SDK error propagation', () => {
    it('wraps SDK errors in SDKError', async () => {
      mockExecute.mockRejectedValueOnce(new Error('Network error'));

      await expect(
        readAssociateRole(
          mockApiRoot,
          {projectKey: 'test-project', isAdmin: true},
          {id: 'role-1'}
        )
      ).rejects.toThrow(SDKError);
    });
  });
});
