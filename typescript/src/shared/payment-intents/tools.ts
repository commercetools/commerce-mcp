import {Tool} from '../../types/tools';
import {z} from 'zod';
import {Context} from '../../types/configuration';
import {PaymentIntentsHandler} from '@commercetools/tools-core';

const handler = new PaymentIntentsHandler();

const tools: Record<string, Tool> = {
  update_payment_intent: {
    name: 'Update Payment Intent',
    method: handler.getToolDefinition('update').name,
    parameters: handler.getToolDefinition('update')
      .inputSchema as unknown as z.ZodObject<any, any, any, any>,
    description: handler.getToolDefinition('update').description,
    actions: {
      'payment-intents': {
        update: true,
      },
    },
  },
};

export const contextToPaymentIntentTools = (_context?: Context) => {
  return [tools.update_payment_intent];
};
