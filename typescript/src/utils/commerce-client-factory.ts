import {GetClientOptions, IApiClientFactory} from '@commercetools/tools-core';
import {Client} from '@commercetools/ts-client';
import {AuthConfig} from '../types/auth';

export class CommerceClientFactory implements IApiClientFactory<AuthConfig> {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  public getClient(
    configuration: AuthConfig,
    authToken: string,
    options?: GetClientOptions
  ): Client {
    return this.client;
  }
}
