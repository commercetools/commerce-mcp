# Commercetools MCP Server — Python

Python implementation of the Commercetools MCP server, built with [FastMCP](https://github.com/jlowin/fastmcp). Exposes Commercetools operations as MCP tools for use with Claude Desktop, Claude Code, and any MCP-compatible client.

## Prerequisites

- Python ≥ 3.11
- [`uv`](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

```bash
cd python

# Using uv (recommended)
uv sync

# Or pip
pip install -e .
```

## Environment Variables

Create a `.env` file or export these variables in your shell.

**Authentication — client credentials:**
```bash
AUTH_URL=https://auth.europe-west1.gcp.commercetools.com
API_URL=https://api.europe-west1.gcp.commercetools.com
PROJECT_KEY=my-project
CLIENT_ID=my-client-id
CLIENT_SECRET=my-client-secret
```

**Authentication — existing access token (alternative):**
```bash
AUTH_URL=https://auth.europe-west1.gcp.commercetools.com
API_URL=https://api.europe-west1.gcp.commercetools.com
PROJECT_KEY=my-project
ACCESS_TOKEN=my-access-token
```

**All variables:**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AUTH_URL` | yes | — | Commercetools auth endpoint |
| `API_URL` | yes | — | Commercetools API endpoint |
| `PROJECT_KEY` | yes | — | Commercetools project key |
| `CLIENT_ID` | yes* | — | OAuth client ID (*unless `ACCESS_TOKEN` is set) |
| `CLIENT_SECRET` | yes* | — | OAuth client secret (*unless `ACCESS_TOKEN` is set) |
| `ACCESS_TOKEN` | yes* | — | Pre-existing access token (alternative to client credentials) |
| `IS_ADMIN` | no | `false` | Enable admin-scope tools |
| `CUSTOMER_ID` | no | — | Scope all operations to a customer |
| `STORE_KEY` | no | — | Scope all operations to a store |
| `BUSINESS_UNIT_KEY` | no | — | Scope all operations to a business unit |
| `TOOLS` | no | `all` | Tool selection (see [Tool Selection](#tool-selection)) |
| `TRANSPORT` | no | `stdio` | `stdio` or `http` |
| `HOST` | no | `0.0.0.0` | Bind host for HTTP transport |
| `PORT` | no | `8000` | Bind port for HTTP transport |
| `DYNAMIC_TOOL_LOADING_THRESHOLD` | no | `30` | Switch to dynamic loading above this tool count |
| `LOGGING` | no | `false` | Enable verbose request logging |
| `STATELESS_HTTP` | no | `true` | HTTP transport: stateless mode (no `Mcp-Session-Id`). Set `false` for stateful sessions |
| `CORS_ORIGINS` | no | — | Comma-separated allowed CORS origins for HTTP transport (e.g. `http://localhost:6274`) |

## Running Locally

### stdio mode (default)

Used by Claude Desktop and Claude Code. The MCP client spawns the process directly.

```bash
AUTH_URL=https://auth.europe-west1.gcp.commercetools.com \
API_URL=https://api.europe-west1.gcp.commercetools.com \
PROJECT_KEY=my-project \
CLIENT_ID=my-client-id \
CLIENT_SECRET=my-client-secret \
IS_ADMIN=true \
  commerce-mcp
```

With a `.env` file:

```bash
env $(grep -v '^#' .env | xargs) commerce-mcp
```

### HTTP mode

Starts a Streamable HTTP server, useful for the MCP Inspector and HTTP-based clients.

```bash
AUTH_URL=... API_URL=... PROJECT_KEY=... CLIENT_ID=... CLIENT_SECRET=... IS_ADMIN=true \
  commerce-mcp --transport http --port 8000
```

### Tool Selection

The `--tools` flag (or `TOOLS` env var) controls which tools are exposed:

```bash
commerce-mcp --tools all                        # all tools (default)
commerce-mcp --tools all.read                   # all namespaces, read-only
commerce-mcp --tools products.read,orders.read  # specific namespaces and permissions
commerce-mcp --tools introspect                 # derive permissions from OAuth token scopes
```

## Testing with MCP Inspector

[`@modelcontextprotocol/inspector`](https://github.com/modelcontextprotocol/inspector) provides a browser UI to browse tools, call them, and inspect responses. Requires Node.js.

### Option A — stdio (inspector spawns the server)

The inspector starts the server as a subprocess. Pass environment variables before the command:

```bash
npx @modelcontextprotocol/inspector \
  env \
    AUTH_URL=https://auth.europe-west1.gcp.commercetools.com \
    API_URL=https://api.europe-west1.gcp.commercetools.com \
    PROJECT_KEY=my-project \
    CLIENT_ID=my-client-id \
    CLIENT_SECRET=my-client-secret \
    IS_ADMIN=true \
  commerce-mcp
```

The inspector opens at `http://localhost:5173`. Click **Connect**, then browse and call tools from the UI.

### Option B — HTTP (connect to a running server)

**Terminal 1** — start the server:
```bash
AUTH_URL=... API_URL=... PROJECT_KEY=... CLIENT_ID=... CLIENT_SECRET=... IS_ADMIN=true \
  CORS_ORIGINS=http://localhost:6274 \
  commerce-mcp --transport http --port 8000
```

**Terminal 2** — launch the inspector:
```bash
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
```

Open `http://localhost:5173`, select **Streamable HTTP** as the transport, and connect to `http://localhost:8000/mcp`.

## Running Tests

```bash
cd python

# Install dev dependencies
uv sync --group dev

# Run all tests
uv run pytest

# Run a specific namespace
uv run pytest tests/tools/products/ -v

# Run with output
uv run pytest -s
```

## Claude Desktop Integration

Add the server to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "commercetools": {
      "command": "commerce-mcp",
      "env": {
        "AUTH_URL": "https://auth.europe-west1.gcp.commercetools.com",
        "API_URL": "https://api.europe-west1.gcp.commercetools.com",
        "PROJECT_KEY": "my-project",
        "CLIENT_ID": "my-client-id",
        "CLIENT_SECRET": "my-client-secret",
        "IS_ADMIN": "true"
      }
    }
  }
}
```

See the [root README](../README.md) for the full tool list and additional configuration options.
