# Stonks Market Analysis 📊🚀

A comprehensive market analysis tool that tracks and visualizes performance across multiple global indices, sectors, and cryptocurrencies. Generates beautiful interactive HTML reports with real-time data.

## Features

- **Global Market Coverage**
  - 🇺🇸 S&P 500 (US Large Cap)
  - 💻 NASDAQ 100 (Tech Growth)
  - 📈 Dow Jones Industrial Average
  - 🇬🇧 FTSE 100 (UK)
  - 🇩🇪 DAX (Germany)

- **Sector Analysis**
  - ⛽ Oil & Gas
  - 🥇 Gold Miners
  - 🥈 Silver Miners
  - 🔶 Copper Miners
  - ⚡ Energy & Renewables
  - 🏥 Healthcare & Biomedical
  - 🛡️ Defense Contractors
  - 🏦 Major Banks

- **Technology Sectors**
  - 🔬 Semiconductors
  - 🖥️ Processors (CPU)
  - 🎮 GPUs
  - 🤖 Artificial Intelligence
  - 💾 Data Storage

- **Cryptocurrencies**
  - 💰 Top 100 Cryptocurrencies
  - 🐕 Memecoins

- **Interactive HTML Reports**
  - Sortable tables
  - Real-time performance metrics
  - Best/worst performers
  - Gainers vs losers statistics
  - Beautiful, responsive design

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Generate Interactive HTML Report

The recommended way to use this tool:

```bash
python create_report.py
```

This will:
1. Fetch data for all categories
2. Calculate performance metrics
3. Generate `market_report.html`
4. Print a summary to console

Then open the report in your browser:
```bash
open market_report.html
```

### Console-Only Analysis

For a quick terminal-based view:

```bash
python main.py
```

This displays top 10 gainers and losers for each category in formatted tables.

### Custom Analysis

You can also use the modules programmatically:

```python
import analyze_market

# Get all market trends
results = analyze_market.get_market_trends()

# Access specific category
sp500_data = results['sp500']
print(f"Best performer: {sp500_data['data'][0]['ticker']}")
```

## Output Examples

### Console Output (main.py)

```
🚀 STARTING MARKET ANALYSIS...

⏳ Fetching data for 503 symbols (S&P 500 (US Large Cap))...

==================================================
📈 S&P 500 (US LARGE CAP)
==================================================

🚀 TOP 10 GAINERS
╒══════════╤═══════════════════════════╤══════════╤══════════╕
│ Ticker   │ Company                   │ Price    │ Change   │
╞══════════╪═══════════════════════════╪══════════╪══════════╡
│ NVDA     │ NVIDIA Corporation        │ $875.28  │ +5.23%   │
│ TSLA     │ Tesla, Inc.               │ $248.42  │ +4.89%   │
│ AMD      │ Advanced Micro Devices    │ $142.18  │ +3.67%   │
╘══════════╧═══════════════════════════╧══════════╧══════════╛
```

### HTML Report Features

- **Tabbed Interface**: Switch between categories
- **Sortable Columns**: Click headers to sort
- **Performance Cards**: Quick stats at a glance
- **Color Coding**: Green for gains, red for losses
- **Responsive Design**: Works on mobile and desktop

## Project Structure

```
stonks/
├── main.py              # Console-based analysis
├── analyze_market.py    # Core data fetching and analysis
├── create_report.py     # HTML report generator
├── get_tickers.py       # Ticker symbol fetchers for all categories
├── requirements.txt     # Python dependencies
└── market_report.html   # Generated report (after running)
```

## How It Works

1. **Data Fetching** (`get_tickers.py`)
   - Fetches ticker symbols for each category
   - Uses web scraping and curated lists
   - Returns dictionaries of {ticker: company_name}

2. **Market Analysis** (`analyze_market.py`)
   - Downloads 5-day historical data using yfinance
   - Calculates percentage changes
   - Sorts by performance
   - Returns structured data for all categories

3. **Report Generation** (`create_report.py`)
   - Takes analyzed data
   - Generates interactive HTML with embedded JavaScript
   - Creates sortable tables and statistics cards
   - Saves to `market_report.html`

## Data Sources

- **Stock Data**: Yahoo Finance (via yfinance)
- **Ticker Lists**: 
  - Wikipedia (S&P 500, NASDAQ 100, etc.)
  - Curated lists for sectors
  - get_all_tickers library for crypto

## Performance Metrics

For each category, the tool calculates:
- **Total Analyzed**: Number of symbols tracked
- **Gainers**: Stocks with positive returns
- **Losers**: Stocks with negative returns
- **Best Performance**: Top gainer with percentage
- **Worst Performance**: Biggest loser with percentage

## Customization

### Add New Categories

Edit `analyze_market.py` and add to the `categories` list:

```python
categories = [
    # ... existing categories ...
    ("your_key", "Your Category Name", gt.get_your_tickers),
]
```

Then implement the ticker fetcher in `get_tickers.py`:

```python
def get_your_tickers():
    return {
        "TICK": "Company Name",
        # ... more tickers
    }
```

### Change Time Period

In `analyze_market.py`, modify the download period:

```python
data = yf.download(tickers, period="1mo", ...)  # 1 month instead of 5 days
```

Options: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `max`

### Modify Report Styling

Edit the CSS in `create_report.py` to customize colors, fonts, and layout.

## Tips

- **First Run**: May take a few minutes to download all data
- **Caching**: yfinance caches data, subsequent runs are faster
- **Rate Limits**: If you get errors, add delays between requests
- **Missing Data**: Some tickers may not have recent data (delisted, etc.)

## Troubleshooting

**Error: "No data found"**
- Check your internet connection
- Verify ticker symbols are valid
- Some markets may be closed

**Slow Performance**
- Reduce the number of categories
- Use shorter time periods
- Check network speed

**Import Errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Use Python 3.8 or higher

## Example Use Cases

1. **Daily Market Check**: Run `create_report.py` each morning to see overnight changes
2. **Sector Rotation**: Identify which sectors are gaining/losing momentum
3. **Stock Screening**: Find top performers in specific categories
4. **Portfolio Monitoring**: Track your holdings across different sectors
5. **Research**: Compare performance across global markets

## Disclaimer

⚠️ **For informational purposes only!**

- This tool provides historical data analysis
- Not financial advice
- Past performance does not guarantee future results
- Always do your own research before investing
- Consult with financial professionals for investment decisions

## Contributing

Feel free to:
- Add new market categories
- Improve ticker fetching logic
- Enhance the HTML report design
- Add new metrics and visualizations

## License

MIT License - Free to use and modify!

---

**Made with 📊 and ☕**

*Track the markets, find the stonks!* 🚀
