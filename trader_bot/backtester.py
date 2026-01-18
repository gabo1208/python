"""
Backtesting engine for testing trading strategies on historical data.
"""
import pandas as pd
from typing import Dict, List
from datetime import datetime
from portfolio import Portfolio
from order_executor import OrderExecutor
from strategies.base_strategy import BaseStrategy
from data_fetcher import DataFetcher
from config import Config


class Backtester:
    """Backtests trading strategies on historical data."""
    
    def __init__(self, strategy: BaseStrategy, initial_capital: float = 100000, config: Config = None):
        """
        Initialize backtester.
        
        Args:
            strategy: Trading strategy to test
            initial_capital: Starting capital
            config: Configuration object
        """
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.config = config or Config()
        self.results = None
        
    def run(self, symbol: str, start_date: str, end_date: str, data_fetcher: DataFetcher = None) -> Dict:
        """
        Run backtest on a single symbol.
        
        Args:
            symbol: Stock symbol to trade
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            data_fetcher: DataFetcher instance (creates new one if None)
            
        Returns:
            Dictionary with backtest results
        """
        # Fetch data
        if data_fetcher is None:
            data_fetcher = DataFetcher(self.config.DATA_CACHE_DIR)
        
        print(f"\n{'='*60}")
        print(f"Running backtest: {self.strategy}")
        print(f"Symbol: {symbol}")
        print(f"Period: {start_date} to {end_date}")
        print(f"Initial Capital: ${self.initial_capital:,.2f}")
        print(f"{'='*60}\n")
        
        data = data_fetcher.get_historical_data(symbol, start_date, end_date)
        
        # Generate signals
        signals = self.strategy.generate_signals(data)
        
        # Initialize portfolio and executor
        portfolio = Portfolio(self.initial_capital)
        executor = OrderExecutor(portfolio, self.config)
        
        # Execute trades based on signals
        for date, signal in signals.items():
            current_price = data.loc[date, 'Close']
            current_prices = {symbol: current_price}
            
            if signal == 1:  # Buy signal
                # Calculate shares to buy (10% of portfolio)
                shares = executor.calculate_shares_to_buy(symbol, current_price, allocation_pct=0.1)
                
                if shares > 0:
                    success = executor.execute_buy(symbol, current_price, shares, date)
                    if success:
                        print(f"{date.date()}: BUY  {shares} shares @ ${current_price:.2f}")
            
            elif signal == -1:  # Sell signal
                # Sell all shares
                position_size = portfolio.get_position_size(symbol)
                
                if position_size > 0:
                    success = executor.execute_sell(symbol, current_price, position_size, date)
                    if success:
                        print(f"{date.date()}: SELL {position_size} shares @ ${current_price:.2f}")
            
            # Record portfolio value
            portfolio.record_equity(date, current_prices)
        
        # Close any open positions at the end
        final_date = data.index[-1]
        final_price = data.loc[final_date, 'Close']
        position_size = portfolio.get_position_size(symbol)
        
        if position_size > 0:
            executor.execute_sell(symbol, final_price, position_size, final_date)
            print(f"{final_date.date()}: SELL {position_size} shares @ ${final_price:.2f} (closing position)")
        
        # Calculate results
        self.results = self._calculate_results(portfolio, data, symbol)
        
        return self.results
    
    def _calculate_results(self, portfolio: Portfolio, data: pd.DataFrame, symbol: str) -> Dict:
        """Calculate backtest performance metrics."""
        equity_curve = pd.DataFrame(portfolio.equity_curve)
        
        # Basic metrics
        final_value = equity_curve['value'].iloc[-1]
        total_return = ((final_value - self.initial_capital) / self.initial_capital) * 100
        
        # Calculate returns
        equity_curve['returns'] = equity_curve['value'].pct_change()
        
        # Sharpe ratio (annualized, assuming 252 trading days)
        mean_return = equity_curve['returns'].mean()
        std_return = equity_curve['returns'].std()
        sharpe_ratio = (mean_return / std_return) * (252 ** 0.5) if std_return > 0 else 0
        
        # Maximum drawdown
        cumulative = (1 + equity_curve['returns']).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        # Win rate
        trades = portfolio.trade_history
        buy_trades = [t for t in trades if t['action'] == 'BUY']
        sell_trades = [t for t in trades if t['action'] == 'SELL']
        
        winning_trades = 0
        total_trades = min(len(buy_trades), len(sell_trades))
        
        for i in range(total_trades):
            if sell_trades[i]['price'] > buy_trades[i]['price']:
                winning_trades += 1
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Buy and hold comparison
        buy_hold_return = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
        
        results = {
            'strategy': str(self.strategy),
            'symbol': symbol,
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'buy_hold_return': buy_hold_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_trades': total_trades,
            'win_rate': win_rate,
            'equity_curve': equity_curve,
            'trade_history': trades,
            'portfolio': portfolio
        }
        
        return results
    
    def print_results(self):
        """Print backtest results summary."""
        if self.results is None:
            print("No results available. Run backtest first.")
            return
        
        r = self.results
        
        print(f"\n{'='*60}")
        print(f"BACKTEST RESULTS")
        print(f"{'='*60}")
        print(f"Strategy:          {r['strategy']}")
        print(f"Symbol:            {r['symbol']}")
        print(f"Initial Capital:   ${r['initial_capital']:,.2f}")
        print(f"Final Value:       ${r['final_value']:,.2f}")
        print(f"Total Return:      {r['total_return']:.2f}%")
        print(f"Buy & Hold Return: {r['buy_hold_return']:.2f}%")
        print(f"Sharpe Ratio:      {r['sharpe_ratio']:.2f}")
        print(f"Max Drawdown:      {r['max_drawdown']:.2f}%")
        print(f"Total Trades:      {r['total_trades']}")
        print(f"Win Rate:          {r['win_rate']:.2f}%")
        print(f"{'='*60}\n")
