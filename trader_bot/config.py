"""
Configuration settings for the trading bot.
"""

class Config:
    """Trading bot configuration."""
    
    # Initial capital
    INITIAL_CAPITAL = 100000.0
    
    # Trading parameters
    COMMISSION_RATE = 0.001  # 0.1% commission per trade
    SLIPPAGE_RATE = 0.0005   # 0.05% slippage
    
    # Risk management
    MAX_POSITION_SIZE = 0.2  # Maximum 20% of portfolio in single position
    STOP_LOSS_PCT = 0.05     # 5% stop loss
    
    # Strategy parameters
    STRATEGY_PARAMS = {
        'moving_average': {
            'short_window': 20,
            'long_window': 50
        },
        'rsi': {
            'period': 14,
            'oversold': 30,
            'overbought': 70
        },
        'momentum': {
            'lookback_period': 20,
            'threshold': 0.02  # 2% momentum threshold
        }
    }
    
    # Data settings
    DATA_CACHE_DIR = 'data_cache'
    
    # Logging
    LOG_DIR = 'logs'
    LOG_LEVEL = 'INFO'
