import {FieldFilteringManager} from './FieldFilteringManager';
import {FieldFilteringManagerConfig} from './FieldFilteringManagerConfig';
import {FieldFilteringHandler} from './FieldFilteringHandler';
import {FieldFilteringRule} from './FieldFilteringRule';

const isFieldFilteringManager = (
  config?: FieldFilteringManager | FieldFilteringManagerConfig
): config is FieldFilteringManager => {
  return Boolean(
    (config as FieldFilteringManager)?.filterFields &&
      (config as FieldFilteringManager)?.filterUrlFields
  );
};

export {
  type FieldFilteringManager,
  type FieldFilteringManagerConfig,
  type FieldFilteringRule,
  FieldFilteringHandler,
  isFieldFilteringManager,
};
