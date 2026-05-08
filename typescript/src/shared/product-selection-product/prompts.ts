export const readProductSelectionProductPrompt = `
This tool fetches products assigned to a Product Selection in commercetools.

Product Selections group products for targeted visibility in Stores. This tool retrieves the list of products assigned to a specific Product Selection.

Either productSelectionId or productSelectionKey must be provided.

**Parameters:**
- productSelectionId (string, optional): The ID of the Product Selection
- productSelectionKey (string, optional): The key of the Product Selection
- where (string array, optional): Query predicates for filtering assigned products
- limit (int, optional): Maximum number of results to return (default: 10, range: 1-500)
- offset (int, optional): Number of results to skip for pagination
- sort (string array, optional): Sort expressions, e.g. ["createdAt desc"]
- expand (string array, optional): References to expand, e.g. ["product"]

**Response:** Returns AssignedProductPagedQueryResponse with items containing:
- product: ProductReference
- variantSelection (optional): Which variants are included
- variantExclusion (optional): Which variants are excluded

**Available for admin and store contexts.**
`;
