import {
  type BaseResourceHandler,
  type ToolExecutionContext,
  type Configuration,
} from '@commercetools/tools-core';

/**
 * Tool handler interface
 */
export interface ToolHandler {
  execute(context: ToolExecutionContext<Configuration>): Promise<unknown>;
}

/**
 * Tool definition type extracted from BaseResourceHandler
 * Represents a single tool definition with name, description, and input schema
 */
export type ToolDefinition = ReturnType<
  BaseResourceHandler<Configuration>['getAllToolDefinitions']
>[number];

/**
 * Array of tool definitions
 */
export type ToolDefinitions = ToolDefinition[];
