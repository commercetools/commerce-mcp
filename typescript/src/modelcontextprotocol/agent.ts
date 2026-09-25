import z from 'zod';
import {
  McpServer,
  SUPPORTED_PROTOCOL_VERSIONS,
  fromJsonSchema,
  type JsonSchemaType,
} from '@modelcontextprotocol/server';
import CommercetoolsAPI from '../shared/api';
import {
  isToolAllowed,
  processConfigurationDefaults,
} from '../shared/configuration';
import {contextToTools} from '../shared/tools';
import {
  deriveToolAnnotationsOrConservative,
  deriveToolTitle,
  titleAndAnnotations,
  toolVerb,
} from '@commercetools/tools-core';
import type {Configuration, Context} from '../types/configuration';
import {scopesToActions} from '../utils/scopes';
import {AuthConfig} from '../types/auth';
import {contextToToolsResourceBasedToolSystem} from '../shared/resource-based-tools-system/tools';
import {Tool} from '../types/tools';
import {contextToBulkTools} from '../shared/bulk/tools';
import {DYNAMIC_TOOL_LOADING_THRESHOLD} from '../shared/constants';
import {SERVER_VERSION} from '../shared/version';
import {toolInputJsonSchema} from '../shared/json-schema';

/**
 * Every tool reaches a live commercetools project over the network, so the
 * set of entities it can touch is open: another client, or a background
 * process, can change what a call sees between one request and the next.
 *
 * `@commercetools/tools-core` reports `false` here. We override it, because
 * that reading only holds for a closed, fully-defined domain.
 */
const OPEN_WORLD_HINT = true;
import {
  MODERN_PROTOCOL_VERSION,
  TOOLS_LIST_CACHE_HINT,
} from '../shared/constants';
import {transformToolOutput} from '@commercetools/processors';
import {
  FieldFilteringHandler,
  FieldFilteringManager,
  isFieldFilteringManager,
} from '@commercetools/processors';

class CommercetoolsCommerceAgent extends McpServer {
  private authConfig: AuthConfig;
  private configuration: Configuration = {};
  private commercetoolsAPI: CommercetoolsAPI;

  private constructor({
    authConfig,
    configuration,
  }: {
    authConfig: AuthConfig;
    configuration: Configuration;
  }) {
    super(
      {
        name: 'Commercetools',
        title: 'commercetools',
        version: SERVER_VERSION,
        description:
          'Query and manage a commercetools project through the commercetools APIs.',
        websiteUrl: 'https://commercetools.com',
      },
      {
        // Opt in to the 2026 era — without this the SDK serves 2025 only and
        // never registers `server/discover` — while keeping every 2025-era
        // revision the SDK knows.
        //
        // Listing just the newest legacy revision looks equivalent but is
        // not: the handshake then counter-offers `2025-11-25` to a client
        // that asked for an older one, and a client that does not recognise
        // that version disconnects rather than downgrading. `mcp-remote`
        // does exactly this. Spreading the SDK's own list keeps the range
        // wide and current.
        supportedProtocolVersions: [
          MODERN_PROTOCOL_VERSION,
          ...SUPPORTED_PROTOCOL_VERSIONS,
        ],
        // The tool list only changes when configuration does, so it is worth
        // caching for modern clients. 2025-era responses are unaffected.
        cacheHints: {'tools/list': TOOLS_LIST_CACHE_HINT},
        instructions:
          'Tools are grouped by commercetools resource (carts, orders, products, ...) ' +
          'and by verb: read_* queries, create_* adds, update_* modifies. Read tools ' +
          'accept `where` predicates and `limit`/`offset` paging. Prefer a resource ' +
          'key over its id where a tool accepts both.',
      }
    );

    this.authConfig = authConfig;
    const configurationWithDefaults =
      processConfigurationDefaults(configuration);
    this.configuration = configurationWithDefaults;

    this.commercetoolsAPI = new CommercetoolsAPI(
      this.authConfig,
      configurationWithDefaults.context
    );
  }

  public static async create(option: {
    authConfig: AuthConfig;
    configuration: Configuration;
  }) {
    try {
      const instance = new CommercetoolsCommerceAgent(option);
      await instance.init();

      return instance;
    } catch (err: unknown) {
      throw new Error(
        (err as Error).message ??
          'Unable to initialze `CommercetoolsCommerceAgent`'
      );
    }
  }

  private async init() {
    const configuration = this.configuration;

    if (this.authConfig?.clientId && this.authConfig?.clientSecret) {
      // list of scopes' permissions ['view_cart', 'manage_products', '...']
      const scopes = await this.commercetoolsAPI.introspect();

      // scope based filtering
      const filteredActions = scopesToActions(scopes, configuration);

      this.configuration = {
        ...configuration,
        actions: {
          ...filteredActions,
        },
      };
    }

    this.registerTools();
  }

  private registerTools(): void {
    const {context} = this.configuration;
    const filteredTools = this.getFilteredTools();

    const dynamicToolLoadingThreshold =
      context?.dynamicToolLoadingThreshold || DYNAMIC_TOOL_LOADING_THRESHOLD;

    const shouldRegisterAllTools =
      filteredTools.length <= dynamicToolLoadingThreshold;

    if (shouldRegisterAllTools) {
      this.registerAllTools(filteredTools);
    } else {
      this.registerResourceBasedToolSystem(
        filteredTools,
        dynamicToolLoadingThreshold
      );
    }
  }

  private getFilteredTools() {
    const configuration = this.configuration;
    const customTools = configuration.customTools || [];

    if (!Array.isArray(customTools)) {
      throw new Error(`Tool Error: 'customTools' must be an array of tools`);
    }

    customTools.forEach((tool) => {
      if (!tool.execute || typeof tool.execute != 'function') {
        throw new Error(
          `Tool Error: Please provide an 'execute' function for '${tool.name}' tool.`
        );
      }
    });

    return [
      ...customTools,
      ...contextToTools(configuration.context).filter((tool) =>
        isToolAllowed(tool, configuration)
      ),
    ];
  }

  private registerAllTools(filteredTools: Tool[]): void {
    filteredTools.forEach((tool) => {
      this.registerSingleTool(tool);
    });
  }

  private registerResourceBasedToolSystem(
    filteredTools: Tool[],
    dynamicToolLoadingThreshold: number
  ): void {
    const {context} = this.configuration;
    const filteredToolsLength = filteredTools.length;

    console.error(
      `Filtered tools (${filteredToolsLength}) > ${dynamicToolLoadingThreshold} - Using resource based tool system`
    );

    const filteredToolsResources = this.filteredResources(filteredTools);

    const {listAvailableTools, injectTools, executeTool} =
      contextToToolsResourceBasedToolSystem(filteredToolsResources);

    this.registerSingleTool(listAvailableTools);
    this.registerInjectToolsTool(injectTools, filteredTools);
    this.registerExecuteTool(executeTool);

    // Bulk tool is not a resource based tool, so we need to register it separately
    contextToBulkTools(context).forEach((tool) => {
      this.registerSingleTool(tool);
    });
  }

  private filteredResources(filteredTools: Tool[]): string[] {
    const actionResources = filteredTools
      .map((tool) => Object.keys(tool.actions)[0])
      .filter(Boolean);

    return Array.from(new Set(actionResources));
  }

  /**
   * MCP tool annotations derived from the tool's declared actions.
   *
   * Every tool carries exactly one verb across `create` / `read` / `update`
   * (no tool deletes), so the mapping is direct. `update` is marked
   * destructive because it overwrites existing resource state; `create` is
   * additive and `read` changes nothing.
   *
   * `openWorldHint` is true throughout: these call a remote commercetools
   * project, not a closed local domain.
   */
  /**
   * A tool's parameters as the Standard Schema v2 `registerTool` expects.
   *
   * Our schemas come from `@commercetools/tools-core` on zod 3, which the v2
   * API cannot consume directly, so they go through the JSON Schema bridge
   * (DEVX-883). The cast is safe and confined here: `toolInputJsonSchema`
   * already guarantees an object schema whose `required` keys all exist, and
   * `JsonSchemaObject` differs from the SDK's `JsonSchemaType` only in
   * modelling property values as `unknown` rather than nested schemas.
   */
  private toolSchema<T>(tool: Tool) {
    return fromJsonSchema<T>(toolInputJsonSchema(tool) as JsonSchemaType);
  }

  /**
   * A tool's `title` and MCP `annotations`, derived upstream.
   *
   * `@commercetools/tools-core` owns the tool catalogue, and since 0.4 it also
   * owns this mapping — with a drift test asserting every catalogue tool
   * resolves. Deriving it here too meant two definitions of what `update_*`
   * implies, so this defers to the package.
   *
   * The catalogue does not cover everything we register: the dynamic-loading
   * meta-tools (`list_available_tools`, `execute_tool`) and any custom tool an
   * embedder supplies have no catalogue verb, and `titleAndAnnotations` throws
   * on those. They take the conservative fallback, which claims the tool both
   * writes and destroys — the reading that makes a client ask first.
   */
  private titleAndAnnotationsFor(tool: Tool) {
    const derived =
      toolVerb(tool.method) !== undefined
        ? titleAndAnnotations(tool.method)
        : this.conservativeTitleAndAnnotations(tool);

    return {
      ...derived,
      annotations: {...derived.annotations, openWorldHint: OPEN_WORLD_HINT},
    };
  }

  /**
   * Annotations for a tool the catalogue does not describe: the
   * dynamic-loading meta-tools and any custom tool an embedder supplies.
   * `titleAndAnnotations` throws on an unrecognised verb, so these take the
   * conservative reading — assume the tool writes and destroys, which is what
   * makes a client ask before calling — and log once.
   */
  private conservativeTitleAndAnnotations(tool: Tool) {
    const title = tool.name || deriveToolTitle(tool.method);
    const annotations = deriveToolAnnotationsOrConservative(tool.method, () => {
      console.error(
        `[mcp] no known verb for "${tool.method}"; assuming it writes and destroys`
      );
    });

    return {title, annotations: {...annotations, title}};
  }

  private registerSingleTool(tool: Tool): void {
    const {method, execute} = tool;
    this.registerTool(
      tool.method,
      {
        ...this.titleAndAnnotationsFor(tool),
        description: tool.description,
        inputSchema: this.toolSchema<Record<string, unknown>>(tool),
      },
      async (args: Record<string, unknown>) => {
        let result = await this.commercetoolsAPI.run(method, args, execute);

        if (this.configuration.context?.fieldFiltering) {
          let fieldFilteringHandler!: FieldFilteringManager;
          if (
            isFieldFilteringManager(this.configuration.context?.fieldFiltering)
          ) {
            fieldFilteringHandler = this.configuration.context?.fieldFiltering;
          } else {
            fieldFilteringHandler = new FieldFilteringHandler(
              this.configuration.context?.fieldFiltering
            );
          }
          result = fieldFilteringHandler.filterFields(result);
        }
        return this.createToolResponse(
          this.formatToolResultText(result, `${tool.method} result`),
          {structuredContent: this.toStructuredContent(result)}
        );
      }
    );
  }

  private registerInjectToolsTool(
    injectTools: Tool,
    filteredTools: Tool[]
  ): void {
    type ToolShape = z.infer<typeof injectTools.parameters.shape>;

    this.registerTool(
      injectTools.method,
      {
        ...this.titleAndAnnotationsFor(injectTools),
        description: injectTools.description,
        inputSchema: this.toolSchema<ToolShape>(injectTools),
      },
      async (arg: ToolShape) => {
        const toolsToInject = filteredTools.filter((tool) =>
          arg.toolMethods.includes(tool.method)
        );

        toolsToInject.forEach((tool) => {
          this.registerSingleTool(tool);
        });

        const injectedTools = this.formatInjectedTools(toolsToInject);

        // eslint-disable-next-line no-return-await -- #tool method signature requires
        return await this.createToolResponse(
          `Relevant tools:\n${injectedTools}`
        );
      }
    );
  }

  private registerExecuteTool(executeTool: Tool): void {
    type ToolShape = z.infer<typeof executeTool.parameters.shape>;

    this.registerTool(
      executeTool.method,
      {
        ...this.titleAndAnnotationsFor(executeTool),
        description: executeTool.description,
        inputSchema: this.toolSchema<ToolShape>(executeTool),
      },
      async (args: ToolShape) => {
        try {
          let result = await this.commercetoolsAPI.run(
            args.toolMethod,
            args.arguments || {}
          );

          if (this.configuration.context?.fieldFiltering) {
            let fieldFilteringHandler!: FieldFilteringManager;
            if (
              isFieldFilteringManager(
                this.configuration.context?.fieldFiltering
              )
            ) {
              fieldFilteringHandler =
                this.configuration.context?.fieldFiltering;
            } else {
              fieldFilteringHandler = new FieldFilteringHandler(
                this.configuration.context?.fieldFiltering
              );
            }
            result = fieldFilteringHandler.filterFields(result);
          }

          return this.createToolResponse(
            this.formatToolResultText(result, `${args.toolMethod} result`),
            {structuredContent: this.toStructuredContent(result)}
          );
        } catch (error) {
          return this.handleToolExecutionError(error, args.toolMethod);
        }
      }
    );
  }

  /**
   * The payload as `structuredContent`, when it is shaped like one.
   *
   * The protocol models structured output as a JSON object, so array and
   * scalar payloads are carried by the text block alone rather than being
   * wrapped in an invented envelope.
   */
  private toStructuredContent(
    result: unknown
  ): Record<string, unknown> | undefined {
    if (
      typeof result !== 'object' ||
      result === null ||
      Array.isArray(result)
    ) {
      return undefined;
    }

    return result as Record<string, unknown>;
  }

  /**
   * Default: plain JSON of the payload (no uppercase title wrapper).
   * With {@link Context.toolOutputFormat} `"tabular"`, uses the legacy titled layout.
   */
  private formatToolResultText(data: unknown, tabularTitle: string): string {
    if (this.configuration.context?.toolOutputFormat === 'tabular') {
      return transformToolOutput({
        data,
        title: tabularTitle,
      });
    }

    return transformToolOutput({
      data,
      format: 'json',
    });
  }

  /**
   * A tool result. The text content stays exactly as before so existing
   * clients are unaffected; `structuredContent` is the same payload in
   * machine-readable form, for clients that would otherwise have to parse our
   * stringified JSON back out of a text block.
   */
  private createToolResponse(
    result: string,
    options: {
      structuredContent?: Record<string, unknown>;
      isError?: boolean;
    } = {}
  ): {
    content: Array<{type: 'text'; text: string}>;
    structuredContent?: Record<string, unknown>;
    isError?: boolean;
  } {
    return {
      content: [
        {
          type: 'text',
          text: result,
        },
      ],
      ...(options.structuredContent && {
        structuredContent: options.structuredContent,
      }),
      ...(options.isError && {isError: true}),
    };
  }

  private formatInjectedTools(toolsToInject: Tool[]): string {
    return toolsToInject
      .map((tool) =>
        [
          `name: ${tool.name}`,
          `description: ${tool.description}`,
          `parameters: ${JSON.stringify(tool.parameters.shape, null, 2)}`,
        ].join('\n')
      )
      .join('\n---\n');
  }

  private handleToolExecutionError(error: unknown, toolMethod: string) {
    const errorMessage = error instanceof Error ? error.message : String(error);

    const errorBody =
      error instanceof Error && 'body' in error
        ? JSON.stringify(error.body, null, 2)
        : String(error);

    console.error('Error executing tool', {
      toolMethod,
      errorMessage,
      errorBody,
    });

    return this.createToolResponse(
      `Error executing tool '${toolMethod}': ${errorMessage} - ${errorBody}`,
      // Without this a failed `execute_tool` call is indistinguishable from a
      // successful one. Tools that throw are already flagged by the SDK.
      {isError: true}
    );
  }
}

export default CommercetoolsCommerceAgent;
