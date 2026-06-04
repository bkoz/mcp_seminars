#!/usr/bin/env python3
"""
MCP Example - Protocol-Based Integration

This CLI tool demonstrates fetching stock quotes using the Model Context Protocol.
It uses a plugin architecture that makes swapping MCP servers trivial.
"""

import argparse
import os
import sys
from alphavantage_mcp_plugin import AlphaVantageMCPPlugin


def format_quote(quote_data: dict) -> str:
    """Format quote data for display."""
    symbol = quote_data['symbol']
    price = quote_data['price']
    change = quote_data['change']
    change_pct = quote_data['change_percent']
    volume = quote_data['volume']
    trading_day = quote_data['latest_trading_day']

    try:
        change_indicator = "+" if float(change) >= 0 else ""
    except (ValueError, TypeError):
        change_indicator = ""

    return f"""
Stock Quote - MCP Protocol
{'=' * 50}
Symbol:              {symbol}
Price:               ${price}
Change:              {change_indicator}{change} ({change_pct})
Volume:              {volume}
Latest Trading Day:  {trading_day}
{'=' * 50}
    """.strip()


def main():
    parser = argparse.ArgumentParser(
        description='Fetch stock quotes using MCP protocol',
        epilog='Example: python main.py IBM'
    )
    parser.add_argument('symbol', help='Stock ticker symbol (e.g., IBM, MSFT, GOOGL)')
    args = parser.parse_args()

    api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        print("Error: ALPHA_VANTAGE_API_KEY environment variable not set", file=sys.stderr)
        print("\nSet it with: export ALPHA_VANTAGE_API_KEY=your_api_key_here", file=sys.stderr)
        sys.exit(1)

    plugin = None
    try:
        plugin = AlphaVantageMCPPlugin(api_key)
        print(f"Fetching quote for {args.symbol.upper()} via MCP protocol...")
        quote = plugin.get_quote(args.symbol)
        print(format_quote(quote))

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        import traceback
        print(f"Unexpected error: {e}", file=sys.stderr)
        print("\nFull traceback:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    finally:
        if plugin:
            try:
                plugin.close()
            except:
                pass  # Ignore cleanup errors


if __name__ == '__main__':
    main()
