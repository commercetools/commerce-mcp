import {
  defaultJsonRedactionText,
  defaultUrlRedactionText,
} from './defaultFilteringRules';
import {FieldFilteringRule} from './FieldFilteringRule';

/**
 * The configuration object to be passed to the default RedactionHandler.
 */
interface FieldFilteringManagerConfig {
  /**
   * An optional array of explicit object paths to properties to redact. For example "account.users.token".
   */
  paths?: FieldFilteringRule[];
  /**
   * An optional array of property names to redact at any object depth. For example "token".
   */
  properties?: FieldFilteringRule[];
  /**
   * An optional array of explicit object paths to properties to retain, overriding all other rules. For example "account.users.passwordHint".
   */
  whitelistPaths?: Omit<FieldFilteringRule, 'type'>[];
  /**
   *  An optional array of strings, all properties containing these strings will be redacted. For example, "password" would redact "password", "oldPassword" if case-insensitive etc...
   */
  includes?: FieldFilteringRule[];
  /**
   * A string in which to replace redacted properties in JSON objects, default of {@link defaultJsonRedactionText}
   */
  jsonRedactionText?: string;
  /**
   * A string in which to replace redacted properties in url queries, default of {@link defaultUrlRedactionText}
   */
  urlRedactionText?: string;
}

export {type FieldFilteringManagerConfig};
