# MCP Implementation Notes

## Successfully Debugged and Implemented

The MCP example is now fully working! Here's what was learned during implementation:

### Alpha Vantage MCP Server Architecture

The server at `https://mcp.alphavantage.co/mcp?apikey=<key>` uses a unique progressive tool discovery pattern:

**Tools Available:**
- `TOOL_LIST` - Lists all available Alpha Vantage API tools
- `TOOL_GET(tool_name)` - Gets the schema for a specific tool
- `TOOL_CALL(tool_name, arguments)` - Executes a tool with arguments

### Key Implementation Details

1. **Transport:** JSON-RPC over HTTP POST (not SSE/stdio)
2. **Response Format:** CSV by default (not JSON)
3. **Tool Invocation:** Nested structure using `TOOL_CALL`

### Example Tool Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "TOOL_CALL",
    "arguments": {
      "tool_name": "GLOBAL_QUOTE",
      "arguments": "{\"symbol\": \"IBM\"}"
    }
  }
}
```

### Response Format

The server returns CSV:
```
symbol,open,high,low,price,volume,latestDay,previousClose,change,changePercent
IBM,318.2950,318.2950,302.5301,305.6300,13926558,2026-06-03,329.2300,-23.6000,-7.1682%
```

### Implementation Approach

**Final Solution:**
- Used `httpx` for async HTTP requests
- Direct JSON-RPC calls instead of MCP SDK's SSE/stdio clients
- CSV parsing for response data
- Proper async/await handling throughout

### Testing Commands

**Using npx MCP inspector:**
```bash
npx @modelcontextprotocol/inspector --cli \
  --method=tools/call \
  --tool-name="TOOL_CALL" \
  --tool-arg=tool_name=GLOBAL_QUOTE \
  --tool-arg='arguments={"symbol": "IBM"}' \
  -- https://mcp.alphavantage.co/mcp?apikey=$ALPHA_VANTAGE_API_KEY
```

**Using the Python client:**
```bash
uv run mcp_example/main.py IBM
```

### Lessons Learned

1. **MCP servers can use different transports** - This one uses HTTP POST, not SSE
2. **Response formats vary** - Don't assume JSON; this returns CSV
3. **Progressive tool discovery** - The TOOL_LIST/TOOL_GET/TOOL_CALL pattern reduces token usage
4. **Testing tools are essential** - The MCP inspector was crucial for debugging
5. **Documentation matters** - The server structure wasn't obvious without testing

### Performance Notes

- Both REST and MCP approaches fetch the same data
- MCP adds overhead (initialization, tool discovery) but provides standardization
- CSV parsing is fast and lightweight
- API rate limits apply equally to both approaches (25 requests/day on free tier)

## Comparison: REST vs MCP

| Aspect | REST | MCP |
|--------|------|-----|
| Lines of Code | ~75 | ~150 |
| Complexity | Low | Medium |
| Setup | Direct HTTP | JSON-RPC protocol |
| Response Format | JSON | CSV (in this case) |
| Abstraction | None | Tool calling interface |
| Swappability | Requires code changes | Plugin interface |
| Learning Curve | Shallow | Steeper |

