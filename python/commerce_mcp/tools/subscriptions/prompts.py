READ_SUBSCRIPTION_PROMPT = """
Read subscriptions from the commercetools platform. You can:
- Get a single subscription by providing either its ID or key
- List multiple subscriptions with optional filtering, sorting, and pagination

Parameters:
- id: The ID of a specific subscription to retrieve (optional)
- key: The key of a specific subscription to retrieve (optional)
- limit: Number of results requested when listing (default: 20, max: 500)
- offset: Number of elements to skip when listing (default: 0, max: 10000)
- sort: Sort criteria for listing results (e.g., ["key asc", "createdAt desc"])
- where: Query predicates for filtering when listing (e.g., ["key=\\"my-subscription\\""])
- expand: Reference paths to expand (e.g., ["destination", "changes"])

Examples:
// Get by ID
subscription.read({
  id: "subscription-123"
})
// Get by key
subscription.read({
  key: "my-subscription"
})
// List with limit and sort
subscription.read({
  limit: 10,
  sort: ["createdAt desc"]
})
"""

CREATE_SUBSCRIPTION_PROMPT = """
Create a new subscription in the commercetools platform.

Parameters:
- key: User-defined unique identifier for the subscription (string, optional, pattern: ^[A-Za-z0-9_-]+$)
- destination: Destination where the messages should be sent (object, required)
  - SQS destination:
    - type: "SQS" (required)
    - queueUrl: URL of the SQS queue (string, required)
    - region: AWS region where the queue is located (string, required)
    - accessKey: AWS access key for authentication (string, optional)
    - accessSecret: AWS access secret for authentication (string, optional)
  - SNS destination:
    - type: "SNS" (required)
    - topicArn: ARN of the SNS topic (string, required)
    - accessKey: AWS access key for authentication (string, optional)
    - accessSecret: AWS access secret for authentication (string, optional)
  - Google Cloud Pub/Sub destination:
    - type: "GoogleCloudPubSub" (required)
    - projectId: Google Cloud project ID (string, required)
    - topic: Pub/Sub topic name (string, required)
  - Azure Event Grid destination:
    - type: "AzureEventGrid" (required)
    - uri: URI of the Event Grid topic (string, required)
    - accessKey: Azure Event Grid access key (string, optional)
  - Azure Service Bus destination:
    - type: "AzureServiceBus" (required)
    - connectionString: Azure Service Bus connection string (string, required)
  - RabbitMQ destination:
    - type: "RabbitMQ" (required)
    - uri: RabbitMQ URI (string, required)
- changes: Array of resource types for change subscriptions (array of objects, optional)
  - resourceTypeId: Resource type for change subscription (required)
- messages: Array of message subscriptions for specific resource types and message types (array of objects, optional)
  - resourceTypeId: Resource type of the subscription (required)
  - types: Message types to subscribe to (array of strings, optional)
- format: Format of the subscription message (object, optional)
  - type: "Platform" or "CloudEvents" (required)
  - cloudEventsVersion: CloudEvents version (string, optional)

Examples:
// Create an SQS subscription for order changes
subscription.create({
  key: "order-changes-sqs",
  destination: {
    type: "SQS",
    queueUrl: "https://sqs.us-east-1.amazonaws.com/123456789012/my-queue",
    region: "us-east-1"
  },
  changes: [
    {
      resourceTypeId: "order"
    }
  ]
})
// Create a Google Cloud Pub/Sub subscription
subscription.create({
  key: "product-messages-pubsub",
  destination: {
    type: "GoogleCloudPubSub",
    projectId: "my-project",
    topic: "my-topic"
  },
  messages: [
    {
      resourceTypeId: "product",
      types: ["ProductCreated", "ProductUpdated"]
    }
  ],
  format: {
    type: "CloudEvents"
  }
})
"""

UPDATE_SUBSCRIPTION_PROMPT = """
Update an existing subscription in the commercetools platform. You must provide either the 'id' or 'key' of the subscription to update, along with its current 'version' and an array of 'actions' to apply.

Parameters:
- id: The ID of the subscription to update (string, required if key is not provided)
- key: The key of the subscription to update (string, required if id is not provided)
- version: The current version of the subscription (number, required)
- actions: An array of update actions to apply to the subscription (array of objects, required)
  - changeDestination: Change the destination configuration (object with destination field)
  - setKey: Set or change the key of the subscription (object with optional key field)
  - setChanges: Change the changes configuration (object with changes array field)
  - setMessages: Change the messages configuration (object with messages array field)
  - setMessageFormat: Set or change the message format (object with format field)

Examples:
// Change the destination by ID
subscription.update({
  id: "subscription-123",
  version: 1,
  actions: [
    {
      action: "changeDestination",
      destination: {
        type: "SQS",
        queueUrl: "https://sqs.us-east-1.amazonaws.com/123456789012/new-queue",
        region: "us-east-1"
      }
    }
  ]
})
// Set changes by key
subscription.update({
  key: "my-subscription",
  version: 2,
  actions: [
    {
      action: "setChanges",
      changes: [
        {
          resourceTypeId: "cart"
        },
        {
          resourceTypeId: "order"
        }
      ]
    }
  ]
})
"""
