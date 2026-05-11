export const readStatePrompt = `
This tool fetches State information from commercetools.

States represent custom workflow states that can be applied to Orders, Line Items, Products, Reviews, Payments, Quotes, and Recurring Orders. States enable custom workflow transitions.

It can be used in three ways:
1. Fetch a single State by its ID
2. Fetch a single State by its key
3. Query multiple States using filter predicates

**Parameters:**
- id (string, optional): The ID of the State to fetch
- key (string, optional): The key of the State to fetch
- where (string array, optional): Query predicates for filtering
- limit (int, optional): Maximum number of results to return (default: 10, range: 1-500)
- offset (int, optional): Number of results to skip for pagination
- sort (string array, optional): Sort expressions, e.g. ["createdAt desc"]
- expand (string array, optional): References to expand, e.g. ["transitions[*]"]

**State types:** OrderState, RecurringOrderState, LineItemState, ProductState, ReviewState, PaymentState, QuoteRequestState, StagedQuoteState, QuoteState

**Admin context only.**
`;

export const createStatePrompt = `
This tool creates a new State in commercetools.

States define custom workflow steps for resources. Each State has a type that determines which resource it applies to.

**Parameters:**
- key (string, required): User-defined unique identifier
- type (string, required): The type of the State — determines which resource it applies to.
  Values: OrderState, RecurringOrderState, LineItemState, ProductState, ReviewState, PaymentState, QuoteRequestState, StagedQuoteState, QuoteState
- initial (boolean, optional): Whether this is an initial State. There can be only one initial State per type.
- name (object, optional): Localized name, e.g. {"en": "Processing"}
- description (object, optional): Localized description
- roles (string array, optional): State roles. Only for LineItemState and ReviewState. Values: ReviewIncludedInStatistics, Return
- transitions (object array, optional): Allowed transition targets, each with { id, typeId: "state" }

**Admin context only.**
`;

export const updateStatePrompt = `
This tool updates a State in commercetools using update actions.

Either the ID or key must be provided to identify the State to update.

**Parameters:**
- id (string, optional): The ID of the State to update
- key (string, optional): The key of the State to update
- version (int, required): Current version of the State (for optimistic concurrency control)
- actions (array, required): List of update actions to apply

**Supported update actions:**
- addRoles: Add roles to the State. Requires "roles" array.
- removeRoles: Remove roles from the State. Requires "roles" array.
- setRoles: Set the roles of the State. Requires "roles" array.
- changeKey: Change the key of the State. Requires "key" field.
- changeType: Change the type of the State. Requires "type" field.
- changeInitial: Change whether this is an initial State. Requires "initial" boolean.
- setName: Set the name. Requires "name" (localized string) field.
- setDescription: Set the description. Requires "description" (localized string) field.
- setTransitions: Set allowed transitions. Requires "transitions" array of StateResourceIdentifier, or null to remove restrictions.

**Admin context only.**
`;
