# screener.py

import os
os.environ["USE_MULTITASKING"] = "False"

import yfinance as yf
import multitasking
multitasking.set_max_threads(1)  # ⛔ limit to one thread only

import pandas as pd
from datetime import datetime, timedelta

def get_top_momentum_stocks(n=10):
    sp500_symbols = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META', 'AMZN', 'AMD', 'NFLX', 'INTC']
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)

    df = yf.download(
    sp500_symbols,
    start=start_date,
    end=end_date,
    group_by="ticker",
    threads=False  # 🔒 disables threading to avoid Streamlit crash
)

if isinstance(df.columns, pd.MultiIndex):
    adj_close = pd.DataFrame({
        ticker: df[ticker]['Adj Close']
        for ticker in df.columns.levels[0]
        if 'Adj Close' in df[ticker]
    })
else:
    return []


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

def calculate_weights(signals):
    """
    Assign equal weights to each stock in the signal list.
    :param signals: dict of symbols with 'buy', 'hold', or 'sell'
    :return: dict of weights
    """
    buy_signals = [symbol for symbol, signal in signals.items() if signal == 'buy']
    if not buy_signals:
        return {}

    weight = 1 / len(buy_signals)
    return {symbol: weight for symbol in buy_signals}