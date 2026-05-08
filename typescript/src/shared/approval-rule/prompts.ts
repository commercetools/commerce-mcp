export const readApprovalRulePrompt = `
This tool fetches Approval Rule information from commercetools.

Approval Rules define when Orders require approval within a Business Unit and who must approve them. Rules match Orders based on a predicate and specify an approver hierarchy.

It can be used in three ways:
1. Fetch a single Approval Rule by its ID
2. Fetch a single Approval Rule by its key
3. Query multiple Approval Rules using filter predicates

**Parameters:**
- id (string, optional): The ID of the Approval Rule to fetch
- key (string, optional): The key of the Approval Rule to fetch
- where (string array, optional): Query predicates for filtering, e.g. ["status=\\"Active\\""]
- limit (int, optional): Maximum number of results to return (default: 10, range: 1-500)
- offset (int, optional): Number of results to skip for pagination
- sort (string array, optional): Sort expressions, e.g. ["createdAt desc"]
- expand (string array, optional): References to expand
- associateId (string, optional): Associate ID — required when using admin context
- businessUnitKey (string, optional): Business Unit key — required when using admin context

**Associate context:** When operating as an associate, associateId and businessUnitKey are taken from session context automatically.
`;

export const createApprovalRulePrompt = `
This tool creates a new Approval Rule in commercetools.

Approval Rules trigger an approval workflow when an Order in a Business Unit matches the rule's predicate. The rule specifies which Associates must approve and who is subject to the rule.

**Parameters:**
- name (string, required): Name of the Approval Rule
- predicate (string, required): Order predicate that triggers the rule, e.g. "totalPrice > \\"1000 EUR\\""
- approvers (object, required): ApproverHierarchy — tiers of approver groups
- requesters (array, required): List of AssociateRoleKeyReference objects representing who the rule applies to
- status (string, required): "Active" or "Inactive"
- key (string, optional): User-defined unique identifier within the Business Unit
- description (string, optional): Description of the Approval Rule
- associateId (string, optional): Associate ID — required when using admin context
- businessUnitKey (string, optional): Business Unit key — required when using admin context
`;

export const updateApprovalRulePrompt = `
This tool updates an Approval Rule in commercetools using update actions.

Either the ID or key must be provided to identify the rule to update.

**Parameters:**
- id (string, optional): The ID of the Approval Rule to update
- key (string, optional): The key of the Approval Rule to update
- version (int, required): Current version of the Approval Rule (for optimistic concurrency control)
- actions (array, required): List of update actions to apply
- associateId (string, optional): Associate ID — required when using admin context
- businessUnitKey (string, optional): Business Unit key — required when using admin context

**Supported update actions:**
- setApprovers: Set the approver hierarchy. Requires "approvers" field.
- setRequesters: Set who the rule applies to. Requires "requesters" array.
- setName: Set the name. Requires "name" field.
- setDescription: Set the description. Requires "description" field.
- setPredicate: Set the order predicate. Requires "predicate" field.
- setStatus: Set Active or Inactive. Requires "status" field.
- setKey: Set the key. Requires "key" field.
- setCustomField: Set a custom field. Requires "name" and optional "value" fields.
- setCustomType: Set or remove the custom type.
`;
