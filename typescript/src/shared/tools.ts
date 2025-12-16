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

  return {
    'business-unit':
      hasConfiguredActions('business-unit') || context?.isAdmin
        ? contextToBusinessUnitTools(getContextForResource('business-unit'))
        : [],
    cart: contextToCartTools(context),
    'cart-discount':
      hasConfiguredActions('cart-discount') || context?.isAdmin
        ? contextToCartDiscountTools(getContextForResource('cart-discount'))
        : [],
    category: contextToCategoryTools(context),
    channel:
      hasConfiguredActions('channel') || context?.isAdmin
        ? contextToChannelTools(getContextForResource('channel'))
        : [],
    customer: contextToCustomerTools(context),
    'customer-group':
      hasConfiguredActions('customer-group') || context?.isAdmin
        ? contextToCustomerGroupTools(getContextForResource('customer-group'))
        : [],
    'discount-code':
      hasConfiguredActions('discount-code') || context?.isAdmin
        ? contextToDiscountCodeTools(getContextForResource('discount-code'))
        : [],
    order:
      hasConfiguredActions('order') || context?.isAdmin
        ? contextToOrderTools(getContextForResource('order'))
        : [],
    inventory:
      hasConfiguredActions('inventory') || context?.isAdmin
        ? contextToInventoryTools(getContextForResource('inventory'))
        : [],
    products: contextToProductsTools(context),
    review: contextToReviewTools(context),
    project: contextToProjectTools(context),
    'product-search': contextToProductSearchTools(context),
    'product-selection':
      hasConfiguredActions('product-selection') || context?.isAdmin
        ? contextToProductSelectionTools(
            getContextForResource('product-selection')
          )
        : [],
    quote:
      hasConfiguredActions('quote') || context?.isAdmin
        ? contextToQuoteTools(getContextForResource('quote'))
        : [],
    'quote-request':
      hasConfiguredActions('quote-request') || context?.isAdmin
        ? contextToQuoteRequestTools(getContextForResource('quote-request'))
        : [],
    'staged-quote':
      hasConfiguredActions('staged-quote') || context?.isAdmin
        ? contextToStagedQuoteTools(getContextForResource('staged-quote'))
        : [],
    'standalone-price':
      hasConfiguredActions('standalone-price') || context?.isAdmin
        ? contextToStandalonePriceTools(
            getContextForResource('standalone-price')
          )
        : [],
    'product-discount':
      hasConfiguredActions('product-discount') || context?.isAdmin
        ? contextToProductDiscountTools(
            getContextForResource('product-discount')
          )
        : [],
    'product-type': contextToProductTypeTools(context),
    store: contextToStoreTools(context),
    bulk:
      hasConfiguredActions('bulk') || context?.isAdmin
        ? contextToBulkTools(getContextForResource('bulk'))
        : [],
    payments:
      hasConfiguredActions('payments') || context?.isAdmin
        ? contextToPaymentTools(getContextForResource('payments'))
        : [],
    'shipping-methods':
      hasConfiguredActions('shipping-methods') || context?.isAdmin
        ? contextToShippingMethodTools(
            getContextForResource('shipping-methods')
          )
        : [],
    'tax-category':
      hasConfiguredActions('tax-category') || context?.isAdmin
        ? contextToTaxCategoryTools(getContextForResource('tax-category'))
        : [],
    zone:
      hasConfiguredActions('zone') || context?.isAdmin
        ? contextToZoneTools(getContextForResource('zone'))
        : [],
    'product-tailoring':
      hasConfiguredActions('product-tailoring') || context?.isAdmin
        ? contextToProductTailoringTools(
            getContextForResource('product-tailoring')
          )
        : [],
    'payment-methods':
      hasConfiguredActions('payment-methods') || context?.isAdmin
        ? contextToPaymentMethodTools(getContextForResource('payment-methods'))
        : [],
    'recurring-orders':
      hasConfiguredActions('recurring-orders') || context?.isAdmin
        ? contextToRecurringOrderTools(
            getContextForResource('recurring-orders')
          )
        : [],
    'shopping-lists':
      hasConfiguredActions('shopping-lists') || context?.isAdmin
        ? contextToShoppingListTools(getContextForResource('shopping-lists'))
        : [],
    extension:
      hasConfiguredActions('extension') || context?.isAdmin
        ? contextToExtensionTools(getContextForResource('extension'))
        : [],
    subscription:
      hasConfiguredActions('subscription') || context?.isAdmin
        ? contextToSubscriptionTools(getContextForResource('subscription'))
        : [],
    'custom-objects':
      hasConfiguredActions('custom-objects') || context?.isAdmin
        ? contextToCustomObjectTools(getContextForResource('custom-objects'))
        : [],
    types:
      hasConfiguredActions('types') || context?.isAdmin
        ? contextToTypeTools(getContextForResource('types'))
        : [],
    'payment-intents':
      hasConfiguredActions('payment-intents') || context?.isAdmin
        ? contextToPaymentIntentTools(getContextForResource('payment-intents'))
        : [],
    transactions:
      hasConfiguredActions('transactions') || context?.isAdmin
        ? contextToTransactionTools(getContextForResource('transactions'))
        : [],
  };
};
export const contextToTools = (
  context?: Context,
  configuration?: Configuration
) => {
  const resourceTools = contextToResourceTools(context, configuration);

  return Object.values(resourceTools).flat();
};
