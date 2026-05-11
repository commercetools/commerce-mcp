import {z} from 'zod';

export const readRecurrencePolicyParameters = z.object({
  id: z
    .string()
    .optional()
    .describe('The ID of the Recurrence Policy to fetch'),
  key: z
    .string()
    .optional()
    .describe('The key of the Recurrence Policy to fetch'),
  where: z
    .array(z.string())
    .optional()
    .describe('Query predicates for filtering Recurrence Policies'),
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
});

export const createRecurrencePolicyParameters = z.object({
  key: z
    .string()
    .describe('User-defined unique identifier for the Recurrence Policy'),
  schedule: z
    .record(z.string(), z.any())
    .describe(
      'Schedule configuration. Use type "standard" for standard schedule or "dayOfMonth" for day-of-month schedule.'
    ),
  name: z
    .record(z.string(), z.string())
    .optional()
    .describe('Localized name of the Recurrence Policy'),
  description: z
    .record(z.string(), z.string())
    .optional()
    .describe('Localized description of the Recurrence Policy'),
});

export const updateRecurrencePolicyParameters = z.object({
  id: z
    .string()
    .optional()
    .describe('The ID of the Recurrence Policy to update'),
  key: z
    .string()
    .optional()
    .describe('The key of the Recurrence Policy to update'),
  version: z
    .number()
    .int()
    .describe(
      'Current version of the Recurrence Policy for optimistic concurrency'
    ),
  actions: z
    .array(
      z
        .object({action: z.string().describe('The update action type')})
        .and(z.record(z.string(), z.any()))
    )
    .describe(
      'List of update actions. Supported actions: setKey, setName, setDescription, setSchedule'
    ),
});
