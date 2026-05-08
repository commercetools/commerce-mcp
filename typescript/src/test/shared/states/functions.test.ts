import {readState, createState, updateState} from '../../../shared/states/functions';
import {contextToStateFunctionMapping} from '../../../shared/states/functions';
import * as adminFunctions from '../../../shared/states/admin.functions';
import {ApiRoot} from '@commercetools/platform-sdk';
import {SDKError} from '../../../shared/errors/sdkError';

const mockExecute = jest.fn();
const mockGet = jest.fn().mockReturnValue({execute: mockExecute});
const mockPost = jest.fn().mockReturnValue({execute: mockExecute});
const mockWithId = jest.fn().mockReturnValue({get: mockGet, post: mockPost});
const mockWithKey = jest.fn().mockReturnValue({get: mockGet, post: mockPost});
const mockStates = jest.fn().mockReturnValue({
  withId: mockWithId,
  withKey: mockWithKey,
  get: mockGet,
  post: mockPost,
});
const mockWithProjectKey = jest.fn().mockReturnValue({states: mockStates});

const mockApiRoot = {withProjectKey: mockWithProjectKey} as unknown as ApiRoot;

describe('State Functions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('contextToStateFunctionMapping', () => {
    it('returns admin functions when isAdmin is true', () => {
      const mapping = contextToStateFunctionMapping({isAdmin: true});
      expect(mapping).toHaveProperty('read_state');
      expect(mapping).toHaveProperty('create_state');
      expect(mapping).toHaveProperty('update_state');
      expect(mapping.read_state).toBe(adminFunctions.readState);
      expect(mapping.create_state).toBe(adminFunctions.createState);
      expect(mapping.update_state).toBe(adminFunctions.updateState);
    });

    it('returns empty object when context is undefined', () => {
      expect(contextToStateFunctionMapping(undefined)).toEqual({});
    });

    it('returns empty object for non-admin context', () => {
      expect(contextToStateFunctionMapping({storeKey: 'store-1'})).toEqual({});
    });
  });

  describe('readState', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('fetches by ID when id is provided', async () => {
      const mockState = {id: 'state-1', version: 1, key: 'processing', type: 'OrderState'};
      mockExecute.mockResolvedValueOnce({body: mockState});

      const result = await readState(mockApiRoot, adminContext, {id: 'state-1'});

      expect(mockWithProjectKey).toHaveBeenCalledWith({projectKey: 'test-project'});
      expect(mockStates).toHaveBeenCalled();
      expect(mockWithId).toHaveBeenCalledWith({ID: 'state-1'});
      expect(result).toEqual(mockState);
    });

    it('fetches by key when key is provided', async () => {
      const mockState = {id: 'state-1', version: 1, key: 'processing'};
      mockExecute.mockResolvedValueOnce({body: mockState});

      const result = await readState(mockApiRoot, adminContext, {key: 'processing'});

      expect(mockWithKey).toHaveBeenCalledWith({key: 'processing'});
      expect(result).toEqual(mockState);
    });

    it('queries list when no id or key is given', async () => {
      const mockResponse = {results: [], count: 0, limit: 10, offset: 0};
      mockExecute.mockResolvedValueOnce({body: mockResponse});

      const result = await readState(mockApiRoot, adminContext, {
        where: ['type="OrderState"'],
        limit: 20,
      });

      expect(mockGet).toHaveBeenCalledWith({
        queryArgs: {where: ['type="OrderState"'], limit: 20},
      });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('createState', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('posts the draft to the endpoint', async () => {
      const mockCreated = {id: 'state-2', version: 1, key: 'shipped', type: 'OrderState'};
      mockExecute.mockResolvedValueOnce({body: mockCreated});

      const result = await createState(mockApiRoot, adminContext, {
        key: 'shipped',
        type: 'OrderState',
        initial: false,
        name: {en: 'Shipped'},
      });

      expect(mockStates).toHaveBeenCalled();
      expect(mockPost).toHaveBeenCalledWith({
        body: {key: 'shipped', type: 'OrderState', initial: false, name: {en: 'Shipped'}},
      });
      expect(result).toEqual(mockCreated);
    });
  });

  describe('updateState', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('updates by ID — fetches current version then posts', async () => {
      const mockCurrent = {id: 'state-1', version: 2};
      const mockUpdated = {id: 'state-1', version: 3};
      mockExecute
        .mockResolvedValueOnce({body: mockCurrent})
        .mockResolvedValueOnce({body: mockUpdated});

      const result = await updateState(mockApiRoot, adminContext, {
        id: 'state-1',
        version: 2,
        actions: [{action: 'setName', name: {en: 'Processing'}}],
      });

      expect(mockWithId).toHaveBeenCalledWith({ID: 'state-1'});
      expect(mockPost).toHaveBeenCalledWith({
        body: {version: 2, actions: [{action: 'setName', name: {en: 'Processing'}}]},
      });
      expect(result).toEqual(mockUpdated);
    });

    it('updates by key — fetches current version then posts', async () => {
      const mockCurrent = {id: 'state-1', version: 1, key: 'processing'};
      const mockUpdated = {id: 'state-1', version: 2, key: 'processing'};
      mockExecute
        .mockResolvedValueOnce({body: mockCurrent})
        .mockResolvedValueOnce({body: mockUpdated});

      const result = await updateState(mockApiRoot, adminContext, {
        key: 'processing',
        version: 1,
        actions: [{action: 'changeInitial', initial: true}],
      });

      expect(mockWithKey).toHaveBeenCalledWith({key: 'processing'});
      expect(result).toEqual(mockUpdated);
    });

    it('throws when neither id nor key is provided', async () => {
      await expect(
        updateState(mockApiRoot, adminContext, {
          version: 1,
          actions: [{action: 'setName', name: {en: 'x'}}],
        })
      ).rejects.toThrow('Either id or key must be provided');
    });
  });

  describe('SDK error propagation', () => {
    it('wraps SDK errors in SDKError', async () => {
      mockExecute.mockRejectedValueOnce(new Error('Network error'));

      await expect(
        readState(
          mockApiRoot,
          {projectKey: 'test-project', isAdmin: true},
          {id: 'state-1'}
        )
      ).rejects.toThrow(SDKError);
    });
  });
});
