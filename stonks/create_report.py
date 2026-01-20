
import analyze_market
import json
import os
import datetime

def generate_html(results):
    # Create investment recommendations by aggregating all stocks
    all_stocks = []
    for key, category in results.items():
        for stock in category['data']:
            # Add category info to each stock
            stock_copy = stock.copy()
            stock_copy['category'] = category['title']
            all_stocks.append(stock_copy)
    
    # Sort by change percentage
    all_stocks.sort(key=lambda x: x['change'], reverse=True)
    
    # Get top 30 gainers and top 30 losers
    top_gainers = all_stocks[:30]
    top_losers = all_stocks[-30:][::-1]  # Reverse to show worst first
    
    # Add recommendations to results
    results_with_recommendations = {
        'recommendations': {
            'title': '💡 Investment Recommendations',
            'data': [],
            'gainers': top_gainers,
            'losers': top_losers
        }
    }
    results_with_recommendations.update(results)
    
    # Load assets
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    with open(os.path.join(frontend_dir, 'template.html'), 'r') as f:
        html_template = f.read()
    with open(os.path.join(frontend_dir, 'styles.css'), 'r') as f:
        styles = f.read()
    with open(os.path.join(frontend_dir, 'script.js'), 'r') as f:
        script = f.read()

    json_data = json.dumps(results_with_recommendations)
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"{timestamp_str}_market_report.html"
    output_dir = "output"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, output_filename)

    # Inject data into JS script string first
    injected_script = script.replace('__DATA__', json_data)
    
    # Assembled HTML
    # We still use a display-friendly timestamp in the HTML if desired, 
    # but the filename uses the safe format.
    display_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = html_template \
        .replace('__STYLES__', styles) \
        .replace('__TIMESTAMP__', display_timestamp) \
        .replace('__SCRIPT__', injected_script)
    
    with open(output_path, "w") as f:
        f.write(html_content)
    
    print(f"Report generated: {output_path}")

def main():
    print("Gathering data and generating interactive report...")
    data = analyze_market.get_market_trends()
    generate_html(data)
    print("Done! Open 'market_report.html' in your browser.")
    
    # Summary of prices as well?
    print("\\nTop Movers Summary:")
    for key, val in data.items():
        if val['data']:
             top = val['data'][0]
             worst = val['data'][-1]
             print(f"{val['title']}:")
             print(f"  Best:  {top['ticker']} ({top['change_str']}) [${top['price_str']}]")
             print(f"  Worst: {worst['ticker']} ({worst['change_str']}) [${worst['price_str']}]")

if __name__ == "__main__":
    main()
