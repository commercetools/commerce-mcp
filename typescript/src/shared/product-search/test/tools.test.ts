import {contextToTools} from '../../tools';
import {contextToProductSearchTools} from '../tools';

describe('tools', () => {
  it('should include product-search tools', () => {
    // Find search_products tool in the combined tools array
    const tools = contextToTools({isAdmin: true});
    const searchProductsTool = tools.find(
      (tool) => tool.method === 'read_product_search'
    );

    const productSearchTools = contextToProductSearchTools({isAdmin: true});

    expect(searchProductsTool).toBeDefined();
    expect(searchProductsTool).toEqual(productSearchTools[0]);
  });

  it('should have correct structure for search_products tool', () => {
    const tools = contextToTools({isAdmin: true});
    const searchProductsTool = tools.find(
      (tool) => tool.method === 'read_product_search'
    );

    expect(searchProductsTool).toMatchObject({
      method: 'read_product_search',
      name: 'Search Products',
      actions: {
        'product-search': {
          read: true,
        },
      },
    });

    // Verify that parameters and description exist
    expect(searchProductsTool?.parameters).toBeDefined();
    expect(searchProductsTool?.description).toBeDefined();
  });
});
