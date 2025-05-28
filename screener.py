# screener.py

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Example subset of S&P 500 stocks
sp500_symbols = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA',
    'TSLA', 'AMD', 'NFLX', 'INTC', 'PEP', 'AVGO'
]

def get_top_momentum_stocks(n=10):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)

    df = yf.download(sp500_symbols, start=start_date, end=end_date)['Adj Close']

    momentum_scores = {}
    for symbol in df.columns:
        try:
            r1w = df[symbol].pct_change(5).iloc[-1]
            r1m = df[symbol].pct_change(21).iloc[-1]
            r3m = df[symbol].pct_change(63).iloc[-1]
            score = 0.2 * r1w + 0.3 * r1m + 0.5 * r3m
            momentum_scores[symbol] = score
        except Exception:
            continue

    top_symbols = sorted(momentum_scores, key=momentum_scores.get, reverse=True)[:n]
    return top_symbols

def calculate_weights(symbols):
    if not symbols:
        return {}
    weight = 1 / len(symbols)
    return {symbol: weight for symbol in symbols}