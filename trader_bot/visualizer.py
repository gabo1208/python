"""
Visualization tools for trading bot results.
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List
from pathlib import Path


class Visualizer:
    """Creates interactive visualizations of trading results."""
    
    @staticmethod
    def plot_equity_curve(results: Dict, output_file: str = None) -> go.Figure:
        """
        Plot portfolio equity curve.
        
        Args:
            results: Backtest results dictionary
            output_file: Optional file path to save HTML
            
        Returns:
            Plotly figure
        """
        equity_curve = results['equity_curve']
        
        fig = go.Figure()
        
        # Portfolio value
        fig.add_trace(go.Scatter(
            x=equity_curve['date'],
            y=equity_curve['value'],
            mode='lines',
            name='Portfolio Value',
            line=dict(color='#00D9FF', width=2)
        ))
        
        # Initial capital line
        fig.add_hline(
            y=results['initial_capital'],
            line_dash="dash",
            line_color="gray",
            annotation_text="Initial Capital"
        )
        
        fig.update_layout(
            title=f"Portfolio Performance - {results['strategy']}",
            xaxis_title="Date",
            yaxis_title="Portfolio Value ($)",
            template="plotly_dark",
            hovermode='x unified',
            height=500
        )
        
        if output_file:
            fig.write_html(output_file)
        
        return fig
    
    @staticmethod
    def plot_trades(results: Dict, data: pd.DataFrame, output_file: str = None) -> go.Figure:
        """
        Plot price chart with buy/sell signals.
        
        Args:
            results: Backtest results dictionary
            data: Historical price data
            output_file: Optional file path to save HTML
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        # Price line
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name='Price',
            line=dict(color='lightblue', width=1)
        ))
        
        # Buy signals
        buy_trades = [t for t in results['trade_history'] if t['action'] == 'BUY']
        if buy_trades:
            buy_dates = [t['date'] for t in buy_trades]
            buy_prices = [t['price'] for t in buy_trades]
            
            fig.add_trace(go.Scatter(
                x=buy_dates,
                y=buy_prices,
                mode='markers',
                name='Buy',
                marker=dict(color='green', size=10, symbol='triangle-up')
            ))
        
        # Sell signals
        sell_trades = [t for t in results['trade_history'] if t['action'] == 'SELL']
        if sell_trades:
            sell_dates = [t['date'] for t in sell_trades]
            sell_prices = [t['price'] for t in sell_trades]
            
            fig.add_trace(go.Scatter(
                x=sell_dates,
                y=sell_prices,
                mode='markers',
                name='Sell',
                marker=dict(color='red', size=10, symbol='triangle-down')
            ))
        
        fig.update_layout(
            title=f"Trading Signals - {results['symbol']}",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_dark",
            hovermode='x unified',
            height=500
        )
        
        if output_file:
            fig.write_html(output_file)
        
        return fig
    
    @staticmethod
    def plot_drawdown(results: Dict, output_file: str = None) -> go.Figure:
        """
        Plot drawdown chart.
        
        Args:
            results: Backtest results dictionary
            output_file: Optional file path to save HTML
            
        Returns:
            Plotly figure
        """
        equity_curve = results['equity_curve']
        
        # Calculate drawdown
        cumulative = (1 + equity_curve['returns']).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max * 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=equity_curve['date'],
            y=drawdown,
            mode='lines',
            name='Drawdown',
            fill='tozeroy',
            line=dict(color='red', width=1)
        ))
        
        fig.update_layout(
            title="Drawdown Over Time",
            xaxis_title="Date",
            yaxis_title="Drawdown (%)",
            template="plotly_dark",
            hovermode='x unified',
            height=400
        )
        
        if output_file:
            fig.write_html(output_file)
        
        return fig
    
    @staticmethod
    def create_dashboard(results: Dict, data: pd.DataFrame, output_file: str = "dashboard.html"):
        """
        Create comprehensive dashboard with all visualizations.
        
        Args:
            results: Backtest results dictionary
            data: Historical price data
            output_file: File path to save HTML dashboard
        """
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(
                f"Portfolio Performance - {results['strategy']}",
                f"Trading Signals - {results['symbol']}",
                "Drawdown"
            ),
            vertical_spacing=0.1,
            row_heights=[0.4, 0.4, 0.2]
        )
        
        equity_curve = results['equity_curve']
        
        # Equity curve
        fig.add_trace(
            go.Scatter(
                x=equity_curve['date'],
                y=equity_curve['value'],
                mode='lines',
                name='Portfolio Value',
                line=dict(color='#00D9FF', width=2)
            ),
            row=1, col=1
        )
        
        # Price with signals
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name='Price',
                line=dict(color='lightblue', width=1)
            ),
            row=2, col=1
        )
        
        # Buy signals
        buy_trades = [t for t in results['trade_history'] if t['action'] == 'BUY']
        if buy_trades:
            fig.add_trace(
                go.Scatter(
                    x=[t['date'] for t in buy_trades],
                    y=[t['price'] for t in buy_trades],
                    mode='markers',
                    name='Buy',
                    marker=dict(color='green', size=10, symbol='triangle-up')
                ),
                row=2, col=1
            )
        
        # Sell signals
        sell_trades = [t for t in results['trade_history'] if t['action'] == 'SELL']
        if sell_trades:
            fig.add_trace(
                go.Scatter(
                    x=[t['date'] for t in sell_trades],
                    y=[t['price'] for t in sell_trades],
                    mode='markers',
                    name='Sell',
                    marker=dict(color='red', size=10, symbol='triangle-down')
                ),
                row=2, col=1
            )
        
        # Drawdown
        cumulative = (1 + equity_curve['returns']).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max * 100
        
        fig.add_trace(
            go.Scatter(
                x=equity_curve['date'],
                y=drawdown,
                mode='lines',
                name='Drawdown',
                fill='tozeroy',
                line=dict(color='red', width=1)
            ),
            row=3, col=1
        )
        
        # Update layout
        fig.update_xaxes(title_text="Date", row=3, col=1)
        fig.update_yaxes(title_text="Value ($)", row=1, col=1)
        fig.update_yaxes(title_text="Price ($)", row=2, col=1)
        fig.update_yaxes(title_text="Drawdown (%)", row=3, col=1)
        
        fig.update_layout(
            template="plotly_dark",
            height=1200,
            showlegend=True,
            hovermode='x unified'
        )
        
        fig.write_html(output_file)
        print(f"\nDashboard saved to: {output_file}")
        
        return fig
    
    @staticmethod
    def plot_strategy_comparison(results_list: List[Dict], output_file: str = None) -> go.Figure:
        """
        Compare multiple strategies on the same chart.
        
        Args:
            results_list: List of backtest result dictionaries
            output_file: Optional file path to save HTML
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        for results in results_list:
            equity_curve = results['equity_curve']
            
            # Normalize to percentage returns
            initial_value = equity_curve['value'].iloc[0]
            normalized_values = (equity_curve['value'] / initial_value - 1) * 100
            
            fig.add_trace(go.Scatter(
                x=equity_curve['date'],
                y=normalized_values,
                mode='lines',
                name=results['strategy'],
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title="Strategy Comparison (Normalized Returns)",
            xaxis_title="Date",
            yaxis_title="Return (%)",
            template="plotly_dark",
            hovermode='x unified',
            height=600
        )
        
        if output_file:
            fig.write_html(output_file)
        
        return fig
