interface FieldFilteringManager {
  /**
   * Recursively dives into an object, filtering and redacting specified properties.
   */
  filterFields<T>(data: T): T extends number | boolean ? string | T : T;
  /**
   * Filters and redacts specified properties from the url query.
   */
  filterUrlFields(url: string): string;
}

export {type FieldFilteringManager};
