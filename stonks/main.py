import yfinance as yf
import pandas as pd
from tabulate import tabulate
import sys
import get_tickers as gt

def analyze_and_print(ticker_dict, title):
    """
    Downloads data for tickers in ticker_dict, calculates trends, 
    and prints top gainers/losers with company names.
    ticker_dict: {ticker_symbol: company_name}
    """
    if not ticker_dict:
        print(f"\n⚠️  No tickers found for {title}. Skipping...")
        return

    tickers = list(ticker_dict.keys())
    print(f"\n⏳ Fetching data for {len(tickers)} symbols ({title})...")
    
    try:
        # Download 5 days of data
        # suppress_errors=True to keep output clean, threads=True for speed
        data = yf.download(tickers, period="5d", progress=True, threads=True)
    except Exception as e:
        print(f"Error downloading data for {title}: {e}")
        return

    if data.empty:
        print(f"No data downloaded for {title}.")
        return

    # Extract Close prices
    # Handle MultiIndex handling robustly
    if isinstance(data.columns, pd.MultiIndex):
        try:
             closes = data['Close']
        except KeyError:
             if 'Adj Close' in data:
                 closes = data['Adj Close']
             else:
                 # fallback to level 0
                 closes = data.xs(data.columns.levels[0][0], axis=1, level=0)
    else:
        # If single level columns, it's either just tickers (if only Close returned?) 
        # or just Close (if single ticker). 
        # But yf.download(list) usually returns MultiIndex or (Price, Ticker) structure unless 1 ticker.
        # If 1 ticker, it returns DataFrame with columns Open, High, etc.
        if 'Close' in data.columns:
            closes = data['Close']
        else:
            closes = data # Should not happen usually with multiple tickers

    # Ensure closes is a DataFrame
    if isinstance(closes, pd.Series):
        closes = closes.to_frame()

    # Calculate percentage change
    pct_change = closes.pct_change()
    
    if pct_change.shape[0] < 2:
         print(f"Not enough history for {title}.")
         return
         
    latest_trends = pct_change.iloc[-1]
    
    # Handle blank latest row
    if latest_trends.isna().all():
        if pct_change.shape[0] > 2:
            latest_trends = pct_change.iloc[-2]
        else:
            print(f"No valid trend data for {title}.")
            return

    # Drop NaNs
    latest_trends = latest_trends.dropna()
    
    if latest_trends.empty:
         print(f"No valid data after cleaning for {title}.")
         return

    # Sort
    top_gainers = latest_trends.nlargest(10)
    top_losers = latest_trends.nsmallest(10)
    
    # Get prices
    latest_prices = closes.loc[latest_trends.name]

    print("\n" + "="*50)
    print(f"📈 {title.upper()}")
    print("="*50)
    
    print("\n🚀 TOP 10 GAINERS")
    print_table(top_gainers, ticker_dict, latest_prices)

    print("\n📉 TOP 10 LOSERS")
    print_table(top_losers, ticker_dict, latest_prices)

def print_table(series, ticker_dict, prices):
    table_data = []
    for ticker, change in series.items():
        # Clean ticker for lookup if needed (sometimes yf modifies it?)
        # yf usually returns same ticker.
        name = ticker_dict.get(ticker, "Unknown Company")
        price = prices[ticker] if ticker in prices else 0.0
        
        change_str = f"{change*100:+.2f}%"
        table_data.append([ticker, name, f"${price:,.2f}", change_str])
    
    print(tabulate(table_data, headers=["Ticker", "Company", "Price", "Change"], tablefmt="fancy_grid"))

def main():
    print("🚀 STARTING MARKET ANALYSIS...")

    # 1. S&P 500
    sp500 = gt.get_sp500_tickers()
    analyze_and_print(sp500, "S&P 500 (US Large Cap)")

    # 2. NASDAQ 100
    nasdaq = gt.get_nasdaq100_tickers()
    analyze_and_print(nasdaq, "NASDAQ 100 (Tech Growth)")

    # 3. Dow Jones
    dow = gt.get_dow_tickers()
    analyze_and_print(dow, "Dow Jones Industrial Average")

    # 4. FTSE 100
    ftse = gt.get_ftse100_tickers()
    analyze_and_print(ftse, "FTSE 100 (UK)")

    # 5. DAX
    dax = gt.get_dax_tickers()
    analyze_and_print(dax, "DAX (Germany)")

    # 6. Crypto
    crypto = gt.get_top_crypto_tickers()
    analyze_and_print(crypto, "Top 20 Cryptocurrencies")

    print("\n✅ ANALYSIS COMPLETE.")

if __name__ == "__main__":
    main()
