# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a learning project that demonstrates two different architectural approaches to fetching stock data from Alpha Vantage:
1. **REST example**: Traditional direct HTTP API calls
2. **MCP example**: Model Context Protocol with plugin architecture

Both implementations fetch real-time stock quotes but use fundamentally different integration patterns.

## Project Structure

```
mcp_seminar_session_2/
├── rest_example/
│   ├── rest_stock_client.py  # Direct REST API client
│   └── main.py               # CLI for REST approach
├── mcp_example/
│   ├── stock_plugin.py       # Abstract plugin interface
│   ├── alphavantage_mcp_plugin.py  # MCP implementation
│   └── main.py               # CLI for MCP approach
├── requirements.txt          # Python dependencies
├── .env.example             # API key template
└── README.md                # Full comparison documentation
```

## Key Architectural Differences

**REST Example (`rest_example/`)**
- Direct HTTP GET requests to `https://www.alphavantage.co/query`
- Uses `requests` library
- Stateless - each request is independent
- Tightly coupled to Alpha Vantage API structure
- Simple, minimal abstraction

**MCP Example (`mcp_example/`)**
- Uses Model Context Protocol via official `mcp` Python SDK
- Stateful session with MCP server
- Plugin architecture via `StockDataPlugin` abstract base class
- Loosely coupled - easy to swap MCP servers
- More abstraction, enables modularity

## Development Setup

**Install dependencies using uv:**
```bash
uv pip install -r requirements.txt
```

**Set API key:**
```bash
export ALPHA_VANTAGE_API_KEY=your_api_key_here
```

Or copy `.env.example` to `.env` and add your key.

**Note:** This project uses `uv` for Python dependency management and running programs.

## Running the Examples

**REST version:**
```bash
uv run rest_example/main.py IBM
```

**MCP version:**
```bash
uv run mcp_example/main.py IBM
```

Both should produce similar output with stock quote data.

## Testing

**Quick test both approaches:**
```bash
# REST
uv run rest_example/main.py MSFT

# MCP
uv run mcp_example/main.py MSFT
```

**Test error handling:**
```bash
# Invalid symbol
uv run rest_example/main.py INVALID

# Missing API key
unset ALPHA_VANTAGE_API_KEY
uv run rest_example/main.py IBM
```

## API Limitations

- Alpha Vantage free tier: 25 requests per day
- Rate limit errors are handled gracefully in both implementations

## Extension Points

**To add a new MCP stock server:**
1. Create new class extending `StockDataPlugin` in `mcp_example/`
2. Implement `get_quote(symbol)` method
3. Implement `close()` for cleanup
4. Update `main.py` to use the new plugin

Example: `FinnhubMCPPlugin`, `PolygonMCPPlugin`, etc.

## Important Notes

- Both implementations return the same data structure for easy comparison
- The MCP version uses async/await internally but presents a synchronous interface
- Plugin architecture in MCP example demonstrates the key benefit: swappable providers without client code changes
- This is a learning project focused on architectural patterns, not production-ready code

## MCP Server Details

The Alpha Vantage MCP server at `https://mcp.alphavantage.co/mcp` uses:
- **Transport**: JSON-RPC over HTTP POST (not SSE/stdio)
- **Response format**: CSV (not JSON)
- **Tool pattern**: Progressive tool discovery (`TOOL_LIST`, `TOOL_GET`, `TOOL_CALL`)
- **Dependencies**: `httpx` for async HTTP requests

See `IMPLEMENTATION_NOTES.md` for detailed debugging and implementation notes.
