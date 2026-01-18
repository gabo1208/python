"""
Moving Average Crossover strategy.
"""
import pandas as pd
from strategies.base_strategy import BaseStrategy
from indicators import calculate_sma


class MovingAverageStrategy(BaseStrategy):
    """
    Moving Average Crossover Strategy.
    
    Generates buy signal when short MA crosses above long MA.
    Generates sell signal when short MA crosses below long MA.
    """
    
    def __init__(self, short_window: int = 20, long_window: int = 50):
        """
        Initialize strategy.
        
        Args:
            short_window: Short moving average window
            long_window: Long moving average window
        """
        super().__init__("Moving Average Crossover")
        self.short_window = short_window
        self.long_window = long_window
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on MA crossover.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Series with signals: 1 (buy), -1 (sell), 0 (hold)
        """
        # Calculate moving averages
        short_ma = calculate_sma(data['Close'], self.short_window)
        long_ma = calculate_sma(data['Close'], self.long_window)
        
        # Initialize signals
        signals = pd.Series(0, index=data.index)
        
        # Generate signals
        # Buy when short MA crosses above long MA
        signals[short_ma > long_ma] = 1
        
        # Sell when short MA crosses below long MA
        signals[short_ma < long_ma] = -1
        
        # Only signal on crossover (change in position)
        signals = signals.diff()
        signals.fillna(0, inplace=True)
        
        # Convert to discrete signals: 1 for buy, -1 for sell, 0 for hold
        signals[signals > 0] = 1
        signals[signals < 0] = -1
        
        return signals
    
    def get_parameters(self) -> dict:
        """Get strategy parameters."""
        return {
            'short_window': self.short_window,
            'long_window': self.long_window
        }
