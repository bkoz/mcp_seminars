#!/usr/bin/env python3
"""
REST Example - Direct API Integration

This CLI tool demonstrates fetching stock quotes using direct REST API calls
to Alpha Vantage. This is the traditional approach without any protocol abstraction.
"""

import argparse
import os
import sys
from rest_stock_client import AlphaVantageRESTClient


def format_quote(quote_data: dict) -> str:
    """Format quote data for display."""
    symbol = quote_data['symbol']
    price = quote_data['price']
    change = quote_data['change']
    change_pct = quote_data['change_percent']
    volume = quote_data['volume']
    trading_day = quote_data['latest_trading_day']

    change_indicator = "+" if float(change) >= 0 else ""

    return f"""
Stock Quote - REST API
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
        description='Fetch stock quotes using REST API',
        epilog='Example: python main.py IBM'
    )
    parser.add_argument('symbol', help='Stock ticker symbol (e.g., IBM, MSFT, GOOGL)')
    args = parser.parse_args()

    api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        print("Error: ALPHA_VANTAGE_API_KEY environment variable not set", file=sys.stderr)
        print("\nSet it with: export ALPHA_VANTAGE_API_KEY=your_api_key_here", file=sys.stderr)
        sys.exit(1)

    try:
        client = AlphaVantageRESTClient(api_key)
        print(f"Fetching quote for {args.symbol.upper()} via REST API...")
        quote = client.get_quote(args.symbol)
        print(format_quote(quote))

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
