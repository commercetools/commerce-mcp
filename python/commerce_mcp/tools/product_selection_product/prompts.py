READ_PRODUCT_SELECTION_PRODUCT_PROMPT = """
Fetch products assigned to a commercetools Product Selection.

It takes these required arguments:
- id (string, optional): The ID of the ProductSelection.
- key (string, optional): The key of the ProductSelection.

Note: Either id or key must be provided.

It takes these optional arguments:
- limit (number, optional): Maximum number of results to return (default: 20, max: 500)
- offset (number, optional): Number of results to skip
- expand (string array, optional): References to expand in the returned objects
- storeKey (string, optional): Key of the store context (for store-scoped access)

Returns an AssignedProductPagedQueryResponse with product references and optional variant selection/exclusion details.
"""
