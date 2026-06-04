# Quick Start Guide

Get up and running in 3 minutes.

## Step 1: Install Dependencies

Using `uv` (recommended - fast, modern Python package manager):
```bash
uv pip install -r requirements.txt
```

Or with pip:
```bash
pip install -r requirements.txt
```

This installs:
- `requests` - for REST API calls
- `mcp` - for Model Context Protocol

## Step 2: Set Your API Key

Get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key), then:

```bash
export ALPHA_VANTAGE_API_KEY=your_actual_key_here
```

## Step 3: Verify Setup

```bash
uv run verify_setup.py
```

Should show all green checkmarks ✓

## Step 4: Run Examples

**REST Example:**
```bash
uv run rest_example/main.py IBM
```

**MCP Example:**
```bash
uv run mcp_example/main.py IBM
```

Both fetch the same Apple stock data using different architectural approaches.

## Try More Symbols

```bash
uv run rest_example/main.py MSFT    # Microsoft
uv run rest_example/main.py GOOGL   # Google
uv run rest_example/main.py TSLA    # Tesla
uv run rest_example/main.py NVDA    # NVIDIA

# Same with MCP
uv run mcp_example/main.py MSFT
```

## Compare Output

Run both and see they return the same data:

```bash
uv run rest_example/main.py IBM > rest_out.txt
uv run mcp_example/main.py IBM > mcp_out.txt
cat rest_out.txt
cat mcp_out.txt
```

## What's the Difference?

- **REST** (`rest_example/`): Direct HTTP requests to Alpha Vantage API
- **MCP** (`mcp_example/`): Uses Model Context Protocol with plugin architecture

See [README.md](README.md) for detailed comparison.

## Troubleshooting

**"Module not found" error?**
```bash
uv pip install -r requirements.txt
```

**"API key not set" error?**
```bash
export ALPHA_VANTAGE_API_KEY=your_key
```

**Rate limit error?**
Free tier allows 25 requests/day. Wait or upgrade your API key.

**Invalid symbol?**
Use valid stock tickers like IBM, MSFT, GOOGL, TSLA, etc.
