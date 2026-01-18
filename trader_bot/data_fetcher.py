"""
Fetches historical market data using yfinance.
"""
import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime
import os


class DataFetcher:
    """Fetches and caches historical market data."""
    
    def __init__(self, cache_dir: str = 'data_cache'):
        """
        Initialize data fetcher.
        
        Args:
            cache_dir: Directory to cache downloaded data
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def get_historical_data(self, symbol: str, start_date: str, end_date: str, 
                           use_cache: bool = True) -> pd.DataFrame:
        """
        Fetch historical OHLCV data for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            use_cache: Whether to use cached data if available
            
        Returns:
            DataFrame with OHLCV data
        """
        cache_file = self.cache_dir / f"{symbol}_{start_date}_{end_date}.csv"
        
        # Check cache
        if use_cache and cache_file.exists():
            print(f"Loading {symbol} from cache...")
            return pd.read_csv(cache_file, index_col=0, parse_dates=True)
        
        # Download data
        print(f"Downloading {symbol} data...")
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                raise ValueError(f"No data found for {symbol}")
            
            # Cache the data
            data.to_csv(cache_file)
            
            return data
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            raise
    
    def get_current_price(self, symbol: str) -> float:
        """
        Get current price for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Current price
        """
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        
        if data.empty:
            raise ValueError(f"Could not fetch current price for {symbol}")
        
        return data['Close'].iloc[-1]
    
    def get_multiple_symbols(self, symbols: list, start_date: str, end_date: str) -> dict:
        """
        Fetch data for multiple symbols.
        
        Args:
            symbols: List of stock symbols
            start_date: Start date
            end_date: End date
            
        Returns:
            Dictionary of symbol -> DataFrame
        """
        data = {}
        for symbol in symbols:
            try:
                data[symbol] = self.get_historical_data(symbol, start_date, end_date)
            except Exception as e:
                print(f"Skipping {symbol}: {e}")
        
        return data
    
    def clear_cache(self):
        """Clear all cached data."""
        for file in self.cache_dir.glob("*.csv"):
            file.unlink()
        print("Cache cleared.")
