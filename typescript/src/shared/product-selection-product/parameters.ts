import {z} from 'zod';

export const readProductSelectionProductParameters = z.object({
  productSelectionId: z
    .string()
    .optional()
    .describe('The ID of the Product Selection to fetch products from'),
  productSelectionKey: z
    .string()
    .optional()
    .describe('The key of the Product Selection to fetch products from'),
  where: z
    .array(z.string())
    .optional()
    .describe('Query predicates for filtering assigned products'),
  limit: z
    .number()
    .int()
    .min(1)
    .max(500)
    .optional()
    .describe(
      'Maximum number of results to return (default: 10, range: 1-500)'
    ),
  offset: z
    .number()
    .int()
    .min(0)
    .optional()
    .describe('Number of results to skip for pagination'),
  sort: z
    .array(z.string())
    .optional()
    .describe('Sort expressions, e.g. ["createdAt desc"]'),
  expand: z
    .array(z.string())
    .optional()
    .describe('References to expand, e.g. ["product"]'),
});
