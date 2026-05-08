export const readApprovalFlowPrompt = `
This tool fetches Approval Flow information from commercetools.

Approval Flows connect Orders that require approval with the Approval Rules that initiated the requirement. They represent the approval process including approvals, rejections, and all involved parties.

It can be used in two ways:
1. Fetch a single Approval Flow by its ID
2. Query multiple Approval Flows using filter predicates

**Parameters:**
- id (string, optional): The ID of the Approval Flow to fetch
- where (string array, optional): Query predicates for filtering, e.g. ["status=\\"Pending\\""]
- limit (int, optional): Maximum number of results to return (default: 10, range: 1-500)
- offset (int, optional): Number of results to skip for pagination
- sort (string array, optional): Sort expressions, e.g. ["createdAt desc"]
- expand (string array, optional): References to expand, e.g. ["order"]
- associateId (string, optional): Associate ID — required when using admin context to act on behalf of an associate
- businessUnitKey (string, optional): Business Unit key — required when using admin context

**Associate context:** When operating as an associate, the associateId and businessUnitKey are taken from the session context automatically.

**Status values:** Pending, Approved, Rejected
`;

export const updateApprovalFlowPrompt = `
This tool updates an Approval Flow in commercetools using update actions.

Common use cases include approving or rejecting an order approval flow, or managing custom fields on the flow.

**Parameters:**
- id (string, required): The ID of the Approval Flow to update
- version (int, required): Current version of the Approval Flow (for optimistic concurrency control)
- actions (array, required): List of update actions to apply
- associateId (string, optional): Associate ID — required when using admin context
- businessUnitKey (string, optional): Business Unit key — required when using admin context

**Supported update actions:**
- approve: Approve the Approval Flow. The Associate's roles are matched against the Approval Rules hierarchy.
- reject: Reject the Approval Flow, setting its status to Rejected. Accepts an optional "reason" field.
- setCustomField: Set a custom field. Requires "name" (string) and optional "value" fields.
- setCustomType: Set or remove the custom type. Accepts optional "type" (TypeResourceIdentifier) and "fields" (FieldContainer).

**Example — approve:**
{ "action": "approve" }

**Example — reject with reason:**
{ "action": "reject", "reason": "Budget exceeded" }

**Example — set custom field:**
{ "action": "setCustomField", "name": "reviewNote", "value": "Approved after review" }
`;
