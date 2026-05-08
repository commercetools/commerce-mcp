import {z} from 'zod';

export const readOrderEditParameters = z.object({
  id: z.string().optional().describe('The ID of the Order Edit to fetch'),
  key: z.string().optional().describe('The key of the Order Edit to fetch'),
  where: z
    .array(z.string())
    .optional()
    .describe('Query predicates for filtering Order Edits'),
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
    .describe('References to expand, e.g. ["resource"]'),
});

export const createOrderEditParameters = z.object({
  resource: z
    .object({
      id: z.string().describe('The ID of the Order to edit'),
      typeId: z.literal('order'),
    })
    .describe('Reference to the Order being edited'),
  stagedActions: z
    .array(
      z
        .object({action: z.string().describe('The order update action type')})
        .and(z.record(z.string(), z.any()))
    )
    .optional()
    .describe('Order update actions to stage for later application'),
  key: z.string().optional().describe('User-defined unique identifier for the Order Edit'),
  comment: z.string().optional().describe('Message describing the Order Edit'),
  dryRun: z
    .boolean()
    .optional()
    .describe('If true, validates the staged actions without persisting the edit'),
  custom: z
    .object({
      type: z.object({id: z.string(), typeId: z.literal('type')}),
      fields: z.record(z.string(), z.any()),
    })
    .optional()
    .describe('Custom fields for the Order Edit'),
});

export const updateOrderEditParameters = z.object({
  id: z.string().optional().describe('The ID of the Order Edit to update'),
  key: z.string().optional().describe('The key of the Order Edit to update'),
  version: z
    .number()
    .int()
    .describe('Current version of the Order Edit for optimistic concurrency'),
  actions: z
    .array(
      z
        .object({action: z.string().describe('The update action type')})
        .and(z.record(z.string(), z.any()))
    )
    .describe(
      'List of update actions. Supported actions: addStagedAction, setStagedActions, setComment, setKey, setCustomField, setCustomType'
    ),
  dryRun: z
    .boolean()
    .optional()
    .describe('If true, validates the actions without persisting changes'),
});

export const applyOrderEditParameters = z.object({
  id: z.string().describe('The ID of the Order Edit to apply'),
  editVersion: z
    .number()
    .int()
    .describe('The version of the Order Edit to apply'),
  resourceVersion: z
    .number()
    .int()
    .describe('The current version of the Order that will be modified'),
});
