
import pandas as pd
import requests
from io import StringIO
import re

# Common headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

def _scrape_wiki_table_column(url, col_name_variants, value_col_variants=None):
    """Helper to scrape a simple ticker/name column from Wiki."""
    try:
        response = requests.get(url, headers=HEADERS)
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
            
            if found_ticker and found_name:
                df = df.dropna(subset=[found_ticker])
                return dict(zip(df[found_ticker], df[found_name]))
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return {}

# --- Existing Functions ---
def get_sp500_tickers():
    return _scrape_wiki_table_column("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", ["Symbol"], ["Security"]) or {}

def get_nasdaq100_tickers():
    return _scrape_wiki_table_column("https://en.wikipedia.org/wiki/Nasdaq-100", ["Ticker"], ["Company"]) or {}

def get_dow_tickers():
    return _scrape_wiki_table_column("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average", ["Symbol"], ["Company"]) or {}

def get_ftse100_tickers():
    d = _scrape_wiki_table_column("https://en.wikipedia.org/wiki/FTSE_100_Index", ["Ticker"], ["Company"])
    if d:
        return {k + ".L" if not k.endswith(".L") else k: v for k, v in d.items()}
    return {}

def get_dax_tickers():
    d = _scrape_wiki_table_column("https://en.wikipedia.org/wiki/DAX", ["Ticker"], ["Company"])
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
        df = tables[0]
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
    # Top Global Oil & Gas (Proxies due to complex scraping)
    return {
        "XOM": "ExxonMobil", "CVX": "Chevron", "SHEL": "Shell", "TTE": "TotalEnergies",
        "BP": "BP", "COP": "ConocoPhillips", "EOG": "EOG Resources", "SLB": "Schlumberger",
        "MPC": "Marathon Petroleum", "PSX": "Phillips 66", "VLO": "Valero", "OXY": "Occidental",
        "HES": "Hess", "KMI": "Kinder Morgan", "WMB": "Williams", "OKE": "ONEOK",
        "TRP": "TC Energy", "ENB": "Enbridge", "PBR": "Petrobras", "EQNR": "Equinor",
        "CVE": "Cenovus", "SU": "Suncor", "CNQ": "Canadian Natural", "HAL": "Halliburton",
        "BKR": "Baker Hughes", "DVN": "Devon Energy", "FANG": "Diamondback", "CTRA": "Coterra",
        "MRO": "Marathon Oil", "APA": "APA Corp"
    }

def get_gold_tickers():
    # Major Gold Miners
    return {
        "NEM": "Newmont", "GOLD": "Barrick Gold", "AEM": "Agnico Eagle", "WPM": "Wheaton Precious",
        "FNV": "Franco-Nevada", "RGLD": "Royal Gold", "KGC": "Kinross", "AU": "AngloGold Ashanti",
        "GFI": "Gold Fields", "HMY": "Harmony Gold", "NGD": "New Gold", "IAG": "Iamgold",
        "EGO": "Eldorado Gold", "BTG": "B2Gold", "SSRM": "SSR Mining", "CDE": "Coeur Mining",
        "HL": "Hecla Mining"
    }

def get_silver_tickers():
    # Major Silver Miners
    return {
        "PAAS": "Pan American Silver", "HL": "Hecla Mining", "AG": "First Majestic", "CDE": "Coeur Mining",
        "MAG": "MAG Silver", "FSM": "Fortuna Silver", "EXK": "Endeavour Silver", "SVM": "Silvercorp",
        "SILV": "SilverCrest", "GATO": "Gatos Silver"
    }

def get_copper_tickers():
    # Major Copper Producers
    return {
        "FCX": "Freeport-McMoRan", "SCCO": "Southern Copper", "RIO": "Rio Tinto", "BHP": "BHP Group",
        "VALE": "Vale", "TECK": "Teck Resources", "IVN.TO": "Ivanhoe Mines", "HBM": "Hudbay",
        "ERO": "Ero Copper", "FM.TO": "First Quantum"
    }

def get_energy_tickers():
    # Broader Energy (similar to Oil/Gas but includes utilities/renewables)
    d = get_oil_gas_tickers()
    d.update({
        "NEE": "NextEra Energy", "DUK": "Duke Energy", "SO": "Southern Co", "D": "Dominion",
        "FSLR": "First Solar", "ENPH": "Enphase", "SEDG": "SolarEdge", "PLUG": "Plug Power",
        "BE": "Bloom Energy"
    })
    return d

def get_health_tickers():
    # Major Bio/Pharma
    return {
        "LLY": "Eli Lilly", "UNH": "UnitedHealth", "JNJ": "Johnson & Johnson", "MRK": "Merck",
        "ABBV": "AbbVie", "TMO": "Thermo Fisher", "NOVO-B.CO": "Novo Nordisk", "NVS": "Novartis",
        "AZN": "AstraZeneca", "PFE": "Pfizer", "AMGN": "Amgen", "ISRG": "Intuitive Surgical",
        "SYK": "Stryker", "ELV": "Elevance", "MDT": "Medtronic", "CVS": "CVS Health",
        "BMY": "Bristol Myers Squibb", "VRTX": "Vertex", "REGN": "Regeneron", "ZTS": "Zoetis"
    }

def get_defense_tickers():
    # Major Defense
    return {
        "RTX": "RTX Corp", "LMT": "Lockheed Martin", "BA": "Boeing", "GD": "General Dynamics",
        "NOC": "Northrop Grumman", "LHX": "L3Harris", "HII": "Huntington Ingalls", "LDOS": "Leidos",
        "TXT": "Textron", "SAIC": "SAIC", "CACI": "CACI", "KTOS": "Kratos", "AVAV": "AeroVironment",
        "PLTR": "Palantir", "BAESuny.L": "BAE Systems" # Note: UK ticker might need special handling
    }

def get_bank_tickers():
    # Major US/Global Banks
    return {
        "JPM": "JPMorgan Chase", "BAC": "Bank of America", "WFC": "Wells Fargo", "C": "Citigroup",
        "HSBC": "HSBC", "RY": "Royal Bank of Canada", "TD": "Toronto-Dominion", "HDB": "HDFC Bank",
        "MS": "Morgan Stanley", "GS": "Goldman Sachs", "SCHW": "Charles Schwab", "AXP": "American Express",
        "USB": "US Bancorp", "PNC": "PNC Financial", "TFC": "Truist", "BK": "BNY Mellon",
        "STT": "State Street", "COF": "Capital One"
    }

def get_semiconductor_tickers():
    # Major Semis (Processors/GPU often overlap here)
    return {
        "NVDA": "NVIDIA", "TSM": "TSMC", "AVGO": "Broadcom", "AMD": "AMD", "INTC": "Intel",
        "QCOM": "Qualcomm", "TXN": "Texas Instruments", "MU": "Micron", "ADI": "Analog Devices",
        "LRCX": "Lam Research", "AMAT": "Applied Materials", "KLAC": "KLA Corp", "MRVL": "Marvell",
        "MCHP": "Microchip"
    }

def get_processor_tickers():
    # Subset of Semis focused on CPU/Compute
    return {"INTC": "Intel", "AMD": "AMD", "NVDA": "NVIDIA", "ARM": "Arm Holdings", "TSM": "TSMC"}

def get_gpu_tickers():
    # Subset focused on GPU
    return {"NVDA": "NVIDIA", "AMD": "AMD", "INTC": "Intel"}

def get_ai_tickers():
    # AI Proxies (Software + Hardware)
    return {
        "NVDA": "NVIDIA", "MSFT": "Microsoft", "GOOGL": "Alphabet", "META": "Meta", "AMZN": "Amazon",
        "TSLA": "Tesla", "AMD": "AMD", "PLTR": "Palantir", "ADBE": "Adobe", "CRM": "Salesforce",
        "NOW": "ServiceNow", "SNOW": "Snowflake", "ORCL": "Oracle", "IBM": "IBM", "AI": "C3.ai",
        "PATH": "UiPath"
    }

def get_storage_tickers():
    # Data Storage (Hardware + Cloud proxies)
    return {
        "WDC": "Western Digital", "STX": "Seagate", "NTAP": "NetApp", "PSTG": "Pure Storage",
        "DELL": "Dell", "HPE": "HPE", "VRT": "Vertiv", "EQIX": "Equinix", "DLR": "Digital Realty"
    }

def get_memecoins_tickers():
    # Top Memecoins
    return {
        "DOGE-USD": "Dogecoin", "SHIB-USD": "Shiba Inu", "PEPE-USD": "Pepe", "BONK-USD": "Bonk",
        "FLOKI-USD": "Floki", "WIF-USD": "dogwifhat", "BOME-USD": "Book of Meme", 
        "DOGE2-USD": "Dogecoin 2.0", # risky matches, stick to big ones
        "MEME-USD": "Memecoin", "BRETT-USD": "Brett", "MOG-USD": "Mog Coin",
        "POPCAT-USD": "Popcat"
    }
