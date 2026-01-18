"""
Portfolio manager for tracking positions and performance.
"""
from typing import Dict, Optional
from datetime import datetime


class Portfolio:
    """Manages portfolio positions, cash, and performance tracking."""
    
    def __init__(self, initial_capital: float):
        """
        Initialize portfolio.
        
        Args:
            initial_capital: Starting cash balance
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, dict] = {}  # symbol -> {shares, avg_price, value}
        self.trade_history = []
        self.equity_curve = []
        
    def get_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        """
        Calculate total portfolio value.
        
        Args:
            current_prices: Dictionary of symbol -> current price
            
        Returns:
            Total portfolio value (cash + positions)
        """
        positions_value = sum(
            pos['shares'] * current_prices.get(symbol, pos['avg_price'])
            for symbol, pos in self.positions.items()
        )
        return self.cash + positions_value
    
    def get_position_size(self, symbol: str) -> int:
        """Get number of shares held for a symbol."""
        return self.positions.get(symbol, {}).get('shares', 0)
    
    def can_buy(self, symbol: str, price: float, shares: int, max_position_pct: float) -> bool:
        """
        Check if we can buy shares.
        
        Args:
            symbol: Stock symbol
            price: Current price
            shares: Number of shares to buy
            max_position_pct: Maximum position size as percentage of portfolio
            
        Returns:
            True if purchase is allowed
        """
        cost = price * shares
        
        # Check if we have enough cash
        if cost > self.cash:
            return False
        
        # Check position size limit
        current_value = self.get_portfolio_value({symbol: price})
        position_value = self.positions.get(symbol, {}).get('shares', 0) * price + cost
        
        if position_value > current_value * max_position_pct:
            return False
        
        return True
    
    def buy(self, symbol: str, price: float, shares: int, date: datetime, commission: float = 0):
        """
        Execute a buy order.
        
        Args:
            symbol: Stock symbol
            price: Purchase price
            shares: Number of shares
            date: Transaction date
            commission: Commission fee
        """
        cost = price * shares + commission
        
        if cost > self.cash:
            raise ValueError(f"Insufficient funds: need ${cost:.2f}, have ${self.cash:.2f}")
        
        self.cash -= cost
        
        # Update position
        if symbol in self.positions:
            current_shares = self.positions[symbol]['shares']
            current_value = current_shares * self.positions[symbol]['avg_price']
            new_shares = current_shares + shares
            new_avg_price = (current_value + price * shares) / new_shares
            
            self.positions[symbol] = {
                'shares': new_shares,
                'avg_price': new_avg_price,
                'value': new_shares * price
            }
        else:
            self.positions[symbol] = {
                'shares': shares,
                'avg_price': price,
                'value': shares * price
            }
        
        # Record trade
        self.trade_history.append({
            'date': date,
            'symbol': symbol,
            'action': 'BUY',
            'shares': shares,
            'price': price,
            'commission': commission,
            'total': cost
        })
    
    def sell(self, symbol: str, price: float, shares: int, date: datetime, commission: float = 0):
        """
        Execute a sell order.
        
        Args:
            symbol: Stock symbol
            price: Sale price
            shares: Number of shares
            date: Transaction date
            commission: Commission fee
        """
        if symbol not in self.positions:
            raise ValueError(f"No position in {symbol}")
        
        current_shares = self.positions[symbol]['shares']
        if shares > current_shares:
            raise ValueError(f"Cannot sell {shares} shares, only have {current_shares}")
        
        proceeds = price * shares - commission
        self.cash += proceeds
        
        # Update position
        remaining_shares = current_shares - shares
        if remaining_shares == 0:
            del self.positions[symbol]
        else:
            self.positions[symbol]['shares'] = remaining_shares
            self.positions[symbol]['value'] = remaining_shares * price
        
        # Record trade
        self.trade_history.append({
            'date': date,
            'symbol': symbol,
            'action': 'SELL',
            'shares': shares,
            'price': price,
            'commission': commission,
            'total': proceeds
        })
    
    def record_equity(self, date: datetime, current_prices: Dict[str, float]):
        """Record portfolio value at a point in time."""
        value = self.get_portfolio_value(current_prices)
        self.equity_curve.append({
            'date': date,
            'value': value,
            'cash': self.cash,
            'positions_value': value - self.cash
        })
    
    def get_returns(self) -> float:
        """Calculate total return percentage."""
        if not self.equity_curve:
            return 0.0
        final_value = self.equity_curve[-1]['value']
        return ((final_value - self.initial_capital) / self.initial_capital) * 100
    
    def get_trade_count(self) -> int:
        """Get total number of trades executed."""
        return len(self.trade_history)
