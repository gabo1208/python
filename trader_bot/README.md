# Trading Bot 🤖📈

A toy trading bot project that demonstrates algorithmic trading concepts with multiple strategies, backtesting capabilities, and performance visualization.

## Features

- **Multiple Trading Strategies**
  - Moving Average Crossover
  - RSI (Relative Strength Index)
  - Momentum-based trading

- **Backtesting Engine** - Test strategies on historical data
- **Portfolio Management** - Track positions, cash, and returns
- **Performance Metrics** - Sharpe ratio, max drawdown, win rate, and more
- **Interactive Visualizations** - Beautiful charts with Plotly
- **Simulated Trading** - Realistic slippage and commission costs

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Run a Single Backtest

```bash
python main.py backtest --strategy ma --symbol AAPL --start 2023-01-01 --end 2024-01-01 --plot
```

### Compare All Strategies

```bash
python main.py compare --symbols AAPL MSFT GOOGL --start 2023-01-01 --end 2024-01-01 --plot
```

### Generate Detailed Report

```bash
python main.py report --strategy rsi --symbol TSLA --start 2023-01-01 --end 2024-01-01
```

## Trading Strategies

### Moving Average Crossover (`ma`)
- **Buy Signal**: Short MA crosses above long MA
- **Sell Signal**: Short MA crosses below long MA
- **Parameters**: Short window (20), Long window (50)

### RSI Strategy (`rsi`)
- **Buy Signal**: RSI < 30 (oversold)
- **Sell Signal**: RSI > 70 (overbought)
- **Parameters**: Period (14), Oversold (30), Overbought (70)

### Momentum Strategy (`momentum`)
- **Buy Signal**: Strong positive momentum (> 2%)
- **Sell Signal**: Momentum weakens or turns negative
- **Parameters**: Lookback period (20), Threshold (2%)

## Configuration

Edit `config.py` to customize:
- Initial capital
- Commission rates
- Slippage
- Risk management parameters
- Strategy parameters

## Performance Metrics

The bot calculates comprehensive metrics:
- **Total Return** - Overall profit/loss percentage
- **Sharpe Ratio** - Risk-adjusted returns
- **Sortino Ratio** - Downside risk-adjusted returns
- **Calmar Ratio** - Return vs. max drawdown
- **Maximum Drawdown** - Largest peak-to-trough decline
- **Win Rate** - Percentage of profitable trades
- **Profit Factor** - Average win / average loss

## Project Structure

```
trader_bot/
├── main.py                 # CLI interface
├── config.py              # Configuration settings
├── portfolio.py           # Portfolio management
├── order_executor.py      # Order execution with slippage
├── backtester.py          # Backtesting engine
├── data_fetcher.py        # Market data fetching
├── indicators.py          # Technical indicators
├── performance_tracker.py # Performance metrics
├── visualizer.py          # Visualization tools
├── strategies/
│   ├── base_strategy.py   # Base strategy class
│   ├── moving_average.py  # MA crossover strategy
│   ├── rsi_strategy.py    # RSI strategy
│   └── momentum.py        # Momentum strategy
└── requirements.txt       # Dependencies
```

## Example Output

```
============================================================
BACKTEST RESULTS
============================================================
Strategy:          Moving Average Crossover(short_window=20, long_window=50)
Symbol:            AAPL
Initial Capital:   $100,000.00
Final Value:       $115,234.56
Total Return:      15.23%
Buy & Hold Return: 12.45%
Sharpe Ratio:      1.45
Max Drawdown:      -8.32%
Total Trades:      24
Win Rate:          58.33%
============================================================
```

## Visualizations

The bot generates interactive HTML dashboards with:
- Portfolio equity curve
- Price chart with buy/sell signals
- Drawdown chart
- Strategy comparison charts

## Disclaimer

⚠️ **This is a toy project for educational purposes only!**

- No real money is involved
- Past performance does not guarantee future results
- Do not use this for actual trading without proper testing and risk management
- Always consult with financial professionals before making investment decisions

## License

MIT License - Feel free to use and modify for learning purposes!

## Contributing

This is a toy project, but suggestions and improvements are welcome!

---

**Happy Trading! 📊🚀**
