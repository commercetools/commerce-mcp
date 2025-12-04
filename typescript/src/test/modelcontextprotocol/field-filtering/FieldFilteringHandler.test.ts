import {FieldFilteringHandler} from '../../../modelcontextprotocol/field-filtering/FieldFilteringHandler';
import {
  defaultJsonRedactionText,
  defaultUrlRedactionText,
} from '../../../modelcontextprotocol/field-filtering/defaultFilteringRules';
import {FieldFilteringManagerConfig} from '../../../modelcontextprotocol/field-filtering/FieldFilteringManagerConfig';

describe(FieldFilteringHandler.name, () => {
  afterAll(() => {
    jest.resetAllMocks();
  });

  describe('filter', () => {
    describe(':type=filter', () => {
      // TODO
    });

    describe(':type=redact', () => {
      test('redacts all paths specified and no other properties without case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          paths: [
            {value: 'pathToRedact', caseSensitive: false, type: 'redact'},
            {
              value: 'myObject.myPathToRedact',
              caseSensitive: false,
              type: 'redact',
            },
            {
              value: 'myObject.nestedObject.nestedPathToRedact',
              caseSensitive: false,
              type: 'redact',
            },
          ],
        };

        const data = {
          pathToRedact: 'my password',
          otherProperty: 'some string',
          myObject: {
            myPathToRedact: 'my credit card number',
            otherProperty: 'my other property',
            nestedObject: {
              nestedPathToRedact: 'my home address',
              myOtherNestedProperty: 'my other nested property',
            },
          },
          myobject: {
            mypathToRedact: 'case sensitivity check',
          },
        };

        const returnedData = new FieldFilteringHandler(
          customOverrideRules
        ).filter(data);

        expect(returnedData.pathToRedact).toBe(defaultJsonRedactionText);
        expect(returnedData.myObject.myPathToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myObject.nestedObject.nestedPathToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myobject.mypathToRedact).toBe(
          defaultJsonRedactionText
        );

        expect(returnedData.otherProperty).toBe(data.otherProperty);
        expect(returnedData.myObject.otherProperty).toBe(
          data.myObject.otherProperty
        );
        expect(returnedData.myObject.nestedObject.myOtherNestedProperty).toBe(
          data.myObject.nestedObject.myOtherNestedProperty
        );
      });

      test('redacts all paths specified and no other properties with case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          paths: [
            {value: 'pathToRedact', caseSensitive: true, type: 'redact'},
            {
              value: 'myObject.myPathToRedact',
              caseSensitive: true,
              type: 'redact',
            },
            {
              value: 'myObject.nestedObject.nestedPathToRedact',
              caseSensitive: true,
              type: 'redact',
            },
          ],
        };

        const data = {
          pathToRedact: 'my password',
          otherProperty: 'some string',
          myObject: {
            myPathToRedact: 'my credit card number',
            otherProperty: 'my other property',
            nestedObject: {
              nestedPathToRedact: 'my home address',
              myOtherNestedProperty: 'my other nested property',
            },
          },
          myobject: {
            mypathToRedact: 'case sensitivity check',
          },
        };

        const returnedData = new FieldFilteringHandler(
          customOverrideRules
        ).filter(data);

        expect(returnedData.pathToRedact).toBe(defaultJsonRedactionText);
        expect(returnedData.myObject.myPathToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myObject.nestedObject.nestedPathToRedact).toBe(
          defaultJsonRedactionText
        );

        expect(returnedData.otherProperty).toBe(data.otherProperty);
        expect(returnedData.myObject.otherProperty).toBe(
          data.myObject.otherProperty
        );
        expect(returnedData.myObject.nestedObject.myOtherNestedProperty).toBe(
          data.myObject.nestedObject.myOtherNestedProperty
        );
        expect(returnedData.myobject.mypathToRedact).toBe(
          data.myobject.mypathToRedact
        );
      });

      test('redacts all properties specified and no other properties without case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          properties: [
            {value: 'myPropertyToRedact', caseSensitive: false, type: 'redact'},
            {
              value: 'nestedPropertyToRedact',
              caseSensitive: false,
              type: 'redact',
            },
          ],
        };

        const data = {
          myPropertyToRedact: 'my password',
          otherProperty: 'some string',
          myObject: {
            myPropertyToRedact: 'my credit card number',
            otherProperty: 'my other property',
            nestedObject: {
              nestedPropertyToRedact: 'my home address',
              myOtherNestedProperty: 'my other nested property',
            },
          },
          myobject: {
            mypropertytoRedact: 'case sensitivity check',
          },
        };

        const returnedData = new FieldFilteringHandler(
          customOverrideRules
        ).filter(data);

        expect(returnedData.myPropertyToRedact).toBe(defaultJsonRedactionText);
        expect(returnedData.myObject.myPropertyToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myObject.nestedObject.nestedPropertyToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myobject.mypropertytoRedact).toBe(
          defaultJsonRedactionText
        );

        expect(returnedData.otherProperty).toBe(data.otherProperty);
        expect(returnedData.myObject.otherProperty).toBe(
          data.myObject.otherProperty
        );
        expect(returnedData.myObject.nestedObject.myOtherNestedProperty).toBe(
          data.myObject.nestedObject.myOtherNestedProperty
        );
      });

      test('redacts all properties specified and no other properties with case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          properties: [
            {value: 'myPropertyToRedact', caseSensitive: true, type: 'redact'},
            {
              value: 'nestedPropertyToRedact',
              caseSensitive: true,
              type: 'redact',
            },
          ],
        };

        const data = {
          myPropertyToRedact: 'my password',
          otherProperty: 'some string',
          myObject: {
            myPropertyToRedact: 'my credit card number',
            otherProperty: 'my other property',
            nestedObject: {
              nestedPropertyToRedact: 'my home address',
              myOtherNestedProperty: 'my other nested property',
            },
          },
          myobject: {
            mypropertytoRedact: 'case sensitivity check',
          },
        };

        const returnedData = new FieldFilteringHandler(
          customOverrideRules
        ).filter(data);

        expect(returnedData.myPropertyToRedact).toBe(defaultJsonRedactionText);
        expect(returnedData.myObject.myPropertyToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myObject.nestedObject.nestedPropertyToRedact).toBe(
          defaultJsonRedactionText
        );

        expect(returnedData.otherProperty).toBe(data.otherProperty);
        expect(returnedData.myObject.otherProperty).toBe(
          data.myObject.otherProperty
        );
        expect(returnedData.myObject.nestedObject.myOtherNestedProperty).toBe(
          data.myObject.nestedObject.myOtherNestedProperty
        );
        expect(returnedData.myobject.mypropertytoRedact).toBe(
          data.myobject.mypropertytoRedact
        );
      });

      test('redacts all properties specified by other config parameters except paths specified by whitelistPaths without case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          paths: [
            {
              value: 'myObject.nestedObject.nestedPathToRedact',
              caseSensitive: false,
              type: 'redact',
            },
          ],
          properties: [
            {
              value: 'myPropertyToNotRedact',
              caseSensitive: false,
              type: 'redact',
            },
          ],
          whitelistPaths: [
            {
              value: 'myObject.myPropertyToNotRedact',
              caseSensitive: false,
              type: 'redact',
            },
          ],
          includes: [{value: 'Redact', type: 'redact', caseSensitive: false}],
        };

        const data = {
          myPropertyToRedact: 'my password',
          otherProperty: 'some string',
          myObject: {
            myPropertyToNotRedact: 'my credit card number',
            otherProperty: 'my other property',
            nestedObject: {
              nestedPropertyToRedact: 'my home address',
              myOtherNestedProperty: 'my other nested property',
            },
          },
          myobject: {
            myPropertyToNotredact: 'case insensitivity check',
          },
        };

        const returnedData = new FieldFilteringHandler(
          customOverrideRules
        ).filter(data);

        expect(returnedData.myPropertyToRedact).toBe(defaultJsonRedactionText);
        expect(returnedData.otherProperty).toBe(data.otherProperty);

        expect(returnedData.myObject.myPropertyToNotRedact).toBe(
          data.myObject.myPropertyToNotRedact
        );
        expect(returnedData.myObject.otherProperty).toBe(
          data.myObject.otherProperty
        );

        expect(returnedData.myObject.nestedObject.nestedPropertyToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myObject.nestedObject.myOtherNestedProperty).toBe(
          data.myObject.nestedObject.myOtherNestedProperty
        );

        expect(returnedData.myobject.myPropertyToNotredact).toBe(
          data.myobject.myPropertyToNotredact
        );
      });

      test('redacts all properties specified by other config parameters except paths specified by whitelistPaths with case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          paths: [
            {
              value: 'myObject.nestedObject.nestedPathToRedact',
              caseSensitive: true,
              type: 'redact',
            },
          ],
          properties: [
            {
              value: 'myPropertyToNotRedact',
              caseSensitive: true,
              type: 'redact',
            },
          ],
          whitelistPaths: [
            {
              value: 'myObject.myPropertyToNotRedact',
              caseSensitive: true,
              type: 'redact',
            },
          ],
          includes: [{value: 'Redact', caseSensitive: true, type: 'redact'}],
        };

        const data = {
          myPropertyToRedact: 'my password',
          otherProperty: 'some string',
          myObject: {
            myPropertyToNotRedact: 'my credit card number',
            otherProperty: 'my other property',
            nestedObject: {
              nestedPropertyToRedact: 'my home address',
              myOtherNestedProperty: 'my other nested property',
            },
          },
          myobject: {
            myPropertyToNotredact: 'case sensitivity check',
          },
        };

        const returnedData = new FieldFilteringHandler(
          customOverrideRules
        ).filter(data);

        expect(returnedData.myPropertyToRedact).toBe(defaultJsonRedactionText);
        expect(returnedData.otherProperty).toBe(data.otherProperty);

        expect(returnedData.myObject.myPropertyToNotRedact).toBe(
          data.myObject.myPropertyToNotRedact
        );
        expect(returnedData.myObject.otherProperty).toBe(
          data.myObject.otherProperty
        );

        expect(returnedData.myObject.nestedObject.nestedPropertyToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myObject.nestedObject.myOtherNestedProperty).toBe(
          data.myObject.nestedObject.myOtherNestedProperty
        );

        expect(returnedData.myobject.myPropertyToNotredact).toBe(
          data.myobject.myPropertyToNotredact
        );
      });

      test('redacts all includes specified for all matching properties and no others, with case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          includes: [
            {value: 'Redact', caseSensitive: true, type: 'redact'},
            {value: 'AlsoRed', caseSensitive: true, type: 'redact'},
          ],
        };

        const data = {
          myPropertyToRedact: 'my password',
          otherProperty: 'some string',
          myObject: {
            myPropertyToRedact: 'my credit card number',
            myPropertyToAlsoRed: 'my email address',
            otherProperty: 'my other property',
            nestedObject: {
              nestedPropertyToRedact: 'my home address',
              myOtherNestedProperty: 'my other nested property',
            },
          },
          myobject: {
            myPropertytoredact: 'case sensitivity check',
          },
        };

        const returnedData = new FieldFilteringHandler(
          customOverrideRules
        ).filter(data);

        expect(returnedData.myPropertyToRedact).toBe(defaultJsonRedactionText);
        expect(returnedData.otherProperty).toBe(data.otherProperty);

        expect(returnedData.myObject.myPropertyToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myObject.myPropertyToAlsoRed).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myObject.otherProperty).toBe(
          data.myObject.otherProperty
        );

        expect(returnedData.myObject.nestedObject.nestedPropertyToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myObject.nestedObject.myOtherNestedProperty).toBe(
          data.myObject.nestedObject.myOtherNestedProperty
        );

        expect(returnedData.myobject.myPropertytoredact).toBe(
          data.myobject.myPropertytoredact
        );
      });

      test('redacts all includes specified for all matching properties and no others, without case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          includes: [
            {value: 'Redact', caseSensitive: false, type: 'redact'},
            {value: 'alsored', caseSensitive: false, type: 'redact'},
          ],
        };

        const data = {
          myPropertyToRedact: 'my password',
          otherProperty: 'some string',
          myObject: {
            myPropertyToRedact: 'my credit card number',
            myPropertyToAlsoRed: 'my email address',
            otherProperty: 'my other property',
            nestedObject: {
              nestedPropertyToRedact: 'my home address',
              myOtherNestedProperty: 'my other nested property',
            },
          },
          myobject: {
            myPropertytoredact: 'case insensitivity check',
          },
        };

        const returnedData = new FieldFilteringHandler(
          customOverrideRules
        ).filter(data);

        expect(returnedData.myPropertyToRedact).toBe(defaultJsonRedactionText);
        expect(returnedData.myObject.myPropertyToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myObject.nestedObject.nestedPropertyToRedact).toBe(
          defaultJsonRedactionText
        );
        expect(returnedData.myobject.myPropertytoredact).toBe(
          defaultJsonRedactionText
        );

        expect(returnedData.otherProperty).toBe(data.otherProperty);
        expect(returnedData.myObject.otherProperty).toBe(
          data.myObject.otherProperty
        );
        expect(returnedData.myObject.nestedObject.myOtherNestedProperty).toBe(
          data.myObject.nestedObject.myOtherNestedProperty
        );
      });

      test(`replaces the default redaction text of "${defaultJsonRedactionText}" with custom jsonRedactionText passed in ctor`, () => {
        const customJsonRedactionText = 'Custom JSON Redaction Text';
        const customOverrideRules: FieldFilteringManagerConfig = {
          includes: [{value: 'Redact', caseSensitive: false, type: 'redact'}],
          jsonRedactionText: customJsonRedactionText,
        };

        const data = {
          propertyToRedact: 'my password',
          myObject: {
            nestedObject: {
              nestedPropertyToRedact: 'my home address',
            },
          },
        };

        const returnedData = new FieldFilteringHandler(
          customOverrideRules
        ).filter(data);

        expect(returnedData.propertyToRedact).toBe(customJsonRedactionText);
        expect(returnedData.myObject.nestedObject.nestedPropertyToRedact).toBe(
          customJsonRedactionText
        );
      });

      test('redacts queries in all url formatted JSON properties by rules passed', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          includes: [{value: 'Redact', caseSensitive: false, type: 'redact'}],
        };

        const httpUrl =
          'http://mywebsite/page/?toRedact=toredact&' +
          'prop=myProperty&nestedObject%5BdeeperNestedObject%5D%5BpasswordToRedact%5D=5BpasswordToRedact';
        const redactedHttpUrl =
          `http://mywebsite/page/?toRedact=${defaultUrlRedactionText}&` +
          `prop=myProperty&nestedObject%5BdeeperNestedObject%5D%5BpasswordToRedact%5D=${defaultUrlRedactionText}`;

        const httpsUrl =
          'https://someothersite?nestedObject%5BnestedArray%5D%5B1%5D%5BredactArrayPassword%5D=sometext';
        const redactedHttpsUrl = `https://someothersite/?nestedObject%5BnestedArray%5D%5B1%5D%5BredactArrayPassword%5D=${defaultUrlRedactionText}`;

        const websocketUrl =
          'ws://somewebsocketurl/?somePropToRedact=2dfg3yuk4d&' +
          'nestedObject%5BdeeperNestedObject%5D%5BtoRedact%5D=lorem+ipsum';
        const redactedWebsocketUrl =
          `ws://somewebsocketurl/?somePropToRedact=${defaultUrlRedactionText}&` +
          `nestedObject%5BdeeperNestedObject%5D%5BtoRedact%5D=${defaultUrlRedactionText}`;

        const ftpUrl =
          'ftp://somewebsocketurl/?somePropToRedact=2dfg3yuk4d&' +
          'nestedObject%5BdeeperNestedObject%5D%5BtoRedact%5D=lorem+ipsum';
        const redactedFtpUrl =
          `ftp://somewebsocketurl/?somePropToRedact=${defaultUrlRedactionText}&` +
          `nestedObject%5BdeeperNestedObject%5D%5BtoRedact%5D=${defaultUrlRedactionText}`;

        const data = {
          httpUrl,
          myObject: {
            httpsUrl,
            nestedObject: {
              websocketUrl,
              ftpUrl,
            },
          },
        };

        const returnedData = new FieldFilteringHandler(
          customOverrideRules
        ).filter(data);

        expect(returnedData.httpUrl).toBe(redactedHttpUrl);
        expect(returnedData.myObject.httpsUrl).toBe(redactedHttpsUrl);
        expect(returnedData.myObject.nestedObject.websocketUrl).toBe(
          redactedWebsocketUrl
        );
        expect(returnedData.myObject.nestedObject.ftpUrl).toBe(redactedFtpUrl);
      });
    });
  });

  describe('filterUrl', () => {
    describe(':type=filter', () => {
      // TODO
    });
    describe(':type=redact', () => {
      test('redacts paths specified and no other properties without case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          paths: [
            {value: 'pathToRedact', caseSensitive: false, type: 'redact'},
            {
              value: 'myObject.nestedObject.nestedPathToRedact',
              caseSensitive: false,
              type: 'redact',
            },
          ],
        };

        const query = {
          pathToRedact: 'myPassword',
          pathToredact: 'caseSensitivityCheck',
          myObject: {
            myPathToRedact: 'myCreditCardNumber',
            nestedObject: {
              nestedPathToRedact: 'myHomeAddress',
              pathToRedact: 'myOtherNestedProperty',
            },
          },
          myobject: {
            nestedobject: {
              nestedPathToRedact: 'caseSensitivityCheck',
            },
          },
        };

        const inputUrl =
          `https://localhost/page?pathToRedact=${query.pathToRedact}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${query.myObject.nestedObject.nestedPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5Bnestedobject%5D%5BnestedPathToRedact%5D=${query.myobject.nestedobject.nestedPathToRedact}`;

        const redactedUrl = new FieldFilteringHandler(
          customOverrideRules
        ).filterUrl(inputUrl);

        const expectedOutputUrl =
          `https://localhost/page?pathToRedact=${defaultUrlRedactionText}&` +
          `pathToredact=${defaultUrlRedactionText}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${defaultUrlRedactionText}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5Bnestedobject%5D%5BnestedPathToRedact%5D=${defaultUrlRedactionText}`;

        expect(redactedUrl).toBe(expectedOutputUrl);
      });

      test('redacts paths specified and no other properties with case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          paths: [
            {value: 'pathToRedact', caseSensitive: true, type: 'redact'},
            {
              value: 'myObject.nestedObject.nestedPathToRedact',
              caseSensitive: true,
              type: 'redact',
            },
          ],
        };

        const query = {
          pathToRedact: 'myPassword',
          pathToredact: 'caseSensitivityCheck',
          myObject: {
            myPathToRedact: 'myCreditCardNumber',
            nestedObject: {
              nestedPathToRedact: 'myHomeAddress',
              pathToRedact: 'myOtherNestedProperty',
            },
          },
          myobject: {
            nestedobject: {
              nestedPathToRedact: 'caseSensitivityCheck',
            },
          },
        };

        const inputUrl =
          `https://localhost/page?pathToRedact=${query.pathToRedact}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${query.myObject.nestedObject.nestedPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToRedact%5D=${query.myobject.nestedobject.nestedPathToRedact}`;

        const redactedUrl = new FieldFilteringHandler(
          customOverrideRules
        ).filterUrl(inputUrl);

        const expectedOutputUrl =
          `https://localhost/page?pathToRedact=${defaultUrlRedactionText}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${defaultUrlRedactionText}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToRedact%5D=${query.myobject.nestedobject.nestedPathToRedact}`;

        expect(redactedUrl).toBe(expectedOutputUrl);
      });

      test('redacts all properties specified and no other properties without case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          properties: [
            {value: 'pathToRedact', caseSensitive: false, type: 'redact'},
            {value: 'nestedPathToRedact', caseSensitive: false, type: 'redact'},
          ],
        };

        const query = {
          pathToRedact: 'myPassword',
          pathToredact: 'caseSensitivityCheck',
          myObject: {
            myPathToRedact: 'myCreditCardNumber',
            nestedObject: {
              nestedPathToRedact: 'myHomeAddress',
              pathToRedact: 'myOtherNestedProperty',
            },
          },
          myobject: {
            nestedobject: {
              nestedPathToredact: 'caseSensitivityCheck',
            },
          },
        };

        const inputUrl =
          `https://localhost/page?pathToRedact=${query.pathToRedact}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${query.myObject.nestedObject.nestedPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${query.myobject.nestedobject.nestedPathToredact}`;

        const redactedUrl = new FieldFilteringHandler(
          customOverrideRules
        ).filterUrl(inputUrl);

        const expectedOutputUrl =
          `https://localhost/page?pathToRedact=${defaultUrlRedactionText}&` +
          `pathToredact=${defaultUrlRedactionText}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${defaultUrlRedactionText}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${defaultUrlRedactionText}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${defaultUrlRedactionText}`;

        expect(redactedUrl).toBe(expectedOutputUrl);
      });

      test('redacts all properties specified and no other properties with case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          properties: [
            {value: 'pathToRedact', caseSensitive: true, type: 'redact'},
            {value: 'nestedPathToRedact', caseSensitive: true, type: 'redact'},
          ],
        };

        const query = {
          pathToRedact: 'myPassword',
          pathToredact: 'caseSensitivityCheck',
          myObject: {
            myPathToRedact: 'myCreditCardNumber',
            nestedObject: {
              nestedPathToRedact: 'myHomeAddress',
              pathToRedact: 'myOtherNestedProperty',
            },
          },
          myobject: {
            nestedobject: {
              nestedPathToredact: 'caseSensitivityCheck',
            },
          },
        };

        const inputUrl =
          `https://localhost/page?pathToRedact=${query.pathToRedact}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${query.myObject.nestedObject.nestedPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${query.myobject.nestedobject.nestedPathToredact}`;

        const redactedUrl = new FieldFilteringHandler(
          customOverrideRules
        ).filterUrl(inputUrl);

        const expectedOutputUrl =
          `https://localhost/page?pathToRedact=${defaultUrlRedactionText}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${defaultUrlRedactionText}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${defaultUrlRedactionText}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${query.myobject.nestedobject.nestedPathToredact}`;

        expect(redactedUrl).toBe(expectedOutputUrl);
      });

      test('redacts all properties specified by other config parameters except paths specified by whitelistPaths without case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          includes: [{value: 'redact', caseSensitive: false, type: 'redact'}],
          whitelistPaths: [
            {value: 'pathToRedact', caseSensitive: false, type: 'redact'},
            {
              value: 'myObject.nestedObject.pathToRedact',
              caseSensitive: false,
              type: 'redact',
            },
          ],
        };

        const query = {
          pathToRedact: 'myPassword',
          pathToredact: 'caseSensitivityCheck',
          myObject: {
            myPathToRedact: 'myCreditCardNumber',
            nestedObject: {
              pathToRedact: 'myOtherNestedProperty',
            },
          },
          myobject: {
            nestedobject: {
              nestedPathToredact: 'caseSensitivityCheck',
            },
          },
        };

        const inputUrl =
          `https://localhost/page?pathToRedact=${query.pathToRedact}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${query.myobject.nestedobject.nestedPathToredact}`;

        const redactedUrl = new FieldFilteringHandler(
          customOverrideRules
        ).filterUrl(inputUrl);

        const expectedOutputUrl =
          `https://localhost/page?pathToRedact=${query.pathToRedact}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathToRedact%5D=${defaultUrlRedactionText}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${defaultUrlRedactionText}`;

        expect(redactedUrl).toBe(expectedOutputUrl);
      });

      test('redacts all properties specified by other config parameters except paths specified by whitelistPaths with case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          includes: [{value: 'redact', caseSensitive: false, type: 'redact'}],
          whitelistPaths: [
            {value: 'pathToRedact', caseSensitive: true, type: 'redact'},
            {
              value: 'myObject.nestedObject.pathToRedact',
              caseSensitive: true,
              type: 'redact',
            },
          ],
        };

        const query = {
          pathToRedact: 'myPassword',
          pathToredact: 'caseSensitivityCheck',
          myObject: {
            myPathToRedact: 'myCreditCardNumber',
            nestedObject: {
              pathToRedact: 'myOtherNestedProperty',
            },
          },
          myobject: {
            nestedobject: {
              nestedPathToredact: 'caseSensitivityCheck',
            },
          },
        };

        const inputUrl =
          `https://localhost/page?pathToRedact=${query.pathToRedact}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${query.myobject.nestedobject.nestedPathToredact}`;

        const redactedUrl = new FieldFilteringHandler(
          customOverrideRules
        ).filterUrl(inputUrl);

        const expectedOutputUrl =
          `https://localhost/page?pathToRedact=${query.pathToRedact}&` +
          `pathToredact=${defaultUrlRedactionText}&` +
          `myObject%5BmyPathToRedact%5D=${defaultUrlRedactionText}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${defaultUrlRedactionText}`;

        expect(redactedUrl).toBe(expectedOutputUrl);
      });

      test('redacts all includes specified and no other properties without case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          includes: [
            {value: 'pathToRedact', caseSensitive: false, type: 'redact'},
            {value: 'NESTED', caseSensitive: false, type: 'redact'},
          ],
        };

        const query = {
          pathToRedact: 'myPassword',
          pathToredact: 'caseSensitivityCheck',
          myObject: {
            myPathNotToRedact: 'myCreditCardNumber',
            nestedObject: {
              nestedPathToRedact: 'myHomeAddress',
              pathToRedact: 'myOtherNestedProperty',
            },
          },
          myobject: {
            nestedobject: {
              nestedPathToredact: 'caseSensitivityCheck',
            },
          },
        };

        const inputUrl =
          `https://localhost/page?pathToRedact=${query.pathToRedact}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathNotToRedact%5D=${query.myObject.myPathNotToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${query.myObject.nestedObject.nestedPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${query.myobject.nestedobject.nestedPathToredact}`;

        const redactedUrl = new FieldFilteringHandler(
          customOverrideRules
        ).filterUrl(inputUrl);

        const expectedOutputUrl =
          `https://localhost/page?pathToRedact=${defaultUrlRedactionText}&` +
          `pathToredact=${defaultUrlRedactionText}&` +
          `myObject%5BmyPathNotToRedact%5D=${query.myObject.myPathNotToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${defaultUrlRedactionText}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${defaultUrlRedactionText}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${defaultUrlRedactionText}`;

        expect(redactedUrl).toBe(expectedOutputUrl);
      });

      test('redacts all includes specified and no other properties with case sensitivity', () => {
        const customOverrideRules: FieldFilteringManagerConfig = {
          includes: [
            {value: 'pathToRedact', caseSensitive: true, type: 'redact'},
            {value: 'NESTED', caseSensitive: true, type: 'redact'},
          ],
        };

        const query = {
          pathToRedact: 'myPassword',
          pathToredact: 'caseSensitivityCheck',
          myObject: {
            myPathToRedact: 'myCreditCardNumber',
            nestedObject: {
              nestedPathToRedact: 'myHomeAddress',
              pathToRedact: 'myOtherNestedProperty',
            },
          },
          myobject: {
            nestedobject: {
              nestedPathToredact: 'caseSensitivityCheck',
            },
          },
        };

        const inputUrl =
          `https://localhost/page?pathToRedact=${query.pathToRedact}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${query.myObject.nestedObject.nestedPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${query.myobject.nestedobject.nestedPathToredact}`;

        const redactedUrl = new FieldFilteringHandler(
          customOverrideRules
        ).filterUrl(inputUrl);

        const expectedOutputUrl =
          `https://localhost/page?pathToRedact=${defaultUrlRedactionText}&` +
          `pathToredact=${query.pathToredact}&` +
          `myObject%5BmyPathToRedact%5D=${query.myObject.myPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BnestedPathToRedact%5D=${query.myObject.nestedObject.nestedPathToRedact}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${defaultUrlRedactionText}&` +
          `myobject%5D%5Bnestedobject%5D%5BnestedPathToredact%5D=${query.myobject.nestedobject.nestedPathToredact}`;

        expect(redactedUrl).toBe(expectedOutputUrl);
      });

      test(`replaces the default redaction text of "${defaultUrlRedactionText}" with custom urlRedactionText passed in ctor`, () => {
        const customUrlRedactionText = 'customUrlRedactionText';
        const customOverrideRules: FieldFilteringManagerConfig = {
          includes: [{value: 'redact', caseSensitive: false, type: 'redact'}],
          urlRedactionText: customUrlRedactionText,
        };

        const query = {
          pathToRedact: 'myPassword',
          myObject: {
            nestedObject: {
              pathToRedact: 'myOtherNestedProperty',
            },
          },
        };

        const inputUrl =
          `https://localhost/page?pathToRedact=${query.pathToRedact}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${query.myObject.nestedObject.pathToRedact}`;

        const redactedUrl = new FieldFilteringHandler(
          customOverrideRules
        ).filterUrl(inputUrl);

        const expectedOutputUrl =
          `https://localhost/page?pathToRedact=${customUrlRedactionText}&` +
          `myObject%5BnestedObject%5D%5BpathToRedact%5D=${customUrlRedactionText}`;

        expect(redactedUrl).toBe(expectedOutputUrl);
      });
    });
  });
});
