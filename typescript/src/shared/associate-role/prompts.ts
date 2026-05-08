export const readAssociateRolePrompt = `
This tool fetches Associate Role information from commercetools.

Associate Roles define sets of permissions that can be assigned to Associates within a Business Unit. They control what actions Associates are allowed to perform.

It can be used in three ways:
1. Fetch a single Associate Role by its ID
2. Fetch a single Associate Role by its key
3. Query multiple Associate Roles using filter predicates

**Parameters:**
- id (string, optional): The ID of the Associate Role to fetch
- key (string, optional): The key of the Associate Role to fetch
- where (string array, optional): Query predicates for filtering
- limit (int, optional): Maximum number of results to return (default: 10, range: 1-500)
- offset (int, optional): Number of results to skip for pagination
- sort (string array, optional): Sort expressions, e.g. ["createdAt desc"]
- expand (string array, optional): References to expand

**Available for both admin and associate contexts. Associates can read roles but cannot create or modify them.**
`;

export const createAssociateRolePrompt = `
This tool creates a new Associate Role in commercetools.

Associate Roles bundle permissions that can be assigned to Associates within Business Units.

**Parameters:**
- key (string, required): User-defined unique identifier
- buyerAssignable (boolean, required): Whether this role can be assigned to buyers
- name (string, optional): Display name of the Associate Role
- permissions (string array, optional): List of permissions granted by this role
- custom (object, optional): Custom fields

**Admin context only.**
`;

export const updateAssociateRolePrompt = `
This tool updates an Associate Role in commercetools using update actions.

Either the ID or key must be provided to identify the role to update.

**Parameters:**
- id (string, optional): The ID of the Associate Role to update
- key (string, optional): The key of the Associate Role to update
- version (int, required): Current version of the Associate Role (for optimistic concurrency control)
- actions (array, required): List of update actions to apply

**Supported update actions:**
- addPermission: Add a permission. Requires "permission" field.
- removePermission: Remove a permission. Requires "permission" field.
- setPermissions: Replace all permissions. Requires "permissions" array.
- changeBuyerAssignable: Change buyerAssignable flag. Requires "buyerAssignable" boolean.
- setName: Set the name. Requires "name" field.
- setCustomField: Set a custom field. Requires "name" and optional "value" fields.
- setCustomType: Set or remove the custom type. Requires optional "type" and "fields".

**Admin context only.**
`;
