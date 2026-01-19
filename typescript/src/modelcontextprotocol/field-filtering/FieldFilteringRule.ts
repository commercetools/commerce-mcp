interface FieldFilteringRule {
  /**
   * A string representing the property value in which to apply the rule.
   */
  value: string;
  /**
   * A boolean dictating whether to apply the rule value with case sensitivity.
   */
  caseSensitive: boolean;
  /**
   * A string of value "filter" or "redact". Specify "filter" to remove the whole key and value,
   * or "redact" to replace the value with the redaction text, leaving the key for context.
   */
  type: 'filter' | 'redact';
}

export {type FieldFilteringRule};
