"""
Base strategy class that all trading strategies must inherit from.
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional


class BaseStrategy(ABC):
    """Abstract base class for trading strategies."""
    
    def __init__(self, name: str):
        """
        Initialize strategy.
        
        Args:
            name: Strategy name
        """
        self.name = name
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals from market data.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Series with signals: 1 (buy), -1 (sell), 0 (hold)
        """
        pass
    
    @abstractmethod
    def get_parameters(self) -> dict:
        """
        Get strategy parameters.
        
        Returns:
            Dictionary of parameter names and values
        """
        pass
    
    def __str__(self) -> str:
        """String representation of strategy."""
        params = self.get_parameters()
        param_str = ", ".join(f"{k}={v}" for k, v in params.items())
        return f"{self.name}({param_str})"
