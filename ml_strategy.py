import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD
from factors import compute_factors


def generate_ml_signals(stock_list):
    signals = {}

    for symbol in stock_list:
        print(f"[INFO] Processing: {symbol}")
        try:
            df = compute_factors(symbol)

            if df.empty:
                raise ValueError(f"No factor data for {symbol}")

            # Ensure the DataFrame isn't multi-dimensional in any column
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Compute RSI and MACD on Adj Close
            rsi = RSIIndicator(close=df['Adj Close'].squeeze()).rsi()
            macd_line = MACD(close=df['Adj Close'].squeeze()).macd_diff()

            # Combine into signal logic
            if rsi.iloc[-1] < 30 and macd_line.iloc[-1] > 0:
                signals[symbol] = "buy"
            elif rsi.iloc[-1] > 70 and macd_line.iloc[-1] < 0:
                signals[symbol] = "sell"
            else:
                signals[symbol] = "hold"

        except Exception as e:
            print(f"Error:  Failed for {symbol}: {e}")
            signals[symbol] = "hold"

    return signals
