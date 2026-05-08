import {readProductSelectionProductPrompt} from './prompts';
import {readProductSelectionProductParameters} from './parameters';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {z} from 'zod';

const tools: Record<string, Tool> = {
  read_product_selection_product: {
    method: 'read_product_selection_product',
    name: 'Read Product Selection Product',
    description: readProductSelectionProductPrompt,
    parameters: readProductSelectionProductParameters as unknown as z.ZodObject<any, any, any, any>,
    actions: {'product-selection-product': {read: true}},
  },
};

export const contextToProductSelectionProductTools = (context?: Context) => {
  if (context?.isAdmin || context?.storeKey) {
    return [tools.read_product_selection_product];
  }
  return [];
};
