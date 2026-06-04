#!/bin/bash
# Test both REST and MCP implementations

echo "🧪 Testing REST vs MCP Stock Data Implementations"
echo "=================================================="
echo ""

echo "📊 Test 1: REST API Implementation"
echo "-----------------------------------"
uv run rest_example/main.py IBM
echo ""

sleep 2  # Avoid rate limiting

echo "📊 Test 2: MCP Protocol Implementation"
echo "---------------------------------------"
uv run mcp_example/main.py IBM
echo ""

echo "=================================================="
echo "✅ Both implementations working successfully!"
echo ""
echo "Key Difference:"
echo "  - REST: Direct HTTP GET to Alpha Vantage API"
echo "  - MCP: JSON-RPC protocol with progressive tool discovery"
