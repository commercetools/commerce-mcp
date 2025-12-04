import qs from 'qs';

type BasicTypes = string | number | boolean;

type AcceptedQueryValueTypes =
  | BasicTypes
  | AcceptedQueryValueTypes[]
  | {
      [key: string]: AcceptedQueryValueTypes;
    };

type AcceptedQueryTypes = {
  [key: string]: AcceptedQueryValueTypes;
};

const normaliseUrl = function (url: string): string {
  let protocolSplit = url.split('//');
  let normalisedUrl = '';
  if (
    protocolSplit[0] &&
    (protocolSplit[0] === 'http:' ||
      protocolSplit[0] === 'https:' ||
      protocolSplit[0] === 'ws:' ||
      protocolSplit[0] === 'wss:')
  ) {
    normalisedUrl = `${protocolSplit[0]}//`;
    protocolSplit.splice(0, 1);
  }

  let query = '';
  let querySplit = protocolSplit.join('//').split('?');
  if (querySplit.length > 1) {
    query = `?${querySplit.slice(1, querySplit.length).join('?')}`;
  }
  const pathSplit = querySplit[0].split('/');

  for (let n = 0; n < pathSplit.length; n++) {
    if (pathSplit[n]) {
      normalisedUrl += `${pathSplit[n]}/`;
    }
  }

  normalisedUrl = normalisedUrl.substring(0, normalisedUrl.length - 1);
  return normalisedUrl + query;
};

const toQueryObject = function (
  key: string,
  value: AcceptedQueryValueTypes
): AcceptedQueryTypes {
  let obj: any = {};
  obj[key] = value;
  return obj;
};

const toQueryString = function (obj: AcceptedQueryTypes): string {
  return qs.stringify(obj, {
    arrayFormat: 'indices',
    encodeValuesOnly: true,
    format: 'RFC3986',
  });
};

const generateQueryString = function (query: AcceptedQueryTypes): string {
  let queryString = '?';

  Object.keys(query).forEach((key) => {
    let value = query[key];
    if (value !== undefined && typeof value !== 'function') {
      if (value === null) {
        queryString += `${key}=null&`;
      } else {
        queryString += `${toQueryString(toQueryObject(key, value))}&`;
      }
    }
  });
  // removes trailing &, or ? if empty query
  queryString = queryString.substring(0, queryString.length - 1);

  return queryString;
};

const isValidUrl = function (urlLike: string): boolean {
  let url: URL;
  try {
    url = new URL(urlLike);
  } catch (_) {
    return false;
  }
  return true;
};

export {normaliseUrl, generateQueryString, isValidUrl};
