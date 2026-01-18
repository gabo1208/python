"""
Technical indicators for trading strategies.
"""
import pandas as pd
import numpy as np


def calculate_sma(data: pd.Series, window: int) -> pd.Series:
    """
    Calculate Simple Moving Average.
    
    Args:
        data: Price data
        window: Window size
        
    Returns:
        SMA values
    """
    return data.rolling(window=window).mean()


def calculate_ema(data: pd.Series, window: int) -> pd.Series:
    """
    Calculate Exponential Moving Average.
    
    Args:
        data: Price data
        window: Window size
        
    Returns:
        EMA values
    """
    return data.ewm(span=window, adjust=False).mean()


def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index.
    
    Args:
        data: Price data
        period: RSI period (default 14)
        
    Returns:
        RSI values (0-100)
    """
    delta = data.diff()
    
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
    """
    Calculate MACD (Moving Average Convergence Divergence).
    
    Args:
        data: Price data
        fast: Fast EMA period
        slow: Slow EMA period
        signal: Signal line period
        
    Returns:
        Tuple of (MACD line, signal line, histogram)
    """
    ema_fast = calculate_ema(data, fast)
    ema_slow = calculate_ema(data, slow)
    
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(data: pd.Series, window: int = 20, num_std: float = 2) -> tuple:
    """
    Calculate Bollinger Bands.
    
    Args:
        data: Price data
        window: Window size
        num_std: Number of standard deviations
        
    Returns:
        Tuple of (upper band, middle band, lower band)
    """
    middle_band = calculate_sma(data, window)
    std = data.rolling(window=window).std()
    
    upper_band = middle_band + (std * num_std)
    lower_band = middle_band - (std * num_std)
    
    return upper_band, middle_band, lower_band


def calculate_momentum(data: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculate price momentum (rate of change).
    
    Args:
        data: Price data
        period: Lookback period
        
    Returns:
        Momentum values (percentage change)
    """
    return ((data - data.shift(period)) / data.shift(period)) * 100


def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Average True Range.
    
    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: ATR period
        
    Returns:
        ATR values
    """
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr


def calculate_stochastic(high: pd.Series, low: pd.Series, close: pd.Series, 
                         k_period: int = 14, d_period: int = 3) -> tuple:
    """
    Calculate Stochastic Oscillator.
    
    Args:
        high: High prices
        low: Low prices
        close: Close prices
        k_period: %K period
        d_period: %D period
        
    Returns:
        Tuple of (%K, %D)
    """
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    
    k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d = k.rolling(window=d_period).mean()
    
    return k, d
