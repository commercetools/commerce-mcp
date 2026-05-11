import {z} from 'zod';

export const readApprovalFlowParameters = z.object({
  id: z.string().optional().describe('The ID of the Approval Flow to fetch'),
  where: z
    .array(z.string())
    .optional()
    .describe(
      'Query predicates for filtering Approval Flows, e.g. ["status=\\"Pending\\""]'
    ),
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
    .describe('References to expand, e.g. ["order"]'),
  customerId: z
    .string()
    .optional()
    .describe('Customer ID (associate ID) — required when using admin context'),
  businessUnitKey: z
    .string()
    .optional()
    .describe('Business Unit key — required when using admin context'),
});

export const updateApprovalFlowParameters = z.object({
  id: z.string().describe('The ID of the Approval Flow to update'),
  version: z
    .number()
    .int()
    .min(0)
    .describe(
      'Current version of the Approval Flow for optimistic concurrency'
    ),
  actions: z
    .array(
      z
        .object({action: z.string().describe('The update action type')})
        .and(z.record(z.string(), z.any()))
    )
    .describe(
      'List of update actions. Supported actions: approve, reject, setCustomField, setCustomType'
    ),
  customerId: z
    .string()
    .optional()
    .describe('Customer ID (associate ID) — required when using admin context'),
  businessUnitKey: z
    .string()
    .optional()
    .describe('Business Unit key — required when using admin context'),
});
