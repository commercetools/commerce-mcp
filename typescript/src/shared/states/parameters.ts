import {z} from 'zod';

export const readStateParameters = z.object({
  id: z.string().optional().describe('The ID of the State to fetch'),
  key: z.string().optional().describe('The key of the State to fetch'),
  where: z
    .array(z.string())
    .optional()
    .describe('Query predicates for filtering States'),
  limit: z
    .number()
    .int()
    .min(1)
    .max(500)
    .optional()
    .describe('Maximum number of results to return (default: 10, range: 1-500)'),
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
    .describe('References to expand, e.g. ["transitions[*]"]'),
});

export const createStateParameters = z.object({
  key: z.string().describe('User-defined unique identifier for the State'),
  type: z
    .enum([
      'OrderState',
      'RecurringOrderState',
      'LineItemState',
      'ProductState',
      'ReviewState',
      'PaymentState',
      'QuoteRequestState',
      'StagedQuoteState',
      'QuoteState',
    ])
    .describe('The type of the State, determining which resource it applies to'),
  initial: z
    .boolean()
    .optional()
    .describe('Whether this is an initial State. There can be only one initial State per type.'),
  name: z
    .record(z.string(), z.string())
    .optional()
    .describe('Localized name of the State'),
  description: z
    .record(z.string(), z.string())
    .optional()
    .describe('Localized description of the State'),
  roles: z
    .array(z.enum(['ReviewIncludedInStatistics', 'Return']))
    .optional()
    .describe('Roles of the State. Only applicable for LineItemState and ReviewState.'),
  transitions: z
    .array(
      z.object({
        id: z.string(),
        typeId: z.literal('state'),
      })
    )
    .optional()
    .describe('States that are allowed as transitions from this State'),
});

export const updateStateParameters = z.object({
  id: z.string().optional().describe('The ID of the State to update'),
  key: z.string().optional().describe('The key of the State to update'),
  version: z.number().int().describe('Current version of the State for optimistic concurrency'),
  actions: z
    .array(
      z
        .object({action: z.string().describe('The update action type')})
        .and(z.record(z.string(), z.any()))
    )
    .describe(
      'List of update actions. Supported actions: addRoles, removeRoles, setRoles, changeKey, changeType, changeInitial, setName, setDescription, setTransitions'
    ),
});
