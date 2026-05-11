import {z} from 'zod';

export const readApprovalRuleParameters = z.object({
  id: z.string().optional().describe('The ID of the Approval Rule to fetch'),
  key: z.string().optional().describe('The key of the Approval Rule to fetch'),
  where: z
    .array(z.string())
    .optional()
    .describe('Query predicates for filtering Approval Rules'),
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
  expand: z.array(z.string()).optional().describe('References to expand'),
  associateId: z
    .string()
    .optional()
    .describe('Associate ID — required when using admin context'),
  businessUnitKey: z
    .string()
    .optional()
    .describe('Business Unit key — required when using admin context'),
});

export const createApprovalRuleParameters = z.object({
  name: z.string().describe('Name of the Approval Rule'),
  predicate: z
    .string()
    .describe('Predicate that must match for the rule to trigger'),
  approvers: z
    .record(z.string(), z.any())
    .describe('Approver hierarchy — tiers of approver groups'),
  requesters: z
    .array(z.record(z.string(), z.any()))
    .describe('Requesters who must comply with this Approval Rule'),
  status: z
    .enum(['Active', 'Inactive'])
    .describe('Whether the Approval Rule is Active or Inactive'),
  key: z
    .string()
    .optional()
    .describe('User-defined unique identifier for the Approval Rule'),
  description: z
    .string()
    .optional()
    .describe('Description of the Approval Rule'),
  associateId: z
    .string()
    .optional()
    .describe('Associate ID — required when using admin context'),
  businessUnitKey: z
    .string()
    .optional()
    .describe('Business Unit key — required when using admin context'),
});

export const updateApprovalRuleParameters = z.object({
  id: z.string().optional().describe('The ID of the Approval Rule to update'),
  key: z.string().optional().describe('The key of the Approval Rule to update'),
  version: z
    .number()
    .int()
    .min(0)
    .describe(
      'Current version of the Approval Rule for optimistic concurrency'
    ),
  actions: z
    .array(
      z
        .object({action: z.string().describe('The update action type')})
        .and(z.record(z.string(), z.any()))
    )
    .describe(
      'List of update actions. Supported actions: setApprovers, setRequesters, setName, setDescription, setPredicate, setStatus, setKey, setCustomField, setCustomType'
    ),
  associateId: z
    .string()
    .optional()
    .describe('Associate ID — required when using admin context'),
  businessUnitKey: z
    .string()
    .optional()
    .describe('Business Unit key — required when using admin context'),
});
