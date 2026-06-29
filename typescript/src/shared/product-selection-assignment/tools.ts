import {readProductSelectionAssignmentsPrompt} from './prompts';
import {readProductSelectionAssignmentsParameters} from './parameters';
import {Tool} from '../../types/tools';
import {Context} from '../../types/configuration';
import {z} from 'zod';

const tools: Record<string, Tool> = {
  read_product_selection_assignments: {
    method: 'read_product_selection_assignments',
    name: 'Read Product Selection Assignments',
    description: readProductSelectionAssignmentsPrompt,
    parameters:
      readProductSelectionAssignmentsParameters as unknown as z.ZodObject<
        any,
        any,
        any,
        any
      >,
    actions: {'product-selection-assignment': {read: true}},
  },
};

export const contextToProductSelectionAssignmentTools = (context?: Context) => {
  if (context?.isAdmin || context?.storeKey) {
    return [tools.read_product_selection_assignments];
  }
  return [];
};
