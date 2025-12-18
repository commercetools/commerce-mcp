import {contextToBusinessUnitTools} from './business-unit/tools';
import {contextToProductsTools} from './products/tools';
import {contextToProjectTools} from './project/tools';
import {contextToProductSearchTools} from './product-search/tools';
import {contextToCategoryTools} from './category/tools';
import {contextToChannelTools} from './channel/tools';
import {contextToProductSelectionTools} from './product-selection/tools';
import {contextToOrderTools} from './order/tools';
import {contextToCartTools} from './cart/tools';
import {contextToCustomerTools} from './customer/tools';
import {contextToCustomerGroupTools} from './customer-group/tools';
import {contextToQuoteTools} from './quote/tools';
import {contextToQuoteRequestTools} from './quote-request/tools';
import {contextToStagedQuoteTools} from './staged-quote/tools';
import {contextToStandalonePriceTools} from './standalone-price/tools';
import {contextToProductDiscountTools} from './product-discount/tools';
import {contextToCartDiscountTools} from './cart-discount/tools';
import {contextToDiscountCodeTools} from './discount-code/tools';
import {contextToProductTypeTools} from './product-type/tools';
import {contextToBulkTools} from './bulk/tools';
import {contextToInventoryTools} from './inventory/tools';
import {contextToStoreTools} from './store/tools';
import {contextToReviewTools} from './reviews/tools';
import {contextToPaymentTools} from './payments/tools';
import {contextToShippingMethodTools} from './shipping-methods/tools';
import {contextToTaxCategoryTools} from './tax-category/tools';
import {contextToZoneTools} from './zones/tools';
import {contextToProductTailoringTools} from './product-tailoring/tools';
import {contextToPaymentMethodTools} from './payment-methods/tools';
import {contextToRecurringOrderTools} from './recurring-orders/tools';
import {contextToShoppingListTools} from './shopping-lists/tools';
import {contextToExtensionTools} from './extensions/tools';
import {contextToSubscriptionTools} from './subscriptions/tools';
import {contextToCustomObjectTools} from './custom-objects/tools';
import {contextToTypeTools} from './types/tools';
import {contextToPaymentIntentTools} from './payment-intents/tools';
import {contextToTransactionTools} from './transactions/tools';
import {Context, Configuration} from '../types/configuration';
import {AvailableNamespaces} from '../types/tools';

export const contextToResourceTools = (
  context?: Context,
  configuration?: Configuration
) => {
  // If configuration.actions is provided, check which resources have actions configured
  // This allows tools to be loaded even when isAdmin is false, if they're explicitly configured
  const hasConfiguredActions = (namespace: string): boolean => {
    if (!configuration?.actions) {
      return false;
    }
    const actions = configuration.actions[namespace as AvailableNamespaces];
    return !!(actions && Object.keys(actions).length > 0);
  };

  // Helper to get context with isAdmin temporarily enabled if actions are configured
  // This allows tools to be loaded when explicitly configured, even if isAdmin is false
  const getContextForResource = (namespace: string): Context | undefined => {
    if (context?.isAdmin) {
      return context;
    }
    if (hasConfiguredActions(namespace)) {
      // Temporarily enable isAdmin to allow tools to be loaded
      // The isToolAllowed filter will ensure only configured tools are available
      return {...context, isAdmin: true};
    }
    return context;
  };

  // Helper function to reduce complexity by handling the common pattern
  const getToolsForResource = (
    namespace: string,
    toolFunction: (ctx?: Context) => any[],
    requiresAdmin: boolean = false
  ): any[] => {
    if (requiresAdmin) {
      return hasConfiguredActions(namespace) || context?.isAdmin
        ? toolFunction(getContextForResource(namespace))
        : [];
    }
    return toolFunction(context);
  };

  return {
    'business-unit': getToolsForResource(
      'business-unit',
      contextToBusinessUnitTools,
      true
    ),
    cart: getToolsForResource('cart', contextToCartTools),
    'cart-discount': getToolsForResource(
      'cart-discount',
      contextToCartDiscountTools,
      true
    ),
    category: getToolsForResource('category', contextToCategoryTools),
    channel: getToolsForResource('channel', contextToChannelTools, true),
    customer: getToolsForResource('customer', contextToCustomerTools),
    'customer-group': getToolsForResource(
      'customer-group',
      contextToCustomerGroupTools,
      true
    ),
    'discount-code': getToolsForResource(
      'discount-code',
      contextToDiscountCodeTools,
      true
    ),
    order: getToolsForResource('order', contextToOrderTools, true),
    inventory: getToolsForResource('inventory', contextToInventoryTools, true),
    products: getToolsForResource('products', contextToProductsTools),
    review: getToolsForResource('review', contextToReviewTools),
    project: getToolsForResource('project', contextToProjectTools),
    'product-search': getToolsForResource(
      'product-search',
      contextToProductSearchTools
    ),
    'product-selection': getToolsForResource(
      'product-selection',
      contextToProductSelectionTools,
      true
    ),
    quote: getToolsForResource('quote', contextToQuoteTools, true),
    'quote-request': getToolsForResource(
      'quote-request',
      contextToQuoteRequestTools,
      true
    ),
    'staged-quote': getToolsForResource(
      'staged-quote',
      contextToStagedQuoteTools,
      true
    ),
    'standalone-price': getToolsForResource(
      'standalone-price',
      contextToStandalonePriceTools,
      true
    ),
    'product-discount': getToolsForResource(
      'product-discount',
      contextToProductDiscountTools,
      true
    ),
    'product-type': getToolsForResource(
      'product-type',
      contextToProductTypeTools
    ),
    store: getToolsForResource('store', contextToStoreTools),
    bulk: getToolsForResource('bulk', contextToBulkTools, true),
    payments: getToolsForResource('payments', contextToPaymentTools, true),
    'shipping-methods': getToolsForResource(
      'shipping-methods',
      contextToShippingMethodTools,
      true
    ),
    'tax-category': getToolsForResource(
      'tax-category',
      contextToTaxCategoryTools,
      true
    ),
    zone: getToolsForResource('zone', contextToZoneTools, true),
    'product-tailoring': getToolsForResource(
      'product-tailoring',
      contextToProductTailoringTools,
      true
    ),
    'payment-methods': getToolsForResource(
      'payment-methods',
      contextToPaymentMethodTools,
      true
    ),
    'recurring-orders': getToolsForResource(
      'recurring-orders',
      contextToRecurringOrderTools,
      true
    ),
    'shopping-lists': getToolsForResource(
      'shopping-lists',
      contextToShoppingListTools,
      true
    ),
    extension: getToolsForResource('extension', contextToExtensionTools, true),
    subscription: getToolsForResource(
      'subscription',
      contextToSubscriptionTools,
      true
    ),
    'custom-objects': getToolsForResource(
      'custom-objects',
      contextToCustomObjectTools,
      true
    ),
    types: getToolsForResource('types', contextToTypeTools, true),
    'payment-intents': getToolsForResource(
      'payment-intents',
      contextToPaymentIntentTools,
      true
    ),
    transactions: getToolsForResource(
      'transactions',
      contextToTransactionTools,
      true
    ),
  };
};
export const contextToTools = (
  context?: Context,
  configuration?: Configuration
) => {
  const resourceTools = contextToResourceTools(context, configuration);

  return Object.values(resourceTools).flat();
};
