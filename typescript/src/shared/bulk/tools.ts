import {Context} from '../../types/configuration';
import {buildBulkTools} from '../core-bridge';

/**
 * Bulk tools are registered separately by the MCP adapter (they are not part of
 * the resource-based tool system). Backed by the core BulkHandler.
 */
export const contextToBulkTools = (context?: Context) =>
  buildBulkTools(context);
