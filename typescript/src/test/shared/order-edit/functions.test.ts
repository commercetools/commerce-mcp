import {
  readOrderEdit,
  createOrderEdit,
  updateOrderEdit,
  applyOrderEdit,
} from '../../../shared/order-edit/functions';
import {contextToOrderEditFunctionMapping} from '../../../shared/order-edit/functions';
import * as adminFunctions from '../../../shared/order-edit/admin.functions';
import {ApiRoot} from '@commercetools/platform-sdk';
import {SDKError} from '../../../shared/errors/sdkError';

const mockExecute = jest.fn();
const mockGet = jest.fn().mockReturnValue({execute: mockExecute});
const mockPost = jest.fn().mockReturnValue({execute: mockExecute});
const mockApplyPost = jest.fn().mockReturnValue({execute: mockExecute});
const mockApply = jest.fn().mockReturnValue({post: mockApplyPost});
const mockWithId = jest
  .fn()
  .mockReturnValue({get: mockGet, post: mockPost, apply: mockApply});
const mockWithKey = jest.fn().mockReturnValue({get: mockGet, post: mockPost});
const mockEdits = jest.fn().mockReturnValue({
  withId: mockWithId,
  withKey: mockWithKey,
  get: mockGet,
  post: mockPost,
});
const mockOrders = jest.fn().mockReturnValue({edits: mockEdits});
const mockWithProjectKey = jest.fn().mockReturnValue({orders: mockOrders});

const mockApiRoot = {withProjectKey: mockWithProjectKey} as unknown as ApiRoot;

describe('Order Edit Functions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('contextToOrderEditFunctionMapping', () => {
    it('returns all 4 functions for admin context', () => {
      const mapping = contextToOrderEditFunctionMapping({isAdmin: true});
      expect(mapping).toHaveProperty('read_order_edit');
      expect(mapping).toHaveProperty('create_order_edit');
      expect(mapping).toHaveProperty('update_order_edit');
      expect(mapping).toHaveProperty('apply_order_edit');
      expect(mapping.read_order_edit).toBe(adminFunctions.readOrderEdit);
      expect(mapping.apply_order_edit).toBe(adminFunctions.applyOrderEdit);
    });

    it('returns empty object when context is undefined', () => {
      expect(contextToOrderEditFunctionMapping(undefined)).toEqual({});
    });

    it('returns empty object for non-admin context', () => {
      expect(
        contextToOrderEditFunctionMapping({
          customerId: 'c1',
          businessUnitKey: 'bu-1',
        })
      ).toEqual({});
    });
  });

  describe('readOrderEdit', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('fetches by ID', async () => {
      const mockEdit = {id: 'edit-1', version: 1};
      mockExecute.mockResolvedValueOnce({body: mockEdit});

      const result = await readOrderEdit(mockApiRoot, adminContext, {
        id: 'edit-1',
      });

      expect(mockWithProjectKey).toHaveBeenCalledWith({
        projectKey: 'test-project',
      });
      expect(mockOrders).toHaveBeenCalled();
      expect(mockEdits).toHaveBeenCalled();
      expect(mockWithId).toHaveBeenCalledWith({ID: 'edit-1'});
      expect(result).toEqual(mockEdit);
    });

    it('fetches by key', async () => {
      const mockEdit = {id: 'edit-1', version: 1, key: 'my-edit'};
      mockExecute.mockResolvedValueOnce({body: mockEdit});

      const result = await readOrderEdit(mockApiRoot, adminContext, {
        key: 'my-edit',
      });

      expect(mockWithKey).toHaveBeenCalledWith({key: 'my-edit'});
      expect(result).toEqual(mockEdit);
    });

    it('queries list', async () => {
      const mockResponse = {results: [], count: 0, limit: 10, offset: 0};
      mockExecute.mockResolvedValueOnce({body: mockResponse});

      const result = await readOrderEdit(mockApiRoot, adminContext, {limit: 5});

      expect(mockGet).toHaveBeenCalledWith({queryArgs: {limit: 5}});
      expect(result).toEqual(mockResponse);
    });
  });

  describe('createOrderEdit', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('posts the draft to the endpoint', async () => {
      const mockCreated = {id: 'edit-2', version: 1};
      mockExecute.mockResolvedValueOnce({body: mockCreated});

      const result = await createOrderEdit(mockApiRoot, adminContext, {
        resource: {id: 'order-1', typeId: 'order'},
        key: 'my-edit',
        comment: 'Fixing address',
      });

      expect(mockEdits).toHaveBeenCalled();
      expect(mockPost).toHaveBeenCalledWith({
        body: {
          resource: {id: 'order-1', typeId: 'order'},
          key: 'my-edit',
          comment: 'Fixing address',
        },
      });
      expect(result).toEqual(mockCreated);
    });
  });

  describe('updateOrderEdit', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('updates by ID — fetches version first then posts', async () => {
      const mockCurrent = {id: 'edit-1', version: 2};
      const mockUpdated = {id: 'edit-1', version: 3};
      mockExecute
        .mockResolvedValueOnce({body: mockCurrent})
        .mockResolvedValueOnce({body: mockUpdated});

      const result = await updateOrderEdit(mockApiRoot, adminContext, {
        id: 'edit-1',
        version: 2,
        actions: [{action: 'setComment', comment: 'Updated comment'}],
      });

      expect(mockWithId).toHaveBeenCalledWith({ID: 'edit-1'});
      expect(mockPost).toHaveBeenCalledWith({
        body: {
          version: 2,
          actions: [{action: 'setComment', comment: 'Updated comment'}],
        },
      });
      expect(result).toEqual(mockUpdated);
    });

    it('updates by key', async () => {
      const mockCurrent = {id: 'edit-1', version: 1, key: 'my-edit'};
      const mockUpdated = {id: 'edit-1', version: 2, key: 'my-edit'};
      mockExecute
        .mockResolvedValueOnce({body: mockCurrent})
        .mockResolvedValueOnce({body: mockUpdated});

      await updateOrderEdit(mockApiRoot, adminContext, {
        key: 'my-edit',
        version: 1,
        actions: [{action: 'setKey', key: 'new-key'}],
      });

      expect(mockWithKey).toHaveBeenCalledWith({key: 'my-edit'});
    });

    it('throws when neither id nor key is provided', async () => {
      await expect(
        updateOrderEdit(mockApiRoot, adminContext, {
          version: 1,
          actions: [{action: 'setComment', comment: 'x'}],
        })
      ).rejects.toThrow('Either id or key must be provided');
    });
  });

  describe('applyOrderEdit', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('calls the apply sub-path with editVersion and resourceVersion', async () => {
      const mockResult = {id: 'edit-1', result: {type: 'Applied'}};
      mockExecute.mockResolvedValueOnce({body: mockResult});

      const result = await applyOrderEdit(mockApiRoot, adminContext, {
        id: 'edit-1',
        editVersion: 3,
        resourceVersion: 7,
      });

      expect(mockWithId).toHaveBeenCalledWith({ID: 'edit-1'});
      expect(mockApply).toHaveBeenCalled();
      expect(mockApplyPost).toHaveBeenCalledWith({
        body: {editVersion: 3, resourceVersion: 7},
      });
      expect(result).toEqual(mockResult);
    });
  });

  describe('SDK error propagation', () => {
    it('wraps SDK errors in SDKError', async () => {
      mockExecute.mockRejectedValueOnce(new Error('Network error'));

      await expect(
        readOrderEdit(
          mockApiRoot,
          {projectKey: 'test-project', isAdmin: true},
          {id: 'edit-1'}
        )
      ).rejects.toThrow(SDKError);
    });
  });
});
