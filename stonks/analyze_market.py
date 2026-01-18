
import yfinance as yf
import pandas as pd
import get_tickers as gt

def get_market_trends():
    """
    Fetches tickers for all categories, downloads data, and calculates trends.
    Returns a dictionary of structure:
    {
        "category_key": {
            "title": "Display Title",
            "data": [ ... sorted list ... ],
            "best": { ... },
            "worst": { ... }
        },
        ...
    }
    """
    results = {}
    
    # categories: key, title, function
    categories = [
        ("sp500", "S&P 500", gt.get_sp500_tickers),
        ("nasdaq100", "NASDAQ 100", gt.get_nasdaq100_tickers),
        ("dow", "Dow Jones", gt.get_dow_tickers),
        ("ftse100", "FTSE 100", gt.get_ftse100_tickers),
        ("dax", "DAX", gt.get_dax_tickers),
        ("crypto", "Top 100 Cryptos", gt.get_top_crypto_tickers),
        
        # New Sectors
        ("oil_gas", "Oil & Gas (Top)", gt.get_oil_gas_tickers),
        ("gold", "Gold Miners", gt.get_gold_tickers),
        ("silver", "Silver Miners", gt.get_silver_tickers),
        ("copper", "Copper Miners", gt.get_copper_tickers),
        ("energy", "Energy & Renewables", gt.get_energy_tickers),
        ("health", "Healthcare (Biomed)", gt.get_health_tickers),
        ("defense", "Defense Contractors", gt.get_defense_tickers),
        ("banks", "Major Banks", gt.get_bank_tickers),
        ("semis", "Semiconductors", gt.get_semiconductor_tickers),
        ("processors", "Processors (CPU)", gt.get_processor_tickers),
        ("gpu", "GPUs", gt.get_gpu_tickers),
        ("ai", "Artificial Intelligence", gt.get_ai_tickers),
        ("storage", "Data Storage", gt.get_storage_tickers),
        ("memecoins", "Memecoins", gt.get_memecoins_tickers),
    ]

    for key, title, func in categories:
        print(f"Fetching {title}...")
        try:
            ticker_dict = func()
        except Exception as e:
            print(f"Error calling ticker func for {title}: {e}")
            ticker_dict = {}

        if not ticker_dict:
            results[key] = {"title": title, "data": []}
            continue

        tickers = list(ticker_dict.keys())
        
        # Download data
        try:
            data = yf.download(tickers, period="5d", progress=False, threads=True)
        except Exception as e:
            print(f"Failed to download {title}: {e}")
            results[key] = {"title": title, "data": []}
            continue

        if data.empty:
            results[key] = {"title": title, "data": []}
            continue

        # Extract closes
        if isinstance(data.columns, pd.MultiIndex):
            try:
                closes = data['Close']
            except KeyError:
                if 'Adj Close' in data:
                    closes = data['Adj Close']
                else:
                    closes = data.xs(data.columns.levels[0][0], axis=1, level=0)
        else:
            if 'Close' in data.columns:
                closes = data['Close']
            else:
                closes = data

        if isinstance(closes, pd.Series):
            closes = closes.to_frame()

        pct_change = closes.pct_change()
        
        # Get latest valid row
        if pct_change.shape[0] < 2:
             # Just use what we have if 1 row? No cant calculate change.
             latest_trends = pd.Series()
        else:
            latest_trends = pct_change.iloc[-1]
            if latest_trends.isna().all() and pct_change.shape[0] > 1:
                latest_trends = pct_change.iloc[-2]

        latest_trends = latest_trends.dropna()
        
        latest_prices = closes.loc[latest_trends.name]

        # Build list
        category_data = []
        for ticker, change in latest_trends.items():
            name = ticker_dict.get(ticker, ticker)
            
            # Get price
            price = latest_prices[ticker] if ticker in latest_prices else 0.0
            
            category_data.append({
                "ticker": ticker,
                "name": name,
                "price": price,
                "price_str": f"{price:,.2f}",
                "change": change,
                "change_str": f"{change*100:+.2f}%"
            })
        
        # Sort by best change descending
        category_data.sort(key=lambda x: x['change'], reverse=True)
        
        results[key] = {"title": title, "data": category_data}
    
    return results
