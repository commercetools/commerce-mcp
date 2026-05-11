export const readRecurrencePolicyPrompt = `
This tool fetches Recurrence Policy information from commercetools.

Recurrence Policies define the schedule for recurring orders, specifying how often and when orders should repeat.

It can be used in three ways:
1. Fetch a single Recurrence Policy by its ID
2. Fetch a single Recurrence Policy by its key
3. Query multiple Recurrence Policies using filter predicates

**Parameters:**
- id (string, optional): The ID of the Recurrence Policy to fetch
- key (string, optional): The key of the Recurrence Policy to fetch
- where (string array, optional): Query predicates for filtering
- limit (int, optional): Maximum number of results to return (default: 10, range: 1-500)
- offset (int, optional): Number of results to skip for pagination
- sort (string array, optional): Sort expressions, e.g. ["createdAt desc"]
- expand (string array, optional): References to expand

**Admin context only.**
`;

export const createRecurrencePolicyPrompt = `
This tool creates a new Recurrence Policy in commercetools.

Recurrence Policies define schedules for recurring orders. A schedule can be either a standard (interval-based) or a day-of-month schedule.

**Parameters:**
- key (string, required): User-defined unique identifier
- schedule (object, required): Schedule configuration with a "type" field. Use type "standard" for interval-based or "dayOfMonth" for calendar-based scheduling.
- name (object, optional): Localized name, e.g. {"en": "Monthly Policy"}
- description (object, optional): Localized description

**Schedule examples:**
Standard schedule: { "type": "standard", "interval": 30, "unit": "Day" }
Day-of-month schedule: { "type": "dayOfMonth", "day": 15, "months": [1, 6] }

**Admin context only.**
`;

export const updateRecurrencePolicyPrompt = `
This tool updates a Recurrence Policy in commercetools using update actions.

Either the ID or key must be provided to identify the policy to update.

**Parameters:**
- id (string, optional): The ID of the Recurrence Policy to update
- key (string, optional): The key of the Recurrence Policy to update
- version (int, required): Current version of the Recurrence Policy (for optimistic concurrency control)
- actions (array, required): List of update actions to apply

**Supported update actions:**
- setKey: Set a new key. Requires "key" field.
- setName: Set the name. Requires "name" (localized string) field.
- setDescription: Set the description. Requires "description" (localized string) field.
- setSchedule: Change the schedule. Requires "schedule" field.

**Admin context only.**
`;
