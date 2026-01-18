"""
RSI (Relative Strength Index) strategy.
"""
import pandas as pd
from strategies.base_strategy import BaseStrategy
from indicators import calculate_rsi


class RSIStrategy(BaseStrategy):
    """
    RSI Strategy.
    
    Buys when RSI indicates oversold conditions (RSI < oversold_threshold).
    Sells when RSI indicates overbought conditions (RSI > overbought_threshold).
    """
    
    def __init__(self, period: int = 14, oversold: int = 30, overbought: int = 70):
        """
        Initialize strategy.
        
        Args:
            period: RSI calculation period
            oversold: Oversold threshold (buy signal)
            overbought: Overbought threshold (sell signal)
        """
        super().__init__("RSI Strategy")
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on RSI.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Series with signals: 1 (buy), -1 (sell), 0 (hold)
        """
        # Calculate RSI
        rsi = calculate_rsi(data['Close'], self.period)
        
        # Initialize signals
        signals = pd.Series(0, index=data.index)
        
        # Track position state
        position = 0  # 0 = no position, 1 = long position
        
        for i in range(len(data)):
            if pd.isna(rsi.iloc[i]):
                continue
                
            # Buy signal: RSI crosses below oversold threshold
            if rsi.iloc[i] < self.oversold and position == 0:
                signals.iloc[i] = 1
                position = 1
            
            # Sell signal: RSI crosses above overbought threshold
            elif rsi.iloc[i] > self.overbought and position == 1:
                signals.iloc[i] = -1
                position = 0
        
        return signals
    
    def get_parameters(self) -> dict:
        """Get strategy parameters."""
        return {
            'period': self.period,
            'oversold': self.oversold,
            'overbought': self.overbought
        }
