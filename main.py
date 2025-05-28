import schedule
import time
from datetime import datetime
from config import get_api_credentials
from executor import execute_trades
from strategy import generate_signals
import yfinance as yf  # Needed for get_trending_stocks

# === Trending Stocks Helper ===
def get_trending_stocks(limit=5):
    # Placeholder: high volume S&P 500 stocks
    sp500_symbols = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META', 'AMZN', 'AMD', 'NFLX', 'INTC']
    
    data = yf.download(sp500_symbols, period="1d", interval="1d", group_by='ticker')

    volume_data = []
    for symbol in sp500_symbols:
        try:
            volume = data[symbol]['Volume'][-1]
            volume_data.append((symbol, volume))
        except:
            continue

    sorted_by_volume = sorted(volume_data, key=lambda x: x[1], reverse=True)
    trending = [symbol for symbol, _ in sorted_by_volume[:limit]]
    return trending

def run_trading_cycle():
    print(f"[{datetime.now()}] Running trading cycle...")

    trending = get_trending_stocks(limit=5)
    top_stocks = ['RDW'] + trending  # Always include RDW

    signals = generate_signals(top_stocks)
    weights = {symbol: 1 / len(signals) for symbol in signals}
    
    execute_trades(signals, weights)
    print(f"[{datetime.now()}] Trading cycle complete.")

schedule.every().day.at("05:30").do(run_trading_cycle)
schedule.every().day.at("13:30").do(run_trading_cycle)

print("Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)