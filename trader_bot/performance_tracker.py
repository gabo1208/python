"""
Performance tracking and metrics calculation.
"""
import pandas as pd
import numpy as np
from typing import Dict, List


class PerformanceTracker:
    """Tracks and calculates trading performance metrics."""
    
    @staticmethod
    def calculate_metrics(equity_curve: pd.DataFrame, trade_history: List[Dict], 
                         initial_capital: float) -> Dict:
        """
        Calculate comprehensive performance metrics.
        
        Args:
            equity_curve: DataFrame with portfolio values over time
            trade_history: List of trade dictionaries
            initial_capital: Starting capital
            
        Returns:
            Dictionary of performance metrics
        """
        if equity_curve.empty:
            return {}
        
        # Total return
        final_value = equity_curve['value'].iloc[-1]
        total_return = ((final_value - initial_capital) / initial_capital) * 100
        
        # Daily returns
        equity_curve['returns'] = equity_curve['value'].pct_change()
        
        # Annualized return (assuming 252 trading days)
        days = len(equity_curve)
        years = days / 252
        annualized_return = ((final_value / initial_capital) ** (1 / years) - 1) * 100 if years > 0 else 0
        
        # Volatility (annualized)
        volatility = equity_curve['returns'].std() * np.sqrt(252) * 100
        
        # Sharpe ratio (annualized, assuming risk-free rate = 0)
        mean_return = equity_curve['returns'].mean()
        std_return = equity_curve['returns'].std()
        sharpe_ratio = (mean_return / std_return) * np.sqrt(252) if std_return > 0 else 0
        
        # Sortino ratio (downside deviation)
        downside_returns = equity_curve['returns'][equity_curve['returns'] < 0]
        downside_std = downside_returns.std()
        sortino_ratio = (mean_return / downside_std) * np.sqrt(252) if downside_std > 0 else 0
        
        # Maximum drawdown
        cumulative = (1 + equity_curve['returns']).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        # Calmar ratio (return / max drawdown)
        calmar_ratio = abs(annualized_return / max_drawdown) if max_drawdown != 0 else 0
        
        # Trade statistics
        buy_trades = [t for t in trade_history if t['action'] == 'BUY']
        sell_trades = [t for t in trade_history if t['action'] == 'SELL']
        
        total_trades = min(len(buy_trades), len(sell_trades))
        
        if total_trades > 0:
            # Calculate profit/loss for each trade
            trade_pnl = []
            winning_trades = 0
            losing_trades = 0
            
            for i in range(total_trades):
                buy_cost = buy_trades[i]['price'] * buy_trades[i]['shares'] + buy_trades[i]['commission']
                sell_proceeds = sell_trades[i]['price'] * sell_trades[i]['shares'] - sell_trades[i]['commission']
                pnl = sell_proceeds - buy_cost
                trade_pnl.append(pnl)
                
                if pnl > 0:
                    winning_trades += 1
                else:
                    losing_trades += 1
            
            win_rate = (winning_trades / total_trades) * 100
            avg_win = np.mean([p for p in trade_pnl if p > 0]) if winning_trades > 0 else 0
            avg_loss = np.mean([p for p in trade_pnl if p < 0]) if losing_trades > 0 else 0
            profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else 0
        else:
            win_rate = 0
            avg_win = 0
            avg_loss = 0
            profit_factor = 0
            winning_trades = 0
            losing_trades = 0
        
        return {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'max_drawdown': max_drawdown,
            'calmar_ratio': calmar_ratio,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'final_value': final_value
        }
    
    @staticmethod
    def compare_strategies(results_list: List[Dict]) -> pd.DataFrame:
        """
        Compare multiple strategy results.
        
        Args:
            results_list: List of backtest result dictionaries
            
        Returns:
            DataFrame comparing strategies
        """
        comparison = []
        
        for result in results_list:
            comparison.append({
                'Strategy': result['strategy'],
                'Symbol': result['symbol'],
                'Total Return (%)': f"{result['total_return']:.2f}",
                'Sharpe Ratio': f"{result['sharpe_ratio']:.2f}",
                'Max Drawdown (%)': f"{result['max_drawdown']:.2f}",
                'Win Rate (%)': f"{result['win_rate']:.2f}",
                'Total Trades': result['total_trades'],
                'Final Value ($)': f"{result['final_value']:,.2f}"
            })
        
        return pd.DataFrame(comparison)
