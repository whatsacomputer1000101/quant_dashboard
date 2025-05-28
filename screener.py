import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_top_momentum_stocks(n=10):
    sp500_symbols = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META', 'AMZN', 'AMD', 'NFLX', 'INTC']
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)

    df = yf.download(sp500_symbols, start=start_date, end=end_date, group_by='ticker')

    # Extract 'Adj Close' data properly from multi-indexed DataFrame
    adj_close = pd.DataFrame({
        ticker: df[ticker]['Adj Close']
        for ticker in df.columns.levels[0]
        if 'Adj Close' in df[ticker]
    })

    momentum_scores = {}
    for symbol in adj_close.columns:
        prices = adj_close[symbol].dropna()
        if len(prices) > 1:
            momentum = (prices[-1] - prices[0]) / prices[0]
            momentum_scores[symbol] = momentum

    sorted_momentum = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
    top_stocks = [symbol for symbol, _ in sorted_momentum[:n]]

    return top_stocks