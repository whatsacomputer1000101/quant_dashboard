import yfinance as yf
import multitasking
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

yf.pdr_override()
multitasking.set_max_threads(1)

def get_top_momentum_stocks(n=10):
    fixed_symbols = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META', 'AMZN', 'AMD', 'NFLX', 'INTC']
    all_symbols = fixed_symbols.copy()

    # Sample dynamic candidates
    potential_symbols = ['AVGO', 'ADBE', 'PEP', 'COST', 'CRM', 'ORCL', 'TXN', 'QCOM', 'LLY', 'UNH',
                         'UPS', 'WMT', 'HD', 'JNJ', 'PG', 'V', 'MA', 'BAC', 'DIS', 'NKE']

    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)
    momentum_scores = {}

    for symbol in potential_symbols:
        try:
            df = yf.download(symbol, start=start_date, end=end_date, progress=False, threads=False)
            if df.empty or 'Adj Close' not in df.columns or 'Volume' not in df.columns:
                continue

            df.dropna(inplace=True)
            if len(df) < 2 or df['Volume'].mean() < 1_000_000:
                continue

            momentum = (df['Adj Close'].iloc[-1] - df['Adj Close'].iloc[0]) / df['Adj Close'].iloc[0]
            momentum_scores[symbol] = momentum

        except Exception:
            continue

    sorted_momentum = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
    top_dynamic = [symbol for symbol, _ in sorted_momentum[:n]]

    all_symbols.extend(top_dynamic)
    return all_symbols

def calculate_weights(signals):
    buy_signals = [symbol for symbol, signal in signals.items() if signal == 'buy']
    if not buy_signals:
        return {}
    weight = 1 / len(buy_signals)
    return {symbol: weight for symbol in buy_signals}