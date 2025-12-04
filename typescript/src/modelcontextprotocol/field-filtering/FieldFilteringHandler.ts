import {
  defaultJsonRedactionText,
  defaultUrlRedactionText,
} from './defaultFilteringRules';
import {isValidUrl} from './urlHelpers';
import {FieldFilteringManager} from './FieldFilteringManager';
import {FieldFilteringManagerConfig} from './FieldFilteringManagerConfig';
import {FieldFilteringRule} from './FieldFilteringRule';

class FieldFilteringHandler implements FieldFilteringManager {
  paths: FieldFilteringRule[];
  properties: FieldFilteringRule[];
  whitelistPaths: FieldFilteringRule[];
  includes: FieldFilteringRule[];
  jsonRedactionText: string;
  urlRedactionText: string;

  constructor(config: FieldFilteringManagerConfig) {
    this.paths = config.paths ?? [];
    this.properties = config.properties ?? [];
    this.whitelistPaths = config.whitelistPaths ?? [];
    this.includes = config.includes ?? [];
    this.jsonRedactionText =
      config.jsonRedactionText ?? defaultJsonRedactionText;
    this.urlRedactionText = config.urlRedactionText ?? defaultUrlRedactionText;
  }

  filter<T>(
    data: T,
    currentPath?: string
  ): T extends number | boolean ? string | T : T {
    if (
      typeof data === 'string' ||
      typeof data === 'number' ||
      typeof data === 'boolean' ||
      typeof data === 'bigint'
    ) {
      if (this.shouldRedact(currentPath ?? '')) {
        return this.jsonRedactionText as any;
      }
      if (typeof data === 'string' && isValidUrl(data)) {
        return this.filterUrl(data) as any;
      }
      return data as any;
    }

    if (typeof data === 'object') {
      // TODO CHECK TO BE FILTERED AND REMOVE/CENSOR
      if (Array.isArray(data)) {
        return data.map((datum) => this.filter(datum, currentPath)) as any;
      } else if (data) {
        Object.keys(data).forEach((key) => {
          (data as any)[key] = this.filter(
            data[key as keyof T],
            currentPath ? `${currentPath}.${key}` : key
          );
        });
        return data as any;
      }
    }
    return data as any;
  }

  filterUrl(inputUrl: string): string {
    const url = new URL(inputUrl);
    const urlParams = new URLSearchParams(url.search);
    for (let [key] of urlParams.entries()) {
      if (this.shouldRedact(this.urlQueryKeyToObjectPath(key))) {
        urlParams.set(key, this.urlRedactionText);
      }
    }

    url.search = urlParams.toString();

    return url.toString();
  }

  // assumes keys of string only
  private urlQueryKeyToObjectPath(urlQueryKey: string): string {
    let urlQueryKeyOpenBracketSplit = urlQueryKey.split('[');
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
          return;
        } else {
          if (closeBracketSplit[0].match(/^-?\d+$/)) {
            return;
          } else {
            objectPath += `.${closeBracketSplit[0]}`;
          }
        }
      });
      return objectPath;
    }
  }

  private shouldRedact(path: string): boolean {
    let ruleIsSatisfied = this.testFilterRules(path, this.whitelistPaths);
    if (ruleIsSatisfied) {
      return false;
    }

    ruleIsSatisfied = this.testFilterRules(path, this.paths);
    if (ruleIsSatisfied) {
      return true;
    }

    const properties = path.split('.');
    const propertyName = properties[properties.length - 1];

    ruleIsSatisfied = this.testFilterRules(propertyName, this.properties);
    if (ruleIsSatisfied) {
      return true;
    }

    for (let n = 0; n < this.includes.length; n++) {
      if (
        propertyName.includes(this.includes[n].value) ||
        (!this.includes[n].caseSensitive &&
          propertyName
            .toLowerCase()
            .includes(this.includes[n].value.toLowerCase()))
      ) {
        n = this.includes.length;
        ruleIsSatisfied = true;
      }
    }
    return ruleIsSatisfied;
  }

  // checks regardless of "filter" | "redact"
  private testFilterRules(path: string, rules: FieldFilteringRule[]): boolean {
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
}

export {FieldFilteringHandler};
