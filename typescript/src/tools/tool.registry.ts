import {
  type BaseResourceHandler,
  type Configuration,
} from '@commercetools/tools-core';
import {type ToolHandler, type ToolDefinitions} from '../types/tool.types';

/**
 * Resource Registry
 * Automatically discovers and registers all resource handlers
 */
export class ToolRegistry {
  private handlers: Map<string, ToolHandler> = new Map();
  private resources: BaseResourceHandler<Configuration>[] = [];

  /**
   * Register a resource handler
   */
  register(handler: BaseResourceHandler<Configuration>): void {
    this.resources.push(handler);

    // Auto-register all tools for this resource
    const toolNames = handler.getAllToolNames();
    toolNames.forEach((toolName: string) => {
      this.handlers.set(toolName, handler);
    });
  }

  /**
   * Get handler for a tool
   */
  getHandler(toolName: string): ToolHandler | undefined {
    return this.handlers.get(toolName);
  }

  /**
   * Check if handler exists
   */
  hasHandler(toolName: string): boolean {
    return this.handlers.has(toolName);
  }

  /**
   * Get all tool definitions for MCP server
   */
  getAllToolDefinitions(): ToolDefinitions {
    return this.resources.flatMap((resource) =>
      resource.getAllToolDefinitions()
    );
  }

  /**
   * Get all registered resources
   */
  getResources(): BaseResourceHandler[] {
    return [...this.resources];
  }
}
