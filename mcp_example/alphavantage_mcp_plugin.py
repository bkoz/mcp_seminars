import asyncio
import json
from typing import Dict
import httpx
from stock_plugin import StockDataPlugin


class AlphaVantageMCPPlugin(StockDataPlugin):
    """
    Alpha Vantage implementation using the MCP protocol.

    This plugin connects to the Alpha Vantage MCP server at
    https://mcp.alphavantage.co/mcp and fetches stock data through
    the Model Context Protocol via JSON-RPC over HTTP.
    """

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.server_url = f"https://mcp.alphavantage.co/mcp?apikey={api_key}"
        self.request_id = 0
        self.client = None
        self.initialized = False

    async def _ensure_client(self):
        """Ensure HTTP client is initialized."""
        if not self.client:
            self.client = httpx.AsyncClient(timeout=30.0)

    async def _rpc_call(self, method: str, params: dict = None) -> dict:
        """Make a JSON-RPC call to the MCP server."""
        await self._ensure_client()

        self.request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }

        response = await self.client.post(
            self.server_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()

        result = response.json()
        if "error" in result:
            raise Exception(f"MCP error: {result['error']}")

        return result.get("result", {})

    async def _initialize(self):
        """Initialize the MCP session."""
        if self.initialized:
            return

        result = await self._rpc_call("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "alphavantage-python-client",
                "version": "1.0.0"
            }
        })
        self.initialized = True

    async def _list_tools(self) -> list:
        """List available tools from the MCP server."""
        await self._initialize()
        result = await self._rpc_call("tools/list")
        return result.get("tools", [])

    def get_quote(self, symbol: str) -> Dict:
        """
        Fetch stock quote via MCP protocol.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary with quote data matching REST format
        """
        return asyncio.run(self._get_quote_async(symbol))

    async def _get_quote_async(self, symbol: str) -> Dict:
        """Async implementation of get_quote."""
        await self._initialize()

        try:
            # Alpha Vantage MCP server uses a special TOOL_CALL interface
            # We call TOOL_CALL with the tool name and arguments
            result = await self._rpc_call("tools/call", {
                "name": "TOOL_CALL",
                "arguments": {
                    "tool_name": "GLOBAL_QUOTE",
                    "arguments": json.dumps({"symbol": symbol.upper()})
                }
            })

            # Extract content from MCP response
            content = result.get("content", [])
            if not content:
                raise ValueError(f"No data available for symbol: {symbol}")

            # Parse the tool response - it returns CSV format
            csv_text = content[0].get("text", "") if content else ""
            if not csv_text:
                raise ValueError(f"No data available for symbol: {symbol}")

            # Parse CSV: first line is header, second line is data
            # Handle both \n and \r\n line endings
            lines = csv_text.strip().replace('\r\n', '\n').split('\n')
            if len(lines) < 2:
                raise ValueError(f"Invalid response format for symbol: {symbol}")

            headers = [h.strip() for h in lines[0].split(',')]
            values = [v.strip() for v in lines[1].split(',')]

            # Create a dict from the CSV
            data = dict(zip(headers, values))

            # Transform to match REST format
            return {
                'symbol': data.get('symbol', symbol.upper()),
                'price': data.get('price', ''),
                'volume': data.get('volume', ''),
                'latest_trading_day': data.get('latestDay', ''),
                'previous_close': data.get('previousClose', ''),
                'change': data.get('change', ''),
                'change_percent': data.get('changePercent', '')
            }

        except httpx.HTTPError as e:
            raise Exception(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse response: {e}")
        except Exception as e:
            raise Exception(f"MCP request failed: {e}")

    def close(self):
        """Close the HTTP client."""
        if self.client:
            asyncio.run(self._close_async())

    async def _close_async(self):
        """Async close implementation."""
        if self.client:
            await self.client.aclose()
            self.client = None
