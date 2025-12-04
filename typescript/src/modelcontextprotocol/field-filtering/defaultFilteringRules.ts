import {FieldFilteringManagerConfig} from './FieldFilteringManagerConfig';

const defaultJsonRedactionText = '[REDACTED]';
const defaultUrlRedactionText = 'REDACTED';

const defaultFilteringRules: FieldFilteringManagerConfig = {
  includes: [{value: 'password', caseSensitive: false, type: 'redact'}],
  properties: [],
  jsonRedactionText: defaultJsonRedactionText,
  urlRedactionText: defaultUrlRedactionText,
};

export {
  defaultFilteringRules,
  defaultJsonRedactionText,
  defaultUrlRedactionText,
};
