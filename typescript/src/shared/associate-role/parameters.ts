import {z} from 'zod';

export const readAssociateRoleParameters = z.object({
  id: z.string().optional().describe('The ID of the Associate Role to fetch'),
  key: z.string().optional().describe('The key of the Associate Role to fetch'),
  where: z
    .array(z.string())
    .optional()
    .describe('Query predicates for filtering Associate Roles'),
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

export const createAssociateRoleParameters = z.object({
  key: z
    .string()
    .describe('User-defined unique identifier for the Associate Role'),
  buyerAssignable: z
    .boolean()
    .describe('Whether the Associate Role can be assigned to buyers'),
  name: z.string().optional().describe('Name of the Associate Role'),
  permissions: z
    .array(z.string())
    .optional()
    .describe('List of permissions granted by this Associate Role'),
  custom: z
    .object({
      type: z.object({id: z.string(), typeId: z.literal('type')}),
      fields: z.record(z.string(), z.any()),
    })
    .optional()
    .describe('Custom fields for the Associate Role'),
});

export const updateAssociateRoleParameters = z.object({
  id: z.string().optional().describe('The ID of the Associate Role to update'),
  key: z
    .string()
    .optional()
    .describe('The key of the Associate Role to update'),
  version: z
    .number()
    .int()
    .describe(
      'Current version of the Associate Role for optimistic concurrency'
    ),
  actions: z
    .array(
      z
        .object({action: z.string().describe('The update action type')})
        .and(z.record(z.string(), z.any()))
    )
    .describe(
      'List of update actions. Supported actions: addPermission, removePermission, setPermissions, changeBuyerAssignable, setName, setCustomField, setCustomType'
    ),
});
