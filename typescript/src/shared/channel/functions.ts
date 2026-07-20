import {ApiRoot} from '@commercetools/platform-sdk';
import {CommercetoolsFuncContext, Context} from '../../types/configuration';
import * as admin from './admin.functions';
import {ChannelsHandler} from '@commercetools/tools-core';

const handler = new ChannelsHandler();

export const contextToChannelFunctionMapping = (
  context?: Context
): Record<
  string,
  (
    apiRoot: ApiRoot,
    context: CommercetoolsFuncContext,
    params: any
  ) => Promise<any>
> => {
  if (context?.isAdmin) {
    return {
      [handler.getToolDefinition('read').name]: admin.readChannel,
      [handler.getToolDefinition('create').name]: admin.createChannel,
      [handler.getToolDefinition('update').name]: admin.updateChannel,
    };
  }

  return {};
};

// Re-exports for backward compatibility
export const readChannel = admin.readChannel;
export const createChannel = admin.createChannel;
export const updateChannel = admin.updateChannel;
