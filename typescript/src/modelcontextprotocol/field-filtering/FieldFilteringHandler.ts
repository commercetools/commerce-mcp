import {
  defaultJsonRedactionText,
  defaultUrlRedactionText,
} from './defaultFilteringRules';
import {isValidUrl} from './urlHelpers';
import {FieldFilteringManager} from './FieldFilteringManager';
import {FieldFilteringManagerConfig} from './FieldFilteringManagerConfig';
import {FieldFilteringRule} from './FieldFilteringRule';

class FieldFilteringHandler implements FieldFilteringManager {
  filterPaths: FieldFilteringRule[];
  redactPaths: FieldFilteringRule[];
  filterProperties: FieldFilteringRule[];
  redactProperties: FieldFilteringRule[];
  whitelistPaths: Omit<FieldFilteringRule, 'type'>[];
  filterIncludes: FieldFilteringRule[];
  redactIncludes: FieldFilteringRule[];
  jsonRedactionText: string;
  urlRedactionText: string;

  constructor(config: FieldFilteringManagerConfig) {
    this.filterPaths =
      config.paths?.filter((path) => path.type === 'filter') ?? [];
    this.redactPaths =
      config.paths?.filter((path) => path.type === 'redact') ?? [];
    this.filterProperties =
      config.properties?.filter((path) => path.type === 'filter') ?? [];
    this.redactProperties =
      config.properties?.filter((path) => path.type === 'redact') ?? [];
    this.whitelistPaths = config.whitelistPaths ?? [];
    this.filterIncludes =
      config.includes?.filter((path) => path.type === 'filter') ?? [];
    this.redactIncludes =
      config.includes?.filter((path) => path.type === 'redact') ?? [];

    this.jsonRedactionText =
      config.jsonRedactionText ?? defaultJsonRedactionText;
    this.urlRedactionText = config.urlRedactionText ?? defaultUrlRedactionText;
  }

  filterFields<T>(
    data: T,
    currentPath?: string
  ): T extends number | boolean ? string | T : T {
    // if should be redacted, do so regardless of type. Filtered object properties are handled one loop up
    if (this.filterConditionMet(currentPath ?? '', 'redact')) {
      return this.jsonRedactionText as any;
    }
    if (typeof data === 'string') {
      // if string, check if value is url, is so check the params
      if (isValidUrl(data)) {
        return this.filterUrlFields(data) as any;
      }
      return data as any;
    }

    if (typeof data === 'object') {
      if (Array.isArray(data)) {
        return data.map((datum) =>
          this.filterFields(datum, currentPath)
        ) as any;
      } else if (data) {
        Object.keys(data).forEach((key) => {
          const newPath = currentPath ? `${currentPath}.${key}` : key;
          if (this.filterConditionMet(newPath, 'filter')) {
            delete data[key as keyof T];
          } else {
            (data as any)[key] = this.filterFields(
              data[key as keyof T],
              newPath
            );
          }
        });
        return data as any;
      }
    }
    return data as any;
  }

  private filterConditionMet(path: string, type: 'redact' | 'filter'): boolean {
    // if path is whitelisted, do not filter
    let ruleIsSatisfied = this.testFilterRules(path, this.whitelistPaths);
    if (ruleIsSatisfied) {
      return false;
    }

    ruleIsSatisfied = this.testFilterRules(path, this[`${type}Paths`]);
    if (ruleIsSatisfied) {
      return true;
    }

    const properties = path.split('.');
    const propertyName = properties[properties.length - 1];

    ruleIsSatisfied = this.testFilterRules(
      propertyName,
      this[`${type}Properties`]
    );
    if (ruleIsSatisfied) {
      return true;
    }

    const includes = this[`${type}Includes`];
    for (let n = 0; n < includes.length; n++) {
      if (
        propertyName.includes(includes[n].value) ||
        (!includes[n].caseSensitive &&
          propertyName.toLowerCase().includes(includes[n].value.toLowerCase()))
      ) {
        n = includes.length;
        ruleIsSatisfied = true;
      }
    }
    return ruleIsSatisfied;
  }

  // checks regardless of "filter" | "redact"
  private testFilterRules(
    path: string,
    rules: Omit<FieldFilteringRule, 'type'>[]
  ): boolean {
    let ruleIsSatisfied = false;
    for (let n = 0; n < rules.length; n++) {
      if (
        path === rules[n].value ||
        (!rules[n].caseSensitive &&
          path.toLowerCase() === rules[n].value.toLowerCase())
      ) {
        n = rules.length;
        ruleIsSatisfied = true;
      }
    }
    return ruleIsSatisfied;
  }

  filterUrlFields(inputUrl: string): string {
    const url = new URL(inputUrl);
    const urlParams = new URLSearchParams(url.search);
    console.log('urlParams.entries(): ', urlParams.entries());
    const keysToDelete: string[] = [];
    for (const [key, _] of urlParams.entries()) {
      if (
        this.filterConditionMet(this.urlQueryKeyToObjectPath(key), 'filter')
      ) {
        // must be added to an array and deleted after loop for case sensitivity
        keysToDelete.push(key);
      } else if (
        this.filterConditionMet(this.urlQueryKeyToObjectPath(key), 'redact')
      ) {
        urlParams.set(key, this.urlRedactionText);
      }
    }
    keysToDelete.forEach((key) => urlParams.delete(key));

    url.search = urlParams.toString();

    return url.toString();
  }

  // assumes keys of string only
  private urlQueryKeyToObjectPath(urlQueryKey: string): string {
    const urlQueryKeyOpenBracketSplit = urlQueryKey.split('[');
    if (urlQueryKeyOpenBracketSplit.length === 1) {
      return urlQueryKey;
    } else {
      let objectPath: string = urlQueryKeyOpenBracketSplit.splice(0, 1)[0];

      urlQueryKeyOpenBracketSplit.forEach((openBracketSplitValue, n) => {
        const closeBracketSplit = openBracketSplitValue.split(']');
        if (closeBracketSplit.length !== 2) {
          console.warn(
            `Object in URL params in incorrect format: [${urlQueryKeyOpenBracketSplit[n]}`
          );
        } else {
          if (!closeBracketSplit[0].match(/^-?\d+$/)) {
            objectPath += `.${closeBracketSplit[0]}`;
          }
        }
      });
      return objectPath;
    }
  }
}

export {FieldFilteringHandler};
