import {contextToZoneFunctionMapping} from '../functions';
import * as admin from '../admin.functions';

describe('Zone Context Mapping', () => {
  test('should return admin functions when isAdmin is true', () => {
    const context = {isAdmin: true};
    const mapping = contextToZoneFunctionMapping(context);

    expect(mapping).toEqual({
      read_zones: admin.readZone,
      create_zones: admin.createZone,
      update_zones: admin.updateZone,
    });
  });

  test('should return empty object when no context is provided', () => {
    const mapping = contextToZoneFunctionMapping();
    expect(mapping).toEqual({});
  });

  test('should return empty object when context has no relevant properties', () => {
    const context = {};
    const mapping = contextToZoneFunctionMapping(context);
    expect(mapping).toEqual({});
  });
});
