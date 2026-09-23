# commercetools Model Context Protocol

This documentation focusses on the development of the MCP server. For the user documentation, view the [main README](../README.md).

## Debugging locally

```bash
#  navigate to ../typescript
pnpm run build
# navigate to ../modelcontextprotocol

# link the local package
pnpm add link:../typescript

# build this package: the executable is dist/cli.js
pnpm run build

# run the server in terminal
node dist/cli.js --tools=read_products --clientId=CLIENT_ID --clientSecret=CLIENT_SECRET --authUrl=AUTH_URL --projectKey=PROJECT_KEY --apiUrl=API_URL

# test using mcptools : Install mcptools from https://github.com/f/mcptools
mcp call read_products --params '{"limit": 2}' node /<absolute-path>/commerce-agent/modelcontextprotocol/dist/cli.js --tools=all \
--projectKey="PROJECT_KEY" \
--clientSecret="CLIENT_SECRET" \
--clientId="CLIENT_ID" \
--authUrl="AUTH_URL" \
--apiUrl="API_URL"
```

`src/index.ts` exports `main()` but does not call it, so running that file
directly starts nothing. `dist/cli.js` is the entry point that does.

**_Do not commit the linked package in package.json to the repo_**

## Testing Using Claude Desktop

NOTE: This package requires Node.js 20 or newer. Make sure the `node` on Claude Desktop's PATH is a v20+ install.

```bash
#  navigate to ../typescript
pnpm run build

# navigate to ../modelcontextprotocol

# link the local package
pnpm add link:../typescript

# build this package: the executable is dist/cli.js
pnpm run build
```

Configure MCP servers in Claude Desktop

```json
{
  "mcpServers": {
    "commercetools": {
      "command": "node",
      "args": [
        "/<absolute-path>/commerce-agent/modelcontextprotocol/dist/cli.js",
        "--tools=all",
        "--projectKey=PROJECT_KEY",
        "--clientSecret=CLIENT_SECRET",
        "--clientId=CLIENT_ID",
        "--authUrl=AUTH_URL",
        "--apiUrl=API_URL"
      ]
    }
  }
}
```

## Debugging the Server

To debug your server, you can use the [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector).

First build the server

```
npm run build
```

Run the following command in your terminal:

```bash
# Start MCP Inspector and server with all tools
npx @modelcontextprotocol/inspector node dist/cli.js --tools=all --clientId=CLIENT_ID --clientSecret=CLIENT_SECRET --projectKey=PROJECT_KEY --authUrl=AUTH_URL --apiUrl=API_URL
```

### Instructions

1. Replace `CLIENT_ID`, `CLIENT_SECRET`, `PROJECT_KEY`, `AUTH_URL`, and `API_URL` with your actual values.
2. Run the command to start the MCP Inspector.
3. Open the MCP Inspector UI in your browser and click Connect to start the MCP server.
4. You can see the list of tools you selected and test each tool individually.
