import type {Tool} from 'ai';
import {tool} from 'ai';
import {z} from 'zod';
import CommercetoolsAPI from '../shared/api';
import {transformToolOutput} from '@commercetools/processors';
import {
  FieldFilteringHandler,
  FieldFilteringManager,
  FieldFilteringManagerConfig,
  isFieldFilteringManager,
} from '@commercetools/processors';

export default function CommercetoolsTool(
  commercetoolsAPI: CommercetoolsAPI,
  method: string,
  description: string,
  schema: z.ZodObject<any, any, any, any, {[x: string]: any}>,
  toolOutputFormat?: 'json' | 'tabular',
  fieldFiltering?: FieldFilteringManagerConfig | FieldFilteringManager
): Tool {
  return tool({
    description: description,
    parameters: schema,
    execute: async (arg: z.output<typeof schema>) => {
      let result = await commercetoolsAPI.run(method, arg);
      if (fieldFiltering) {
        let fieldFilteringHandler!: FieldFilteringManager;
        if (isFieldFilteringManager(fieldFiltering)) {
          fieldFilteringHandler = fieldFiltering;
        } else {
          fieldFilteringHandler = new FieldFilteringHandler(fieldFiltering);
        }
        result = fieldFilteringHandler.filterFields(result);
      }
      return transformToolOutput({
        title: `${method} result`,
        data: result,
        format: toolOutputFormat,
      });
    },
  });
}
