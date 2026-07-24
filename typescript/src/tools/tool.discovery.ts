import {ToolRegistry} from './tool.registry';
import {
  BaseResourceHandler,
  getDecoratorRegisteredHandlers,
  type Configuration,
} from '@commercetools/tools-core';
import {type ToolDefinitions} from '../types/tool.types';

// Import all resource handlers to trigger decorator registration
// The decorator automatically registers handlers when classes are defined
import './resource';

/**
 * Tool Discovery Service - Decorator Pattern Only
 * Automatically discovers and registers all resource handlers using @ToolHandler() decorator
 *
 * To add a new handler, simply:
 * 1. Create a class extending BaseResourceHandler
 * 2. Add @ToolHandler() decorator
 * 3. Export it from ./resource/index.ts (decorator runs on class definition)
 */
export class ToolDiscovery {
  private toolRegistry: ToolRegistry;

  constructor(toolRegistry: ToolRegistry) {
    this.toolRegistry = toolRegistry;
    this.discoverAndRegister();
  }

  /**
   * Discover and register all resource handlers via decorator
   * Handlers are already registered by decorators when modules are imported
   */
  private discoverAndRegister(): void {
    // Get all handlers registered via decorator
    // These were registered when the handler classes were defined (decorator execution)
    const handlers = getDecoratorRegisteredHandlers();

    // Register them in the registry
    handlers.forEach((handler: BaseResourceHandler<Configuration>) => {
      this.toolRegistry.register(handler);
    });
  }

  /**
   * Get the registry
   */
  getRegistry(): ToolRegistry {
    return this.toolRegistry;
  }

  /**
   * Get all tool definitions
   */
  getAllToolDefinitions(): ToolDefinitions {
    return this.toolRegistry.getAllToolDefinitions();
  }
}
