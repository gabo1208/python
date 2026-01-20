
import pandas as pd
import requests
from io import StringIO
import re

# Common headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

def _scrape_table(url, col_name_variants, value_col_variants=None, limit=None):
    """General helper to scrape a simple ticker/name column from a table."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        tables = pd.read_html(StringIO(response.text))
        for df in tables:
            # Normalize cols
            cols = [c if isinstance(c, str) else str(c) for c in df.columns]
            df.columns = cols
            
            # Find ticker column
            found_ticker = None
            for v in col_name_variants:
                for c in df.columns:
                    if v.lower() in c.lower():
                        found_ticker = c
                        break
                if found_ticker: break
            
            # Find company name column
            found_name = None
            if value_col_variants:
                 for v in value_col_variants:
                    for c in df.columns:
                        if v.lower() in c.lower():
                            found_name = c
                            break
                    if found_name: break
            
            if found_ticker:
                df = df.dropna(subset=[found_ticker])
                # Apply limit if specified
                if limit:
                    df = df.head(limit)
                
                if found_name:
                    return dict(zip(df[found_ticker], df[found_name]))
                else:
                    return dict(zip(df[found_ticker], df[found_ticker]))
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return {}

# --- Existing Functions ---
def get_sp500_tickers():
    return _scrape_table("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", ["Symbol"], ["Security"]) or {}

def get_nasdaq100_tickers():
    return _scrape_table("https://en.wikipedia.org/wiki/Nasdaq-100", ["Ticker"], ["Company"]) or {}

def get_dow_tickers():
    return _scrape_table("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average", ["Symbol"], ["Company"]) or {}

def get_ftse100_tickers():
    d = _scrape_table("https://en.wikipedia.org/wiki/FTSE_100_Index", ["Ticker"], ["Company"])
    if d:
        return {k + ".L" if not k.endswith(".L") else k: v for k, v in d.items()}
    return {}

def get_dax_tickers():
    d = _scrape_table("https://en.wikipedia.org/wiki/DAX", ["Ticker"], ["Company"])
    if d:
        return {k + ".DE" if not k.endswith(".DE") else k: v for k, v in d.items()}
    return {}

def get_top_crypto_tickers(limit=100):
    """Scrapes top cryptos from Yahoo Finance."""
    url = f"https://finance.yahoo.com/crypto?count={limit}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        tables = pd.read_html(StringIO(response.text))
        df = tables[0].copy()
        if 'Symbol' in df.columns and 'Name' in df.columns:
             df = df.dropna(subset=['Symbol'])
             df['Symbol'] = df['Symbol'].astype(str)
             def clean_ticker(t):
                 match = re.search(r'([A-Z0-9]+-USD)', t)
                 if match: return match.group(1)
                 return t
             df['Symbol'] = df['Symbol'].apply(clean_ticker)
             return dict(zip(df['Symbol'], df['Name']))
    except Exception:
        pass
    # Fallback
    return {"BTC-USD": "Bitcoin", "ETH-USD": "Ethereum", "SOL-USD": "Solana"}

# --- New Sectors ---

def get_oil_gas_tickers():
    url = "https://stockanalysis.com/stocks/industry/oil-gas-e-and-p/"
    d = _scrape_table(url, ["Symbol"], ["Company Name"], limit=50)
    if d: return d
    return {"XOM": "ExxonMobil", "CVX": "Chevron", "SHEL": "Shell", "BP": "BP"}

def get_gold_tickers():
    url = "https://stockanalysis.com/stocks/industry/gold/"
    d = _scrape_table(url, ["Symbol"], ["Company Name"], limit=50)
    if d: return d
    return {"NEM": "Newmont", "GOLD": "Barrick Gold", "AEM": "Agnico Eagle"}

def get_silver_tickers():
    url = "https://stockanalysis.com/stocks/industry/silver/"
    d = _scrape_table(url, ["Symbol"], ["Company Name"], limit=50)
    if d: return d
    return {"PAAS": "Pan American Silver", "HL": "Hecla Mining", "AG": "First Majestic"}

def get_copper_tickers():
    url = "https://stockanalysis.com/stocks/industry/copper/"
    d = _scrape_table(url, ["Symbol"], ["Company Name"], limit=50)
    if d: return d
    return {"FCX": "Freeport-McMoRan", "SCCO": "Southern Copper", "RIO": "Rio Tinto"}

def get_energy_tickers():
    url = "https://stockanalysis.com/stocks/sector/energy/"
    d = _scrape_table(url, ["Symbol"], ["Company Name"], limit=50)
    if d: return d
    return {"NEE": "NextEra Energy", "DUK": "Duke Energy", "FSLR": "First Solar"}

def get_health_tickers():
    url = "https://stockanalysis.com/stocks/sector/healthcare/"
    d = _scrape_table(url, ["Symbol"], ["Company Name"], limit=50)
    if d: return d
    return {"LLY": "Eli Lilly", "UNH": "UnitedHealth", "JNJ": "Johnson & Johnson"}

def get_defense_tickers():
    url = "https://stockanalysis.com/stocks/industry/aerospace-and-defense/"
    d = _scrape_table(url, ["Symbol"], ["Company Name"], limit=50)
    if d: return d
    return {"RTX": "RTX Corp", "LMT": "Lockheed Martin", "BA": "Boeing"}

def get_bank_tickers():
    url = "https://stockanalysis.com/stocks/industry/banks-regional/"
    d = _scrape_table(url, ["Symbol"], ["Company Name"], limit=50)
    if d: return d
    return {"JPM": "JPMorgan Chase", "BAC": "Bank of America", "WFC": "Wells Fargo"}

def get_semiconductor_tickers():
    url = "https://stockanalysis.com/stocks/industry/semiconductors/"
    d = _scrape_table(url, ["Symbol"], ["Company Name"], limit=50)
    if d: return d
    return {"NVDA": "NVIDIA", "TSM": "TSMC", "AVGO": "Broadcom", "AMD": "AMD"}

def get_processor_tickers():
    return {"INTC": "Intel", "AMD": "AMD", "NVDA": "NVIDIA", "ARM": "Arm Holdings", "TSM": "TSMC"}

def get_gpu_tickers():
    return {"NVDA": "NVIDIA", "AMD": "AMD", "INTC": "Intel"}

def get_ai_tickers():
    url = "https://stockanalysis.com/list/ai-stocks/"
    d = _scrape_table(url, ["Symbol"], ["Company Name"], limit=50)
    if d: return d
    return {"NVDA": "NVIDIA", "MSFT": "Microsoft", "GOOGL": "Alphabet", "PLTR": "Palantir"}

def get_storage_tickers():
    url = "https://stockanalysis.com/stocks/industry/computer-hardware/"
    d = _scrape_table(url, ["Symbol"], ["Company Name"], limit=50)
    if d: return d
    return {"WDC": "Western Digital", "STX": "Seagate", "NTAP": "NetApp", "PSTG": "Pure Storage"}

def get_memecoins_tickers():
    url = "https://coinmarketcap.com/view/memes/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        tables = pd.read_html(StringIO(response.text))
        for df in tables:
            # CMC usually has Name and Symbol in columns
            if 'Name' in df.columns and 'Symbol' in df.columns:
                 # Apply limit to CMC too
                 df = df.head(50)
                 # Clean symbols (CMC often adds rank or logo info in scrapes)
                 df['Symbol'] = df['Symbol'].astype(str).str.split().str[0]
                 # Add -USD for yfinance
                 return {f"{s}-USD": n for s, n in zip(df['Symbol'], df['Name'])}
    except Exception:
        pass
    return {"DOGE-USD": "Dogecoin", "SHIB-USD": "Shiba Inu", "PEPE-USD": "Pepe"}
