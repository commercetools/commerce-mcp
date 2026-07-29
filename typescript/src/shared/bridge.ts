/**
 * Bridge between the commerce-mcp tool contract (`Tool` objects + method-based
 * execution) and the `@commercetools/tools-core` resource handlers.
 *
 * The public surface of `shared` (contextToTools, contextToResourceTools,
 * CommercetoolsAPI.run, contextToBulkTools) is preserved; this module is the
 * single place that maps between the two systems.
 */
import {z} from 'zod';
import type {Client} from '@commercetools/ts-client';
import {
  BaseResourceHandler,
  type Configuration as CoreConfiguration,
  type IApiClientFactory,
  type ToolExecutionContext,
  ApprovalFlowsHandler,
  ApprovalRulesHandler,
  AssociateRolesHandler,
  BulkHandler,
  BusinessUnitsHandler,
  CartDiscountsHandler,
  CartsHandler,
  CategoriesHandler,
  ChannelsHandler,
  CustomObjectsHandler,
  CustomerGroupsHandler,
  CustomersHandler,
  DiscountCodesHandler,
  ExtensionsHandler,
  InventoryHandler,
  OrderEditsHandler,
  OrdersHandler,
  PaymentIntentsHandler,
  PaymentMethodsHandler,
  PaymentsHandler,
  ProductDiscountsHandler,
  ProductSearchHandler,
  ProductSelectionAssignmentsHandler,
  ProductSelectionsHandler,
  ProductTailoringHandler,
  ProductTypesHandler,
  ProductsHandler,
  ProjectHandler,
  QuoteRequestsHandler,
  QuotesHandler,
  RecurrencePoliciesHandler,
  RecurringOrdersHandler,
  ReviewsHandler,
  ShippingMethodsHandler,
  ShoppingListsHandler,
  StagedQuotesHandler,
  StandalonePricesHandler,
  StatesHandler,
  StoresHandler,
  SubscriptionsHandler,
  TaxCategoriesHandler,
  TransactionsHandler,
  TypesHandler,
  ZonesHandler,
} from '@commercetools/tools-core';
import type {Tool} from '../types/tools';
import type {AuthConfig} from '../types/auth';
import type {Context} from '../types/configuration';

export type Op = 'read' | 'create' | 'update';
type Branch = 'associate' | 'customer' | 'store' | 'admin';
type ApiKind = 'platform' | 'checkout';

type HandlerCtor = new (
  factory?: IApiClientFactory<CoreConfiguration>
) => BaseResourceHandler<CoreConfiguration>;

interface ResourceDef {
  /** commerce-mcp namespace — used as the `actions` key (drives scope filtering). */
  nsKey: string;
  /** core plural namespace — used to derive tool method names (`<op>_<namespace>`). */
  coreNamespace: string;
  Handler: HandlerCtor;
  /** Operations exposed by default (admin) — only ops actually implemented in core. */
  baseOps: Op[];
  /** Per-context overrides that change which operations are exposed. */
  overrides?: Partial<Record<Branch, Op[]>>;
  apiKind?: ApiKind;
}

const RCU: Op[] = ['read', 'create', 'update'];

/**
 * Single source of truth mapping each commerce-mcp resource to its core handler,
 * default operations, and context-sensitive availability. Faithfully reproduces
 * the legacy per-resource `contextTo*Tools` availability matrix.
 *
 * Notes:
 * - `delete` is never exposed (core stubs it; parity with legacy commerce-mcp).
 * - resource extras (replicate carts, apply order-edits) are not yet exposed.
 */
const RESOURCE_DEFS: ResourceDef[] = [
  {
    nsKey: 'business-unit',
    coreNamespace: 'business-units',
    Handler: BusinessUnitsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'cart',
    coreNamespace: 'carts',
    Handler: CartsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'cart-discount',
    coreNamespace: 'cart-discounts',
    Handler: CartDiscountsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'category',
    coreNamespace: 'categories',
    Handler: CategoriesHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'channel',
    coreNamespace: 'channels',
    Handler: ChannelsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'customer',
    coreNamespace: 'customers',
    Handler: CustomersHandler,
    baseOps: RCU,
    overrides: {
      associate: ['read'],
      customer: ['read'],
      store: ['read', 'create'],
    },
  },
  {
    nsKey: 'customer-group',
    coreNamespace: 'customer-groups',
    Handler: CustomerGroupsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'discount-code',
    coreNamespace: 'discount-codes',
    Handler: DiscountCodesHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'order',
    coreNamespace: 'orders',
    Handler: OrdersHandler,
    baseOps: RCU,
    overrides: {customer: ['read']},
  },
  {
    nsKey: 'inventory',
    coreNamespace: 'inventory',
    Handler: InventoryHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'products',
    coreNamespace: 'products',
    Handler: ProductsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'review',
    coreNamespace: 'reviews',
    Handler: ReviewsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'project',
    coreNamespace: 'project',
    Handler: ProjectHandler,
    baseOps: ['read', 'update'],
  },
  {
    nsKey: 'product-search',
    coreNamespace: 'product-search',
    Handler: ProductSearchHandler,
    baseOps: ['read'],
  },
  {
    nsKey: 'product-selection',
    coreNamespace: 'product-selections',
    Handler: ProductSelectionsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'quote',
    coreNamespace: 'quotes',
    Handler: QuotesHandler,
    baseOps: RCU,
    overrides: {associate: ['read', 'update'], customer: ['read', 'update']},
  },
  {
    nsKey: 'quote-request',
    coreNamespace: 'quote-requests',
    Handler: QuoteRequestsHandler,
    baseOps: RCU,
    overrides: {customer: ['read', 'update']},
  },
  {
    nsKey: 'staged-quote',
    coreNamespace: 'staged-quotes',
    Handler: StagedQuotesHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'standalone-price',
    coreNamespace: 'standalone-prices',
    Handler: StandalonePricesHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'product-discount',
    coreNamespace: 'product-discounts',
    Handler: ProductDiscountsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'product-type',
    coreNamespace: 'product-types',
    Handler: ProductTypesHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'store',
    coreNamespace: 'stores',
    Handler: StoresHandler,
    baseOps: RCU,
    overrides: {store: ['read']},
  },
  {
    nsKey: 'payments',
    coreNamespace: 'payments',
    Handler: PaymentsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'shipping-methods',
    coreNamespace: 'shipping-methods',
    Handler: ShippingMethodsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'tax-category',
    coreNamespace: 'tax-categories',
    Handler: TaxCategoriesHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'zone',
    coreNamespace: 'zones',
    Handler: ZonesHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'product-tailoring',
    coreNamespace: 'product-tailoring',
    Handler: ProductTailoringHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'payment-methods',
    coreNamespace: 'payment-methods',
    Handler: PaymentMethodsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'recurring-orders',
    coreNamespace: 'recurring-orders',
    Handler: RecurringOrdersHandler,
    baseOps: RCU,
    overrides: {customer: ['read']},
  },
  {
    nsKey: 'shopping-lists',
    coreNamespace: 'shopping-lists',
    Handler: ShoppingListsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'extensions',
    coreNamespace: 'extensions',
    Handler: ExtensionsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'subscriptions',
    coreNamespace: 'subscriptions',
    Handler: SubscriptionsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'custom-objects',
    coreNamespace: 'custom-objects',
    Handler: CustomObjectsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'types',
    coreNamespace: 'types',
    Handler: TypesHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'payment-intents',
    coreNamespace: 'payment-intents',
    Handler: PaymentIntentsHandler,
    baseOps: ['update'],
    apiKind: 'checkout',
  },
  {
    nsKey: 'transactions',
    coreNamespace: 'transactions',
    Handler: TransactionsHandler,
    baseOps: ['read', 'create'],
    apiKind: 'checkout',
  },
  {
    nsKey: 'approval-flow',
    coreNamespace: 'approval-flows',
    Handler: ApprovalFlowsHandler,
    baseOps: ['read', 'update'],
  },
  {
    nsKey: 'approval-rule',
    coreNamespace: 'approval-rules',
    Handler: ApprovalRulesHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'associate-role',
    coreNamespace: 'associate-roles',
    Handler: AssociateRolesHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'order-edit',
    coreNamespace: 'order-edits',
    Handler: OrderEditsHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'product-selection-assignment',
    coreNamespace: 'product-selection-assignments',
    Handler: ProductSelectionAssignmentsHandler,
    baseOps: ['read'],
  },
  {
    nsKey: 'recurrence-policy',
    coreNamespace: 'recurrence-policies',
    Handler: RecurrencePoliciesHandler,
    baseOps: RCU,
  },
  {
    nsKey: 'states',
    coreNamespace: 'states',
    Handler: StatesHandler,
    baseOps: RCU,
  },
];

/** Bulk is registered separately by the MCP adapter (not part of contextToTools). */
const BULK_DEF: ResourceDef = {
  nsKey: 'bulk',
  coreNamespace: 'bulk',
  Handler: BulkHandler,
  baseOps: ['create', 'update'],
};

const DEFS_BY_NS = new Map<string, ResourceDef>(
  [...RESOURCE_DEFS, BULK_DEF].map((d) => [d.nsKey, d])
);

/** Derives the core tool method name for an operation (`read_customers`, ...). */
function methodName(def: ResourceDef, op: Op): string {
  return `${op}_${def.coreNamespace.replace(/-/g, '_')}`;
}

function titleCase(def: ResourceDef, op: Op): string {
  const opTitle = op.charAt(0).toUpperCase() + op.slice(1);
  return `${opTitle} ${def.nsKey}`;
}

// ---------------------------------------------------------------------------
// Client factory
// ---------------------------------------------------------------------------

/**
 * Factory injected into core handlers so they reuse commerce-mcp's already
 * authenticated ts-client instead of building their own. `getClient` ignores
 * the passed configuration/authToken and delegates to the resolver bound to a
 * live CommercetoolsAPI instance.
 */
export class BridgeApiClientFactory
  implements IApiClientFactory<CoreConfiguration>
{
  constructor(private readonly resolve: (apiKind: ApiKind) => Client) {}

  getClient(
    _configuration: CoreConfiguration,
    _authToken: string,
    options?: {apiKind?: ApiKind}
  ): Client {
    return this.resolve(options?.apiKind ?? 'platform');
  }
}

/** Factory used only for reading tool definitions — never provides a client. */
const NOOP_FACTORY: IApiClientFactory<CoreConfiguration> = {
  getClient(): Client {
    throw new Error(
      'BridgeApiClientFactory not configured for execution (definition-only handler)'
    );
  },
};

// Definition-only handler singletons (no client needed for getToolDefinition).
const definitionHandlers = new Map<
  string,
  BaseResourceHandler<CoreConfiguration>
>();
function getDefinitionHandler(
  def: ResourceDef
): BaseResourceHandler<CoreConfiguration> {
  let handler = definitionHandlers.get(def.nsKey);
  if (!handler) {
    handler = new def.Handler(NOOP_FACTORY);
    definitionHandlers.set(def.nsKey, handler);
  }
  return handler;
}

// ---------------------------------------------------------------------------
// Availability matrix
// ---------------------------------------------------------------------------

function resolveBranch(context?: Context): Branch {
  const customerId = context?.customerId;
  const businessUnitKey = context?.businessUnitKey;
  if (customerId && businessUnitKey) return 'associate';
  if (customerId) return 'customer';
  if (context?.storeKey) return 'store';
  return 'admin';
}

function opsForBranch(def: ResourceDef, branch: Branch): Op[] {
  const override = def.overrides?.[branch];
  const ops = override ?? def.baseOps;
  // Never expose an operation the resource does not implement.
  return ops.filter((op) => def.baseOps.includes(op));
}

// ---------------------------------------------------------------------------
// Tool building
// ---------------------------------------------------------------------------

function buildTool(def: ResourceDef, op: Op): Tool {
  const handler = getDefinitionHandler(def) as unknown as {
    getToolDefinition: (op: Op) => {
      name: string;
      description: string;
      inputSchema: unknown;
    };
  };
  const definition = handler.getToolDefinition(op);
  return {
    method: methodName(def, op),
    name: titleCase(def, op),
    description: definition.description,
    parameters: definition.inputSchema as z.ZodObject<any, any, any, any>,
    actions: {[def.nsKey]: {[op]: true}},
  };
}

/** Builds the per-resource tool map for the given context (excludes bulk). */
export function buildResourceTools(context?: Context): Record<string, Tool[]> {
  const branch = resolveBranch(context);
  const result: Record<string, Tool[]> = {};
  for (const def of RESOURCE_DEFS) {
    const ops = opsForBranch(def, branch);
    if (ops.length > 0) {
      result[def.nsKey] = ops.map((op) => buildTool(def, op));
    }
  }
  return result;
}

/** Builds the bulk tools (registered separately by the MCP adapter). */
export function buildBulkTools(_context?: Context): Tool[] {
  return BULK_DEF.baseOps.map((op) => buildTool(BULK_DEF, op));
}

// ---------------------------------------------------------------------------
// Execution
// ---------------------------------------------------------------------------

/** Resolves a tool method name to its resource definition + operation. */
export function resolveMethod(
  method: string
): {def: ResourceDef; op: Op} | undefined {
  const match = /^(read|create|update)_(.+)$/.exec(method);
  if (!match) return undefined;
  const op = match[1] as Op;
  const coreNamespace = match[2];
  for (const def of DEFS_BY_NS.values()) {
    if (
      def.coreNamespace.replace(/-/g, '_') === coreNamespace &&
      def.baseOps.includes(op)
    ) {
      return {def, op};
    }
  }
  return undefined;
}

/** Resolves a tool method name to its `{namespace, action}` action pair. */
export function resolveMethodToAction(
  method: string
): {namespace: string; action: Op} | undefined {
  const resolved = resolveMethod(method);
  if (!resolved) return undefined;
  return {namespace: resolved.def.nsKey, action: resolved.op};
}

/**
 * The canonical list of every selectable tool method name (underscore-based),
 * across all resources (admin superset) plus bulk. Single source of truth for
 * the CLI `--tools` allow-list.
 */
export function listAllToolMethods(): string[] {
  const methods: string[] = [];
  for (const def of [...RESOURCE_DEFS, BULK_DEF]) {
    for (const op of def.baseOps) {
      methods.push(methodName(def, op));
    }
  }
  return methods;
}

/**
 * Builds the core Configuration from commerce-mcp auth + context. Scoping hooks:
 * - `metadata.customer` ← context.customerId (self-service / associate identity)
 * - `metadata.associate.key` ← context.businessUnitKey (B2B associate context)
 */
export function buildCoreConfiguration(
  authConfig: AuthConfig,
  context?: Context,
  correlationId?: string
): CoreConfiguration {
  const apiUrl = (authConfig as {apiUrl?: string}).apiUrl;
  const checkoutApiUrl = deriveCheckoutUrl(apiUrl);
  return {
    projectKey: authConfig.projectKey,
    correlationId: correlationId ?? 'commerce-mcp',
    tools: [],
    metadata: {
      ...(apiUrl && {apiUrl}),
      ...(checkoutApiUrl && {checkoutApiUrl}),
      ...(context?.customerId && {
        customer: {typeId: 'customer' as const, id: context.customerId},
      }),
      ...(context?.businessUnitKey && {
        associate: {
          typeId: 'customer' as const,
          id: context.customerId ?? '',
          key: context.businessUnitKey,
        },
      }),
    },
  };
}

/** Derives the Checkout API host from the Platform API host (api.* → checkout.*). */
export function deriveCheckoutUrl(apiUrl?: string): string | undefined {
  if (!apiUrl) return undefined;
  return apiUrl.replace('//api.', '//checkout.');
}

/**
 * Injects context-derived values into tool parameters where core reads them
 * from params (rather than configuration): store scope and cart override.
 */
export function mergeContextIntoParams(
  def: ResourceDef,
  params: Record<string, unknown>,
  context?: Context
): Record<string, unknown> {
  const merged: Record<string, unknown> = {...params};
  if (context?.storeKey && merged.storeKey === undefined) {
    merged.storeKey = context.storeKey;
  }
  // Cart: context.cartId acts as an id override for reads/updates.
  if (
    def.nsKey === 'cart' &&
    context?.cartId &&
    merged.id === undefined &&
    merged.key === undefined
  ) {
    merged.id = context.cartId;
  }
  return merged;
}

/** Builds the core ToolExecutionContext for a handler execution. */
export function buildExecutionContext(
  method: string,
  params: Record<string, unknown>,
  coreConfiguration: CoreConfiguration,
  authToken: string,
  sessionId?: string
): ToolExecutionContext<CoreConfiguration> {
  return {
    authToken,
    toolName: method,
    configuration: coreConfiguration,
    parameters: params,
    ...(sessionId && {sessionId}),
  };
}

/** Instantiates a core handler bound to the execution factory. */
export function createHandler(
  def: ResourceDef,
  factory: IApiClientFactory<CoreConfiguration>
): BaseResourceHandler<CoreConfiguration> {
  return new def.Handler(factory);
}
