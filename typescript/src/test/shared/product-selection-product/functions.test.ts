import {readProductSelectionProduct} from '../../../shared/product-selection-product/functions';
import {contextToProductSelectionProductFunctionMapping} from '../../../shared/product-selection-product/functions';
import * as adminFunctions from '../../../shared/product-selection-product/admin.functions';
import * as storeFunctions from '../../../shared/product-selection-product/store.functions';
import {ApiRoot} from '@commercetools/platform-sdk';
import {SDKError} from '../../../shared/errors/sdkError';

const mockExecute = jest.fn();
const mockGet = jest.fn().mockReturnValue({execute: mockExecute});
const mockProducts = jest.fn().mockReturnValue({get: mockGet});
const mockWithId = jest.fn().mockReturnValue({products: mockProducts});
const mockWithKey = jest.fn().mockReturnValue({products: mockProducts});
const mockProductSelections = jest.fn().mockReturnValue({
  withId: mockWithId,
  withKey: mockWithKey,
});
const mockWithProjectKey = jest.fn().mockReturnValue({
  productSelections: mockProductSelections,
});

const mockApiRoot = {withProjectKey: mockWithProjectKey} as unknown as ApiRoot;

describe('Product Selection Product Functions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('contextToProductSelectionProductFunctionMapping', () => {
    it('returns store function when storeKey is present', () => {
      const mapping = contextToProductSelectionProductFunctionMapping({storeKey: 'store-1'});
      expect(mapping).toHaveProperty('read_product_selection_product');
      expect(mapping.read_product_selection_product).toBe(
        storeFunctions.readProductSelectionProduct
      );
    });

    it('returns admin function when isAdmin is true', () => {
      const mapping = contextToProductSelectionProductFunctionMapping({isAdmin: true});
      expect(mapping).toHaveProperty('read_product_selection_product');
      expect(mapping.read_product_selection_product).toBe(
        adminFunctions.readProductSelectionProduct
      );
    });

    it('returns empty object when context is undefined', () => {
      expect(contextToProductSelectionProductFunctionMapping(undefined)).toEqual({});
    });

    it('returns empty object for associate context', () => {
      expect(
        contextToProductSelectionProductFunctionMapping({
          customerId: 'c1',
          businessUnitKey: 'bu-1',
        })
      ).toEqual({});
    });
  });

  describe('readProductSelectionProduct (admin context)', () => {
    const adminContext = {projectKey: 'test-project', isAdmin: true};

    it('queries products by selection ID', async () => {
      const mockResponse = {results: [], count: 0, limit: 10, offset: 0};
      mockExecute.mockResolvedValueOnce({body: mockResponse});

      const result = await readProductSelectionProduct(mockApiRoot, adminContext, {
        productSelectionId: 'sel-1',
        limit: 10,
      });

      expect(mockWithProjectKey).toHaveBeenCalledWith({projectKey: 'test-project'});
      expect(mockProductSelections).toHaveBeenCalled();
      expect(mockWithId).toHaveBeenCalledWith({ID: 'sel-1'});
      expect(mockProducts).toHaveBeenCalled();
      expect(mockGet).toHaveBeenCalledWith({queryArgs: {limit: 10}});
      expect(result).toEqual(mockResponse);
    });

    it('queries products by selection key', async () => {
      const mockResponse = {results: [], count: 0, limit: 10, offset: 0};
      mockExecute.mockResolvedValueOnce({body: mockResponse});

      const result = await readProductSelectionProduct(mockApiRoot, adminContext, {
        productSelectionKey: 'selection-key',
      });

      expect(mockWithKey).toHaveBeenCalledWith({key: 'selection-key'});
      expect(result).toEqual(mockResponse);
    });

    it('throws when neither productSelectionId nor productSelectionKey is given', async () => {
      await expect(
        readProductSelectionProduct(mockApiRoot, adminContext, {})
      ).rejects.toThrow('Either productSelectionId or productSelectionKey must be provided');
    });
  });

  describe('readProductSelectionProduct (store context)', () => {
    const storeContext = {projectKey: 'test-project', storeKey: 'my-store'};

    it('queries products by selection ID via store context', async () => {
      const mockResponse = {results: [{product: {id: 'prod-1', typeId: 'product'}}], count: 1};
      mockExecute.mockResolvedValueOnce({body: mockResponse});

      const result = await readProductSelectionProduct(mockApiRoot, storeContext, {
        productSelectionId: 'sel-2',
      });

      expect(mockWithId).toHaveBeenCalledWith({ID: 'sel-2'});
      expect(result).toEqual(mockResponse);
    });
  });

  describe('SDK error propagation', () => {
    it('wraps SDK errors in SDKError', async () => {
      mockExecute.mockRejectedValueOnce(new Error('Network error'));

      await expect(
        readProductSelectionProduct(
          mockApiRoot,
          {projectKey: 'test-project', isAdmin: true},
          {productSelectionId: 'sel-1'}
        )
      ).rejects.toThrow(SDKError);
    });
  });
});
