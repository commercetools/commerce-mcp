export const readOrderEditPrompt = `
This tool fetches Order Edit information from commercetools.

Order Edits allow staged modifications to existing Orders. Changes are captured as staged actions and can be reviewed before applying them to the actual Order.

It can be used in three ways:
1. Fetch a single Order Edit by its ID
2. Fetch a single Order Edit by its key
3. Query multiple Order Edits using filter predicates

**Parameters:**
- id (string, optional): The ID of the Order Edit to fetch
- key (string, optional): The key of the Order Edit to fetch
- where (string array, optional): Query predicates for filtering
- limit (int, optional): Maximum number of results to return (default: 10, range: 1-500)
- offset (int, optional): Number of results to skip for pagination
- sort (string array, optional): Sort expressions, e.g. ["createdAt desc"]
- expand (string array, optional): References to expand, e.g. ["resource"]

**Admin context only.**
`;

export const createOrderEditPrompt = `
This tool creates a new Order Edit in commercetools.

An Order Edit captures staged modifications to an existing Order. The staged actions are not applied to the Order until the edit is explicitly applied using the apply_order_edit tool.

**Parameters:**
- resource (object, required): Reference to the Order being edited: { id: "<orderId>", typeId: "order" }
- stagedActions (array, optional): Order update actions to stage for later application
- key (string, optional): User-defined unique identifier for this Order Edit
- comment (string, optional): Description of the changes
- dryRun (boolean, optional): If true, validates without persisting
- custom (object, optional): Custom fields

**Admin context only.**
`;

export const updateOrderEditPrompt = `
This tool updates an Order Edit in commercetools using update actions.

Either the ID or key must be provided. These actions modify the Order Edit itself (not the Order), for example adding more staged actions or changing metadata.

**Parameters:**
- id (string, optional): The ID of the Order Edit to update
- key (string, optional): The key of the Order Edit to update
- version (int, required): Current version of the Order Edit (for optimistic concurrency control)
- actions (array, required): List of update actions to apply
- dryRun (boolean, optional): If true, validates without persisting

**Supported update actions:**
- addStagedAction: Add a single staged order action. Requires "stagedAction" field.
- setStagedActions: Replace all staged actions. Requires "stagedActions" array.
- setComment: Set the comment. Requires "comment" field.
- setKey: Set the key. Requires "key" field.
- setCustomField: Set a custom field. Requires "name" and optional "value" fields.
- setCustomType: Set or remove the custom type. Requires optional "type" and "fields".

**Admin context only.**
`;

export const applyOrderEditPrompt = `
This tool applies an Order Edit to its target Order in commercetools.

Applying an Order Edit executes all the staged actions against the Order, modifying it permanently. Both the edit version and the current Order version must be provided for optimistic concurrency control.

**Parameters:**
- id (string, required): The ID of the Order Edit to apply
- editVersion (int, required): The version of the Order Edit
- resourceVersion (int, required): The current version of the Order that will be modified

**Admin context only.**
`;
