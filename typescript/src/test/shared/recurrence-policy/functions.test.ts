import {
  readRecurrencePolicy,
  createRecurrencePolicy,
  updateRecurrencePolicy,
} from '../../../shared/recurrence-policy/functions';
import {contextToRecurrencePolicyFunctionMapping} from '../../../shared/recurrence-policy/functions';
import * as adminFunctions from '../../../shared/recurrence-policy/admin.functions';
import {ApiRoot} from '@commercetools/platform-sdk';
import {SDKError} from '../../../shared/errors/sdkError';

const mockExecute = jest.fn();
const mockGet = jest.fn().mockReturnValue({execute: mockExecute});
const mockPost = jest.fn().mockReturnValue({execute: mockExecute});
const mockWithId = jest.fn().mockReturnValue({get: mockGet, post: mockPost});
const mockWithKey = jest.fn().mockReturnValue({get: mockGet, post: mockPost});
const mockRecurrencePolicies = jest.fn().mockReturnValue({
  withId: mockWithId,
  withKey: mockWithKey,
  get: mockGet,
  post: mockPost,
});
const mockWithProjectKey = jest.fn().mockReturnValue({
  recurrencePolicies: mockRecurrencePolicies,
});

const mockApiRoot = {withProjectKey: mockWithProjectKey} as unknown as ApiRoot;

describe('Recurrence Policy Functions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('contextToRecurrencePolicyFunctionMapping', () => {
    it('returns admin functions when isAdmin is true', () => {
      const mapping = contextToRecurrencePolicyFunctionMapping({isAdmin: true});
      expect(mapping).toHaveProperty('read_recurrence_policy');
      expect(mapping).toHaveProperty('create_recurrence_policy');
      expect(mapping).toHaveProperty('update_recurrence_policy');
      expect(mapping.read_recurrence_policy).toBe(
        adminFunctions.readRecurrencePolicy
      );
      expect(mapping.create_recurrence_policy).toBe(
        adminFunctions.createRecurrencePolicy
      );
      expect(mapping.update_recurrence_policy).toBe(
        adminFunctions.updateRecurrencePolicy
      );
    });

    it('returns empty object when context is undefined', () => {
      expect(contextToRecurrencePolicyFunctionMapping(undefined)).toEqual({});
    });

    it('returns empty object when context has no relevant fields', () => {
      expect(
        contextToRecurrencePolicyFunctionMapping({storeKey: 'some-store'})
      ).toEqual({});
    });
  });

  describe('readRecurrencePolicy', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('fetches by ID when id is provided', async () => {
      const mockPolicy = {id: 'policy-1', version: 1, key: 'monthly'};
      mockExecute.mockResolvedValueOnce({body: mockPolicy});

      const result = await readRecurrencePolicy(mockApiRoot, adminContext, {
        id: 'policy-1',
      });

      expect(mockWithProjectKey).toHaveBeenCalledWith({
        projectKey: 'test-project',
      });
      expect(mockRecurrencePolicies).toHaveBeenCalled();
      expect(mockWithId).toHaveBeenCalledWith({ID: 'policy-1'});
      expect(result).toEqual(mockPolicy);
    });

    it('fetches by key when key is provided', async () => {
      const mockPolicy = {id: 'policy-1', version: 1, key: 'monthly'};
      mockExecute.mockResolvedValueOnce({body: mockPolicy});

      const result = await readRecurrencePolicy(mockApiRoot, adminContext, {
        key: 'monthly',
      });

      expect(mockWithKey).toHaveBeenCalledWith({key: 'monthly'});
      expect(result).toEqual(mockPolicy);
    });

    it('queries list when no id or key is given', async () => {
      const mockResponse = {results: [], count: 0, limit: 10, offset: 0};
      mockExecute.mockResolvedValueOnce({body: mockResponse});

      const result = await readRecurrencePolicy(mockApiRoot, adminContext, {
        where: ['key="monthly"'],
        limit: 5,
      });

      expect(mockGet).toHaveBeenCalledWith({
        queryArgs: {where: ['key="monthly"'], limit: 5},
      });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('createRecurrencePolicy', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('posts the draft body to the endpoint', async () => {
      const mockCreated = {id: 'policy-2', version: 1, key: 'weekly'};
      mockExecute.mockResolvedValueOnce({body: mockCreated});

      const result = await createRecurrencePolicy(mockApiRoot, adminContext, {
        key: 'weekly',
        schedule: {type: 'standard', interval: 7, unit: 'Day'},
      });

      expect(mockRecurrencePolicies).toHaveBeenCalled();
      expect(mockPost).toHaveBeenCalledWith({
        body: {
          key: 'weekly',
          schedule: {type: 'standard', interval: 7, unit: 'Day'},
        },
      });
      expect(result).toEqual(mockCreated);
    });
  });

  describe('updateRecurrencePolicy', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('updates by ID — fetches version first then posts', async () => {
      const mockCurrent = {id: 'policy-1', version: 3};
      const mockUpdated = {id: 'policy-1', version: 4};
      mockExecute
        .mockResolvedValueOnce({body: mockCurrent})
        .mockResolvedValueOnce({body: mockUpdated});

      const result = await updateRecurrencePolicy(mockApiRoot, adminContext, {
        id: 'policy-1',
        version: 3,
        actions: [{action: 'setKey', key: 'new-key'}],
      });

      expect(mockWithId).toHaveBeenCalledWith({ID: 'policy-1'});
      expect(mockPost).toHaveBeenCalledWith({
        body: {version: 3, actions: [{action: 'setKey', key: 'new-key'}]},
      });
      expect(result).toEqual(mockUpdated);
    });

    it('updates by key — fetches version first then posts', async () => {
      const mockCurrent = {id: 'policy-1', version: 2, key: 'monthly'};
      const mockUpdated = {id: 'policy-1', version: 3, key: 'monthly'};
      mockExecute
        .mockResolvedValueOnce({body: mockCurrent})
        .mockResolvedValueOnce({body: mockUpdated});

      const result = await updateRecurrencePolicy(mockApiRoot, adminContext, {
        key: 'monthly',
        version: 2,
        actions: [{action: 'setName', name: {en: 'Monthly'}}],
      });

      expect(mockWithKey).toHaveBeenCalledWith({key: 'monthly'});
      expect(result).toEqual(mockUpdated);
    });

    it('throws when neither id nor key is provided', async () => {
      await expect(
        updateRecurrencePolicy(mockApiRoot, adminContext, {
          version: 1,
          actions: [{action: 'setKey', key: 'x'}],
        })
      ).rejects.toThrow('Either id or key must be provided');
    });
  });

  describe('SDK error propagation', () => {
    it('wraps SDK errors in SDKError', async () => {
      mockExecute.mockRejectedValueOnce(new Error('Network error'));

      await expect(
        readRecurrencePolicy(
          mockApiRoot,
          {projectKey: 'test-project', isAdmin: true},
          {id: 'policy-1'}
        )
      ).rejects.toThrow(SDKError);
    });
  });
});
