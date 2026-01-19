import {createTool} from '@mastra/core/tools';
import {z} from 'zod';
import CommercetoolsAPI from '../shared/api';
import {transformToolOutput} from '../modelcontextprotocol/transform';
import {
  FieldFilteringHandler,
  FieldFilteringManager,
  FieldFilteringManagerConfig,
  isFieldFilteringManager,
} from '../modelcontextprotocol/field-filtering';

export default function CommercetoolsTool(
  commercetoolsAPI: CommercetoolsAPI,
  method: string,
  description: string,
  schema: z.ZodObject<any, any, any, any, {[x: string]: any}>,
  toolOutputFormat?: 'json' | 'tabular',
  fieldFiltering?: FieldFilteringManagerConfig | FieldFilteringManager
) {
  return createTool({
    id: method,
    description,
    inputSchema: schema,
    outputSchema: z.object({result: z.string()}),
    execute: async ({context}) => {
      let result = await commercetoolsAPI.run(method, context);
      if (fieldFiltering) {
        let fieldFilteringHandler!: FieldFilteringManager;
        if (isFieldFilteringManager(fieldFiltering)) {
          fieldFilteringHandler = fieldFiltering;
        } else {
          fieldFilteringHandler = new FieldFilteringHandler(fieldFiltering);
        }
        result = fieldFilteringHandler.filterFields(result);
      }
      return {
        result: transformToolOutput({
          title: `${method} result`,
          data: result,
          format: toolOutputFormat,
        }),
      };
    },
  });
}
