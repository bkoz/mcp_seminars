import requests
from typing import Dict, Optional


class AlphaVantageRESTClient:
    """
    Direct REST API client for Alpha Vantage stock data.

    This implementation makes direct HTTP requests to the Alpha Vantage API
    endpoints without any abstraction layer.
    """

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key

    def get_quote(self, symbol: str) -> Dict:
        """
        Fetch real-time stock quote for the given symbol.

        Args:
            symbol: Stock ticker symbol (e.g., 'IBM', 'MSFT')

        Returns:
            Dictionary containing quote data with keys like:
            - symbol
            - price
            - volume
            - change
            - change_percent

        Raises:
            requests.RequestException: If the API request fails
            ValueError: If the response is invalid or symbol not found
        """
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol.upper(),
            'apikey': self.api_key
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'Global Quote' not in data:
                if 'Error Message' in data:
                    raise ValueError(f"Invalid symbol: {symbol}")
                elif 'Note' in data:
                    raise ValueError(f"API rate limit reached: {data['Note']}")
                else:
                    raise ValueError(f"Unexpected API response: {data}")

            quote_data = data['Global Quote']
            if not quote_data:
                raise ValueError(f"No data available for symbol: {symbol}")

            return {
                'symbol': quote_data.get('01. symbol', ''),
                'price': quote_data.get('05. price', ''),
                'volume': quote_data.get('06. volume', ''),
                'latest_trading_day': quote_data.get('07. latest trading day', ''),
                'previous_close': quote_data.get('08. previous close', ''),
                'change': quote_data.get('09. change', ''),
                'change_percent': quote_data.get('10. change percent', '')
            }

        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch quote: {e}")
