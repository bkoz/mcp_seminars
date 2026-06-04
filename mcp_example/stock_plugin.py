from abc import ABC, abstractmethod
from typing import Dict


class StockDataPlugin(ABC):
    """
    Abstract base class for stock data sources.

    This interface defines the contract that any stock data provider
    (via MCP or other protocols) must implement. This enables easy
    swapping between different MCP servers or data sources.
    """

    @abstractmethod
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
            Exception: If the data fetch fails
        """
        pass

    @abstractmethod
    def close(self):
        """
        Clean up any resources (connections, sessions, etc.).
        """
        pass
