import os
os.environ["USE_MULTITASKING"] = "False"

import multitasking
multitasking.set_max_threads(1)

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_top_momentum_stocks(n=10):
    sp500_symbols = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META', 'AMZN', 'AMD', 'NFLX', 'INTC']
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)

    momentum_scores = {}

    for symbol in sp500_symbols:
        try:
            df = yf.download(
                symbol,
                start=start_date,
                end=end_date,
                interval="1d",
                auto_adjust=False,
                progress=False,
                threads=False
            )

            if df.empty or 'Adj Close' not in df.columns:
                print(f"[WARN] No valid data for {symbol}")
                continue

            prices = df['Adj Close'].dropna()
            if len(prices) < 2:
                print(f"[WARN] Not enough price data for {symbol}")
                continue

            # Use .item() to extract scalars from single-element Series
            start_price = prices.iloc[0].item()
            end_price = prices.iloc[-1].item()
            momentum = (end_price - start_price) / start_price

            momentum_scores[symbol] = momentum

        except Exception as e:
            print(f"[WARN] Failed to fetch data for {symbol}: {e}")

    sorted_momentum = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
    return [symbol for symbol, _ in sorted_momentum[:n]]

def calculate_weights(signals):
    buy_signals = [symbol for symbol, signal in signals.items() if signal == 'buy']
    if not buy_signals:
        return {}
    weight = 1 / len(buy_signals)
    return {symbol: weight for symbol in buy_signals}
