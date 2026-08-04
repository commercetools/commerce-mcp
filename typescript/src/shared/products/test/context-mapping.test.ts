import {contextToProductFunctionMapping} from '../functions';
import * as admin from '../admin.functions';
import {Context, CommercetoolsFuncContext} from '../../../types/configuration';

describe('contextToProductFunctionMapping', () => {
  it('should return admin functions when context has isAdmin set to true', () => {
    const context: CommercetoolsFuncContext = {
      projectKey: 'test-project',
      isAdmin: true,
    };
    const mapping = contextToProductFunctionMapping(context);

    expect(mapping).toEqual({
      read_products: admin.listProducts,
      create_products: admin.createProduct,
      update_products: admin.updateProduct,
    });
  });

  it('should return empty object when context is not provided', () => {
    const mapping = contextToProductFunctionMapping();
    expect(mapping).toEqual({
      read_products: admin.listProducts,
    });
  });

  it('should return empty object when context does not have isAdmin', () => {
    const context: CommercetoolsFuncContext = {projectKey: 'test-project'};
    const mapping = contextToProductFunctionMapping(context);
    expect(mapping).toEqual({
      read_products: admin.listProducts,
    });
  });
});
