import {z} from 'zod';
import {DynamicStructuredTool} from '@langchain/core/tools';
import {CallbackManagerForToolRun} from '@langchain/core/callbacks/manager';
import {RunnableConfig} from '@langchain/core/runnables';
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
): DynamicStructuredTool {
  return new DynamicStructuredTool({
    name: method,
    description: description,
    schema: schema,
    func: async (
      arg: z.output<typeof schema>,
      _runManager?: CallbackManagerForToolRun,
      _config?: RunnableConfig
    ): Promise<string> => {
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
