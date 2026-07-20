import {contextToCustomerFunctionMapping} from '../functions';
import * as customer from '../customer.functions';
import * as admin from '../admin.functions';
import * as store from '../store.functions';
import {CommercetoolsFuncContext} from '../../../types/configuration';

describe('contextToCustomerFunctionMapping', () => {
  it('should return customer context functions when customerId is provided', () => {
    const context: CommercetoolsFuncContext = {
      projectKey: 'test-project',
      customerId: 'customer-123',
    };

    const mapping = contextToCustomerFunctionMapping(context);

    expect(mapping).toEqual({
      read_customers: customer.readCustomerProfile,
    });
  });

  it('should return store context functions when storeKey is provided', () => {
    const context: CommercetoolsFuncContext = {
      projectKey: 'test-project',
      storeKey: 'store-123',
    };

    const mapping = contextToCustomerFunctionMapping(context);

    expect(mapping).toEqual({
      read_customers: store.readCustomerInStore,
      create_customers: store.createCustomerInStore,
      update_customers: store.updateCustomerInStore,
    });
  });

  it('should return admin context functions when isAdmin is provided', () => {
    const context: CommercetoolsFuncContext = {
      projectKey: 'test-project',
      isAdmin: true,
    };

    const mapping = contextToCustomerFunctionMapping(context);

    expect(mapping).toEqual({
      read_customers: admin.readCustomer,
      create_customers: admin.createCustomerAsAdmin,
      update_customers: admin.updateCustomerAsAdmin,
    });
  });

  it('should return empty object when no context is provided', () => {
    const mapping = contextToCustomerFunctionMapping();
    expect(mapping).toEqual({});
  });

  it('should return empty object when only projectKey is provided', () => {
    const context: CommercetoolsFuncContext = {
      projectKey: 'test-project',
    };

    const mapping = contextToCustomerFunctionMapping(context);
    expect(mapping).toEqual({});
  });
});
