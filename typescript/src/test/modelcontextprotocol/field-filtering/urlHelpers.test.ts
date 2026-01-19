import {
  generateQueryString,
  isValidUrl,
  normaliseUrl,
} from '../../../modelcontextprotocol/field-filtering/urlHelpers';

describe('urlHelpers', () => {
  describe('normaliseUrl', () => {
    test("doesn't error on improper URL", () => {
      expect(() => normaliseUrl('whoops')).not.toThrow();
    });

    test('preserves protocol at the start of the URL', () => {
      const test = 'http://test.com/sub?query=myQuery';
      const test2 = 'https://test.com/sub?query=myQuery';
      const test3 = 'ws://test.com/sub?query=myQuery';
      const test4 = 'wss://test.com/sub?query=myQuery';
      const test5 = 'test.com/sub?query=myQuery';

      expect(normaliseUrl(test)).toBe(test);
      expect(normaliseUrl(test2)).toBe(test2);
      expect(normaliseUrl(test3)).toBe(test3);
      expect(normaliseUrl(test4)).toBe(test4);
      expect(normaliseUrl(test5)).toBe(test5);
    });

    test('removes unwanted slashes', () => {
      const testUrl1 = 'http://domain/page//secondpage';
      const expectedUrl1 = 'http://domain/page/secondpage';
      const testUrl2 = 'http://domain/page//secondpage?param=true';
      const expectedUrl2 = 'http://domain/page/secondpage?param=true';
      const testUrl3 = 'http://domain/page//secondpage/?param=true';
      const expectedUrl3 = 'http://domain/page/secondpage?param=true';

      expect(normaliseUrl(testUrl1)).toBe(expectedUrl1);
      expect(normaliseUrl(testUrl2)).toBe(expectedUrl2);
      expect(normaliseUrl(testUrl3)).toBe(expectedUrl3);
    });

    test("doesn't replace the host when another url is part of the url", () => {
      const url =
        'https://domain.frontastic.rocks/path?param=https://attacker.example';
      const url2 =
        'https://domain.frontastic.rocks/path?param=https://attacker.example?query=true';
      const url3 =
        'domain.frontastic.rocks/path?param=https://attacker.example?query=true';

      expect(normaliseUrl(url)).toBe(url);
      expect(normaliseUrl(url2)).toBe(url2);
      expect(normaliseUrl(url3)).toBe(url3);
    });
  });

  describe('generateQueryString', () => {
    test('ignores function values passed to query without error or serialising', () => {
      const query = {
        myFunc: () => {},
      };
      const expectedQueryString = '';
      // @ts-expect-error
      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });

    test('ignores undefined values passed to query without error or serialising', () => {
      const query = {
        val: undefined,
      };
      const expectedQueryString = '';
      // @ts-expect-error
      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });

    test('serialises null values into query without error', () => {
      const query = {
        val: null,
      };
      const expectedQueryString = '?val=null';
      // @ts-expect-error
      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });

    test('serialises string types into query correctly', () => {
      const query = {
        val1: 'test',
        val2: 'abcdefghijklmnopqrstuvwxyz',
      };
      const expectedQueryString = '?val1=test&val2=abcdefghijklmnopqrstuvwxyz';
      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });

    test('serialises special characters into query correctly', () => {
      const query = {
        spec: ' |\\,./<>?;\'#:@~[]{}-=_+¬`!"£$%^&*()_+',
      };
      const expectedQueryString =
        '?spec=%20%7C%5C%2C.%2F%3C%3E%3F%3B%27%23%3A%40~%5B%5D%7B%7D-%3D_' +
        '%2B%C2%AC%60%21%22%C2%A3%24%25%5E%26%2A%28%29_%2B';
      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });

    test('serialises number types into query correctly', () => {
      const query = {
        val1: 1243567890,
        val2: 345.4334,
      };
      const expectedQueryString = '?val1=1243567890&val2=345.4334';
      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });

    test('serialises boolean types into query correctly', () => {
      const query = {
        val1: true,
        val2: false,
      };
      const expectedQueryString = '?val1=true&val2=false';
      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });

    test('serialises basic objects into query correctly', () => {
      const query = {
        object1: {str: 'string', num: 3, bool: true},
        object2: {str2: 'string2', num: 40, bool2: false},
      };
      const expectedQueryString =
        '?object1[str]=string&object1[num]=3&object1[bool]=true&' +
        'object2[str2]=string2&object2[num]=40&object2[bool2]=false';
      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });

    test('serialises basic array types into query correctly', () => {
      const query = {
        stringArray: ['string 1', 'string 2, with comma', 'string 3'],
        singleStringArray: ['string 1'],
        singleStringArrayWithComma: ['str,ing'],
        numberArray: [43504, 345],
        boolArray: [true, true, false, true],
      };
      const expectedQueryString =
        '?stringArray[0]=string%201&stringArray[1]=string%202%2C%20with%' +
        '20comma&stringArray[2]=string%203&singleStringArray[0]=string%201' +
        '&singleStringArrayWithComma[0]=str%2Cing&numberArray[0]=43504&' +
        'numberArray[1]=345&boolArray[0]=true&boolArray[1]=true&boolArray[2]' +
        '=false&boolArray[3]=true';
      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });

    test('serialises object array types into query correctly', () => {
      const query: any = {
        boolObjArray1: [
          {obj1Bool1: true, obj1Bool2: false},
          {obj2Bool1: true},
          {obj3Bool1: true},
        ],
        numObjArray1: [
          {obj1Num1: 345, obj1Num2: 4.543},
          {obj2Num1: 123},
          {obj3Num1: 564},
        ],
        stringObjArray1: [
          {
            obj1String1: 'Obj 1 String 1',
            obj1String2: 'Obj 1 String2',
          },
          {obj2String1: 'Obj 2 String 1'},
          {obj3String1: 'Obj 3 String 1'},
        ],
        mixedObjArray1: [
          {obj1String1: 'Obj 1 String 1', obj1Num1: 123},
          {obj2String1: 'Obj 2 String 1'},
          {obj3String1: 'Obj 3 String 1', obj3Bool1: true},
        ],
      };
      const expectedQueryString =
        '?boolObjArray1[0][obj1Bool1]=true&boolObjArray1[0][obj1Bool2]=false' +
        '&boolObjArray1[1][obj2Bool1]=true&boolObjArray1[2][obj3Bool1]=true' +
        '&numObjArray1[0][obj1Num1]=345&numObjArray1[0][obj1Num2]=4.543' +
        '&numObjArray1[1][obj2Num1]=123&numObjArray1[2][obj3Num1]=564&' +
        'stringObjArray1[0][obj1String1]=Obj%201%20String%201&stringObjArray1' +
        '[0][obj1String2]=Obj%201%20String2&stringObjArray1[1][obj2String1]=' +
        'Obj%202%20String%201&stringObjArray1[2][obj3String1]=Obj%203%20String' +
        '%201&mixedObjArray1[0][obj1String1]=Obj%201%20String%201&mixedObjArray1' +
        '[0][obj1Num1]=123&mixedObjArray1[1][obj2String1]=Obj%202%20String%201&' +
        'mixedObjArray1[2][obj3String1]=Obj%203%20String%201&mixedObjArray1[2]' +
        '[obj3Bool1]=true';

      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });

    test('serialises complex nested array types into query correctly', () => {
      const query: any = {
        nestedArray: [
          {
            nestedArrObj: {
              nestedArrObjStr: 'Obj 3 String 1',
              nestedArrObjArr: ['string 1', 'string 2, with comma', 'string 3'],
              nestedArrObjObj: {
                nestedArrObjObjArr: ['str,ing'],
                nestedArrObjObjArr2: [
                  [
                    {
                      nestedArrObjObjArr2ArrArrObj: 'string',
                    },
                  ],
                  [
                    {
                      nestedArrObjObjArr2ArrArrObj: 'string',
                    },
                  ],
                ],
              },
            },
          },
          {
            nestedArrObjBool: true,
          },
        ],
      };
      const expectedQueryString =
        '?nestedArray[0][nestedArrObj][nestedArrObjStr]' +
        '=Obj%203%20String%201&nestedArray[0][nestedArrObj][nestedArrObjArr][0]=string' +
        '%201&nestedArray[0][nestedArrObj][nestedArrObjArr][1]=string%202%2C%20with%20' +
        'comma&nestedArray[0][nestedArrObj][nestedArrObjArr][2]=string%203&nestedArray[0]' +
        '[nestedArrObj][nestedArrObjObj][nestedArrObjObjArr][0]=str%2Cing&nestedArray[0]' +
        '[nestedArrObj][nestedArrObjObj][nestedArrObjObjArr2][0][0][nestedArrObjObjArr2ArrArrObj]' +
        '=string&nestedArray[0][nestedArrObj][nestedArrObjObj][nestedArrObjObjArr2][1][0]' +
        '[nestedArrObjObjArr2ArrArrObj]=string&nestedArray[1][nestedArrObjBool]=true';

      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });

    test('serialises complex nested object types into query correctly', () => {
      const query: any = {
        nestedObject: {
          nestedObjObj1: {
            nestedObjObjObj1: {
              nestedObjObjObjStr: 'Obj 3 String 1',
              nestedObjObjObjArr: [
                'string 1',
                'string 2, with comma',
                'string 3',
              ],
              nestedObjObjObj2: {
                nestedObjObjObjArr: ['str,ing'],
                nestedObjObjObjArr2: [
                  [
                    {
                      nestedArrObjObjArr2ArrArrObj: 'string',
                    },
                  ],
                  [
                    {
                      nestedArrObjObjArr2ArrArrObj: 'string',
                    },
                  ],
                ],
              },
            },
          },
          nestedObjObj2: {
            nestedArrObjBool: true,
          },
        },
      };
      const expectedQueryString =
        '?nestedObject[nestedObjObj1][nestedObjObjObj1][nestedObjObjObjStr]=Obj%203%20' +
        'String%201&nestedObject[nestedObjObj1][nestedObjObjObj1][nestedObjObjObjArr][0]' +
        '=string%201&nestedObject[nestedObjObj1][nestedObjObjObj1][nestedObjObjObjArr][1]' +
        '=string%202%2C%20with%20comma&nestedObject[nestedObjObj1][nestedObjObjObj1]' +
        '[nestedObjObjObjArr][2]=string%203&nestedObject[nestedObjObj1][nestedObjObjObj1]' +
        '[nestedObjObjObj2][nestedObjObjObjArr][0]=str%2Cing&nestedObject[nestedObjObj1]' +
        '[nestedObjObjObj1][nestedObjObjObj2][nestedObjObjObjArr2][0][0][nestedArrObjObjA' +
        'rr2ArrArrObj]=string&nestedObject[nestedObjObj1][nestedObjObjObj1][nestedObjObjObj2]' +
        '[nestedObjObjObjArr2][1][0][nestedArrObjObjArr2ArrArrObj]=string&nestedObject' +
        '[nestedObjObj2][nestedArrObjBool]=true';

      const queryString = generateQueryString(query);

      expect(queryString).toBe(expectedQueryString);
    });
  });

  describe('isValidUrl', () => {
    test('returns true as expected on various types of URLs', () => {
      const url = 'https://myWebsite.org?params=12';
      const url2 = 'http://myWebsite.com?params=someString';
      const url3 = 'ws://myWebsite.com';
      const url4 = 'ftp://myftp.com';

      expect(isValidUrl(url)).toBeTruthy();
      expect(isValidUrl(url2)).toBeTruthy();
      expect(isValidUrl(url3)).toBeTruthy();
      expect(isValidUrl(url4)).toBeTruthy();
    });

    test('returns false as expected on various types of non-URLs', () => {
      const string = 'myWebsite.org';
      const string2 = 'webbymcwebface?param=true';
      const string3 = '12345678';
      const string4 = '2d5690456.456456/456';
      const string5 = 'ertert-434333';

      expect(isValidUrl(string)).toBeFalsy();
      expect(isValidUrl(string2)).toBeFalsy();
      expect(isValidUrl(string3)).toBeFalsy();
      expect(isValidUrl(string4)).toBeFalsy();
      expect(isValidUrl(string5)).toBeFalsy();
    });
  });
});
