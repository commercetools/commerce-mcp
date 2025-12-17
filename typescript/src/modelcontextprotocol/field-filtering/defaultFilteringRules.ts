import {FieldFilteringManagerConfig} from './FieldFilteringManagerConfig';

const defaultJsonRedactionText = '[REDACTED]';
const defaultUrlRedactionText = 'REDACTED';

const defaultFilteringRules: FieldFilteringManagerConfig = {
  jsonRedactionText: defaultJsonRedactionText,
  urlRedactionText: defaultUrlRedactionText,
};

export {
  defaultFilteringRules,
  defaultJsonRedactionText,
  defaultUrlRedactionText,
};
