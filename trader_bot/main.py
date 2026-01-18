"""
Main CLI interface for the trading bot.
"""
import argparse
from datetime import datetime, timedelta
from backtester import Backtester
from strategies import MovingAverageStrategy, RSIStrategy, MomentumStrategy
from data_fetcher import DataFetcher
from visualizer import Visualizer
from performance_tracker import PerformanceTracker
from config import Config


def get_strategy(strategy_name: str):
    """Get strategy instance by name."""
    config = Config()
    
    strategies = {
        'ma': MovingAverageStrategy(
            short_window=config.STRATEGY_PARAMS['moving_average']['short_window'],
            long_window=config.STRATEGY_PARAMS['moving_average']['long_window']
        ),
        'rsi': RSIStrategy(
            period=config.STRATEGY_PARAMS['rsi']['period'],
            oversold=config.STRATEGY_PARAMS['rsi']['oversold'],
            overbought=config.STRATEGY_PARAMS['rsi']['overbought']
        ),
        'momentum': MomentumStrategy(
            lookback_period=config.STRATEGY_PARAMS['momentum']['lookback_period'],
            threshold=config.STRATEGY_PARAMS['momentum']['threshold']
        )
    }
    
    return strategies.get(strategy_name.lower())


def backtest_command(args):
    """Run a single backtest."""
    strategy = get_strategy(args.strategy)
    
    if strategy is None:
        print(f"Unknown strategy: {args.strategy}")
        print("Available strategies: ma, rsi, momentum")
        return
    
    config = Config()
    backtester = Backtester(strategy, args.capital, config)
    data_fetcher = DataFetcher(config.DATA_CACHE_DIR)
    
    # Run backtest
    results = backtester.run(args.symbol, args.start, args.end, data_fetcher)
    
    # Print results
    backtester.print_results()
    
    # Create visualizations
    if args.plot:
        data = data_fetcher.get_historical_data(args.symbol, args.start, args.end)
        output_file = f"backtest_{args.strategy}_{args.symbol}.html"
        Visualizer.create_dashboard(results, data, output_file)


def compare_command(args):
    """Compare multiple strategies."""
    config = Config()
    data_fetcher = DataFetcher(config.DATA_CACHE_DIR)
    
    strategies = {
        'ma': MovingAverageStrategy(
            short_window=config.STRATEGY_PARAMS['moving_average']['short_window'],
            long_window=config.STRATEGY_PARAMS['moving_average']['long_window']
        ),
        'rsi': RSIStrategy(
            period=config.STRATEGY_PARAMS['rsi']['period'],
            oversold=config.STRATEGY_PARAMS['rsi']['oversold'],
            overbought=config.STRATEGY_PARAMS['rsi']['overbought']
        ),
        'momentum': MomentumStrategy(
            lookback_period=config.STRATEGY_PARAMS['momentum']['lookback_period'],
            threshold=config.STRATEGY_PARAMS['momentum']['threshold']
        )
    }
    
    all_results = []
    
    # Run backtests for each strategy and symbol
    for strategy_name, strategy in strategies.items():
        for symbol in args.symbols:
            print(f"\n{'='*60}")
            print(f"Testing {strategy_name.upper()} on {symbol}")
            print(f"{'='*60}")
            
            backtester = Backtester(strategy, args.capital, config)
            results = backtester.run(symbol, args.start, args.end, data_fetcher)
            all_results.append(results)
            backtester.print_results()
    
    # Create comparison table
    print("\n" + "="*80)
    print("STRATEGY COMPARISON")
    print("="*80)
    comparison_df = PerformanceTracker.compare_strategies(all_results)
    print(comparison_df.to_string(index=False))
    print("="*80 + "\n")
    
    # Create comparison chart
    if args.plot:
        output_file = "strategy_comparison.html"
        Visualizer.plot_strategy_comparison(all_results, output_file)


def report_command(args):
    """Generate detailed report for a strategy."""
    strategy = get_strategy(args.strategy)
    
    if strategy is None:
        print(f"Unknown strategy: {args.strategy}")
        return
    
    config = Config()
    backtester = Backtester(strategy, args.capital, config)
    data_fetcher = DataFetcher(config.DATA_CACHE_DIR)
    
    # Run backtest
    results = backtester.run(args.symbol, args.start, args.end, data_fetcher)
    
    # Print results
    backtester.print_results()
    
    # Calculate detailed metrics
    equity_curve = results['equity_curve']
    trade_history = results['trade_history']
    metrics = PerformanceTracker.calculate_metrics(
        equity_curve, trade_history, args.capital
    )
    
    print("\nDETAILED METRICS:")
    print(f"{'='*60}")
    print(f"Annualized Return:  {metrics['annualized_return']:.2f}%")
    print(f"Volatility:         {metrics['volatility']:.2f}%")
    print(f"Sharpe Ratio:       {metrics['sharpe_ratio']:.2f}")
    print(f"Sortino Ratio:      {metrics['sortino_ratio']:.2f}")
    print(f"Calmar Ratio:       {metrics['calmar_ratio']:.2f}")
    print(f"Profit Factor:      {metrics['profit_factor']:.2f}")
    print(f"Winning Trades:     {metrics['winning_trades']}")
    print(f"Losing Trades:      {metrics['losing_trades']}")
    print(f"Average Win:        ${metrics['avg_win']:.2f}")
    print(f"Average Loss:       ${metrics['avg_loss']:.2f}")
    print(f"{'='*60}\n")
    
    # Create dashboard
    data = data_fetcher.get_historical_data(args.symbol, args.start, args.end)
    output_file = f"report_{args.strategy}_{args.symbol}.html"
    Visualizer.create_dashboard(results, data, output_file)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Trading Bot - Backtest and compare trading strategies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run backtest on a single strategy
  python main.py backtest --strategy ma --symbol AAPL --start 2023-01-01 --end 2024-01-01
  
  # Compare all strategies on multiple symbols
  python main.py compare --symbols AAPL MSFT GOOGL --start 2023-01-01 --end 2024-01-01
  
  # Generate detailed report
  python main.py report --strategy rsi --symbol TSLA --start 2023-01-01 --end 2024-01-01
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Backtest command
    backtest_parser = subparsers.add_parser('backtest', help='Run a single backtest')
    backtest_parser.add_argument('--strategy', required=True, choices=['ma', 'rsi', 'momentum'],
                                help='Trading strategy (ma=Moving Average, rsi=RSI, momentum=Momentum)')
    backtest_parser.add_argument('--symbol', required=True, help='Stock symbol (e.g., AAPL)')
    backtest_parser.add_argument('--start', required=True, help='Start date (YYYY-MM-DD)')
    backtest_parser.add_argument('--end', required=True, help='End date (YYYY-MM-DD)')
    backtest_parser.add_argument('--capital', type=float, default=100000, help='Initial capital (default: 100000)')
    backtest_parser.add_argument('--plot', action='store_true', help='Generate visualization')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare multiple strategies')
    compare_parser.add_argument('--symbols', nargs='+', required=True, help='Stock symbols to test')
    compare_parser.add_argument('--start', required=True, help='Start date (YYYY-MM-DD)')
    compare_parser.add_argument('--end', required=True, help='End date (YYYY-MM-DD)')
    compare_parser.add_argument('--capital', type=float, default=100000, help='Initial capital (default: 100000)')
    compare_parser.add_argument('--plot', action='store_true', help='Generate comparison chart')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate detailed report')
    report_parser.add_argument('--strategy', required=True, choices=['ma', 'rsi', 'momentum'],
                              help='Trading strategy')
    report_parser.add_argument('--symbol', required=True, help='Stock symbol')
    report_parser.add_argument('--start', required=True, help='Start date (YYYY-MM-DD)')
    report_parser.add_argument('--end', required=True, help='End date (YYYY-MM-DD)')
    report_parser.add_argument('--capital', type=float, default=100000, help='Initial capital (default: 100000)')
    
    args = parser.parse_args()
    
    if args.command == 'backtest':
        backtest_command(args)
    elif args.command == 'compare':
        compare_command(args)
    elif args.command == 'report':
        report_command(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
