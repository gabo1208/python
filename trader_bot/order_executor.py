"""
Simulated order execution with realistic slippage and commissions.
"""
from typing import Optional
from datetime import datetime
from portfolio import Portfolio
from config import Config


class OrderExecutor:
    """Executes buy/sell orders with simulated market conditions."""
    
    def __init__(self, portfolio: Portfolio, config: Config = None):
        """
        Initialize order executor.
        
        Args:
            portfolio: Portfolio instance to execute orders against
            config: Configuration object
        """
        self.portfolio = portfolio
        self.config = config or Config()
        
    def execute_buy(self, symbol: str, price: float, shares: int, date: datetime) -> bool:
        """
        Execute a buy order with slippage and commission.
        
        Args:
            symbol: Stock symbol
            price: Market price
            shares: Number of shares to buy
            date: Transaction date
            
        Returns:
            True if order executed successfully
        """
        # Apply slippage (we pay slightly more)
        execution_price = price * (1 + self.config.SLIPPAGE_RATE)
        
        # Calculate commission
        commission = execution_price * shares * self.config.COMMISSION_RATE
        
        # Check if we can buy
        if not self.portfolio.can_buy(symbol, execution_price, shares, self.config.MAX_POSITION_SIZE):
            return False
        
        try:
            self.portfolio.buy(symbol, execution_price, shares, date, commission)
            return True
        except ValueError:
            return False
    
    def execute_sell(self, symbol: str, price: float, shares: int, date: datetime) -> bool:
        """
        Execute a sell order with slippage and commission.
        
        Args:
            symbol: Stock symbol
            price: Market price
            shares: Number of shares to sell
            date: Transaction date
            
        Returns:
            True if order executed successfully
        """
        # Apply slippage (we receive slightly less)
        execution_price = price * (1 - self.config.SLIPPAGE_RATE)
        
        # Calculate commission
        commission = execution_price * shares * self.config.COMMISSION_RATE
        
        try:
            self.portfolio.sell(symbol, execution_price, shares, date, commission)
            return True
        except ValueError:
            return False
    
    def calculate_shares_to_buy(self, symbol: str, price: float, allocation_pct: float = 0.1) -> int:
        """
        Calculate number of shares to buy based on allocation percentage.
        
        Args:
            symbol: Stock symbol
            price: Current price
            allocation_pct: Percentage of portfolio to allocate (default 10%)
            
        Returns:
            Number of shares to buy
        """
        current_prices = {symbol: price}
        portfolio_value = self.portfolio.get_portfolio_value(current_prices)
        
        # Calculate target allocation
        target_value = portfolio_value * allocation_pct
        
        # Account for slippage and commission
        execution_price = price * (1 + self.config.SLIPPAGE_RATE)
        shares = int(target_value / (execution_price * (1 + self.config.COMMISSION_RATE)))
        
        return max(1, shares)  # At least 1 share
