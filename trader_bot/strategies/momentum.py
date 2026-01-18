"""
Momentum-based trading strategy.
"""
import pandas as pd
from strategies.base_strategy import BaseStrategy
from indicators import calculate_momentum


class MomentumStrategy(BaseStrategy):
    """
    Momentum Strategy.
    
    Buys when positive momentum exceeds threshold.
    Sells when negative momentum exceeds threshold.
    """
    
    def __init__(self, lookback_period: int = 20, threshold: float = 0.02):
        """
        Initialize strategy.
        
        Args:
            lookback_period: Period for momentum calculation
            threshold: Momentum threshold (as decimal, e.g., 0.02 = 2%)
        """
        super().__init__("Momentum Strategy")
        self.lookback_period = lookback_period
        self.threshold = threshold * 100  # Convert to percentage
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on momentum.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Series with signals: 1 (buy), -1 (sell), 0 (hold)
        """
        # Calculate momentum
        momentum = calculate_momentum(data['Close'], self.lookback_period)
        
        # Initialize signals
        signals = pd.Series(0, index=data.index)
        
        # Track position state
        position = 0  # 0 = no position, 1 = long position
        
        for i in range(len(data)):
            if pd.isna(momentum.iloc[i]):
                continue
            
            # Buy signal: strong positive momentum
            if momentum.iloc[i] > self.threshold and position == 0:
                signals.iloc[i] = 1
                position = 1
            
            # Sell signal: momentum turns negative or weakens significantly
            elif (momentum.iloc[i] < -self.threshold or momentum.iloc[i] < self.threshold / 2) and position == 1:
                signals.iloc[i] = -1
                position = 0
        
        return signals
    
    def get_parameters(self) -> dict:
        """Get strategy parameters."""
        return {
            'lookback_period': self.lookback_period,
            'threshold': f"{self.threshold}%"
        }
