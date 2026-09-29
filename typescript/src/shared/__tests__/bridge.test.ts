import {contextToTools, contextToResourceTools} from '../tools';
import {contextToBulkTools} from '../bulk/tools';
import {
  resolveMethod,
  buildCoreConfiguration,
  deriveCheckoutUrl,
} from '../bridge';
import {isToolAllowed} from '../configuration';
import type {AuthConfig} from '../../types/auth';

const methods = (tools: {method: string}[]) => tools.map((t) => t.method);

describe('bridge tool building', () => {
  it('produces plural, namespace-based tool methods with a zod parameters schema', () => {
    const tools = contextToTools({isAdmin: true});
    const customerRead = tools.find((t) => t.method === 'read_customers');

    expect(customerRead).toBeDefined();
    // MCP registers tools via `tool.parameters.shape`.
    expect(customerRead!.parameters.shape).toBeDefined();
    expect(typeof customerRead!.description).toBe('string');
  });

  it('uses singular commerce-mcp namespaces as the actions key (scope filtering contract)', () => {
    const resources = contextToResourceTools({isAdmin: true});
    for (const tool of resources.customer) {
      expect(Object.keys(tool.actions)).toEqual(['customer']);
    }
    // isToolAllowed keys off actions -> namespace/permission.
    const read = resources.customer.find((t) => t.method === 'read_customers')!;
    expect(isToolAllowed(read, {actions: {customer: {read: true}}})).toBe(true);
    expect(isToolAllowed(read, {actions: {customer: {read: false}}})).toBe(
      false
    );
  });

  it('admin context exposes read/create/update for a standard resource', () => {
    const resources = contextToResourceTools({isAdmin: true});
    expect(methods(resources.customer).sort()).toEqual([
      'create_customers',
      'read_customers',
      'update_customers',
    ]);
  });

  it('customerId context scopes customer-owned resources (create/update are ownership-scoped in core)', () => {
    const resources = contextToResourceTools({customerId: 'cust-1'});

    // customers: own profile read + update, but no create (rejected in core).
    expect(methods(resources.customer).sort()).toEqual([
      'read_customers',
      'update_customers',
    ]);
    // orders / recurring-orders: full read/create/update (all scoped in core).
    expect(methods(resources.order).sort()).toEqual([
      'create_orders',
      'read_orders',
      'update_orders',
    ]);
    expect(methods(resources['recurring-orders']).sort()).toEqual([
      'create_recurring_orders',
      'read_recurring_orders',
      'update_recurring_orders',
    ]);
    // quotes / quote-requests: read + update only (create not self-scoped).
    expect(methods(resources.quote).sort()).toEqual([
      'read_quotes',
      'update_quotes',
    ]);
    expect(methods(resources['quote-request']).sort()).toEqual([
      'read_quote_requests',
      'update_quote_requests',
    ]);
    // Non customer-aware resources keep their full op set.
    expect(methods(resources.products).sort()).toEqual([
      'create_products',
      'read_products',
      'update_products',
    ]);
  });

  it('storeKey context narrows customer and store availability', () => {
    const resources = contextToResourceTools({storeKey: 'store-1'});
    expect(methods(resources.customer).sort()).toEqual([
      'create_customers',
      'read_customers',
    ]);
    expect(methods(resources.store)).toEqual(['read_stores']);
  });

  it('never exposes delete tools', () => {
    const tools = contextToTools({isAdmin: true});
    expect(tools.some((t) => t.method.startsWith('delete_'))).toBe(false);
  });

  it('exposes checkout-backed resources', () => {
    const tools = contextToTools({isAdmin: true});
    expect(methods(tools)).toContain('update_payment_intents');
    expect(methods(tools)).toContain('read_transactions');
    expect(methods(tools)).toContain('create_transactions');
  });

  it('exposes MCP servers and the read-only MCP server type catalogue', () => {
    const resources = contextToResourceTools({isAdmin: true});
    expect(methods(resources['mcp-server']).sort()).toEqual([
      'create_mcp_servers',
      'read_mcp_servers',
      'update_mcp_servers',
    ]);
    expect(methods(resources['mcp-server-type'])).toEqual([
      'read_mcp_server_types',
    ]);
  });

  it('exposes read-only views (messages, projections, customer search) as read only', () => {
    const resources = contextToResourceTools({isAdmin: true});
    expect(methods(resources.message)).toEqual(['read_messages']);
    expect(methods(resources['product-projection'])).toEqual([
      'read_product_projections',
    ]);
    expect(methods(resources['customer-search'])).toEqual([
      'read_customer_search',
    ]);
    expect(methods(resources['attribute-group']).sort()).toEqual([
      'create_attribute_groups',
      'read_attribute_groups',
      'update_attribute_groups',
    ]);
  });

  it('exposes checkout applications and payment integrations', () => {
    const resources = contextToResourceTools({isAdmin: true});
    expect(methods(resources.application).sort()).toEqual([
      'create_applications',
      'read_applications',
      'update_applications',
    ]);
    expect(methods(resources['payment-integration']).sort()).toEqual([
      'create_payment_integrations',
      'read_payment_integrations',
      'update_payment_integrations',
    ]);
  });

  it('exposes replicate carts and apply order-edits under their own action', () => {
    const resources = contextToResourceTools({isAdmin: true});
    const replicate = resources.cart.find(
      (t) => t.method === 'replicate_carts'
    )!;
    const apply = resources['order-edit'].find(
      (t) => t.method === 'apply_order_edits'
    )!;

    expect(replicate.actions).toEqual({cart: {replicate: true}});
    expect(apply.actions).toEqual({'order-edit': {apply: true}});
    // Neither extra is reachable through the create / update permission.
    expect(
      isToolAllowed(replicate, {actions: {cart: {create: true, update: true}}})
    ).toBe(false);
    expect(
      isToolAllowed(apply, {actions: {'order-edit': {update: true}}})
    ).toBe(false);
    expect(typeof replicate.description).toBe('string');
    expect(replicate.parameters.shape.reference).toBeDefined();
  });

  it('bulk tools are create/update and separate from contextToTools', () => {
    expect(methods(contextToBulkTools()).sort()).toEqual([
      'create_bulk',
      'update_bulk',
    ]);
    expect(
      contextToTools({isAdmin: true}).some((t) => t.method.endsWith('_bulk'))
    ).toBe(false);
  });
});

describe('bridge execution mapping', () => {
  it('resolveMethod maps exposed methods to a def + op and rejects others', () => {
    expect(resolveMethod('read_customers')).toMatchObject({
      op: 'read',
      def: {nsKey: 'customer'},
    });
    expect(resolveMethod('update_quote_requests')).toMatchObject({
      op: 'update',
      def: {nsKey: 'quote-request'},
    });
    // delete is not implemented/exposed.
    expect(resolveMethod('delete_customers')).toBeUndefined();
    // `mcp_servers` must not swallow `mcp_server_types` (or vice versa).
    expect(resolveMethod('read_mcp_server_types')).toMatchObject({
      op: 'read',
      def: {nsKey: 'mcp-server-type'},
    });
    expect(resolveMethod('update_mcp_servers')).toMatchObject({
      op: 'update',
      def: {nsKey: 'mcp-server'},
    });
    // create on a read-only resource is not exposed.
    expect(resolveMethod('create_product_search')).toBeUndefined();
    expect(resolveMethod('create_mcp_server_types')).toBeUndefined();
    expect(resolveMethod('replicate_carts')).toMatchObject({
      op: 'replicate',
      def: {nsKey: 'cart'},
    });
    expect(resolveMethod('apply_order_edits')).toMatchObject({
      op: 'apply',
      def: {nsKey: 'order-edit'},
    });
    // resource extras are only exposed on the resource that implements them.
    expect(resolveMethod('replicate_orders')).toBeUndefined();
    expect(resolveMethod('apply_carts')).toBeUndefined();
    expect(resolveMethod('not_a_tool')).toBeUndefined();
  });

  it('buildCoreConfiguration maps context to core configuration metadata', () => {
    const authConfig = {
      type: 'auth_token',
      projectKey: 'proj-1',
      apiUrl: 'https://api.europe-west1.gcp.commercetools.com',
      accessToken: 'tok',
    } as unknown as AuthConfig;

    const selfService = buildCoreConfiguration(authConfig, {
      customerId: 'cust-9',
    });
    expect(selfService.projectKey).toBe('proj-1');
    expect(selfService.metadata?.customer).toEqual({
      typeId: 'customer',
      id: 'cust-9',
    });
    expect(selfService.metadata?.businessUnit).toBeUndefined();
    expect(selfService.metadata?.apiUrl).toBe(authConfig.apiUrl as unknown);
    expect(selfService.metadata?.checkoutApiUrl).toBe(
      'https://checkout.europe-west1.gcp.commercetools.com'
    );

    const b2b = buildCoreConfiguration(authConfig, {
      customerId: 'cust-9',
      businessUnitKey: 'bu-1',
    });
    expect(b2b.metadata?.businessUnit).toEqual({
      typeId: 'business-unit',
      key: 'bu-1',
    });
  });

  it('deriveCheckoutUrl swaps the api host for the checkout host', () => {
    expect(
      deriveCheckoutUrl('https://api.us-central1.gcp.commercetools.com')
    ).toBe('https://checkout.us-central1.gcp.commercetools.com');
    expect(deriveCheckoutUrl(undefined)).toBeUndefined();
  });
});
