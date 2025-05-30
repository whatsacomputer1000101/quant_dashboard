
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import AverageTrueRange
from factors import compute_factors

def generate_ml_signals(stock_list):
    signals = {}

    for symbol in stock_list:
        print(f"[INFO] Processing: {symbol}")
        try:
            df = compute_factors(symbol)

            if df.empty or 'Adj Close' not in df.columns:
                raise ValueError(f"No valid data for {symbol}")

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df.dropna(inplace=True)
            if len(df) < 30:
                continue

            rsi = RSIIndicator(close=df['Adj Close'].squeeze()).rsi()
            macd = MACD(close=df['Adj Close'].squeeze()).macd_diff()
            ema_fast = EMAIndicator(close=df['Adj Close'], window=12).ema_indicator()
            ema_slow = EMAIndicator(close=df['Adj Close'], window=26).ema_indicator()
            atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Adj Close']).average_true_range()

            zscore = (df['Adj Close'] - df['Adj Close'].rolling(window=20).mean()) / df['Adj Close'].rolling(window=20).std()

            latest_rsi = rsi.iloc[-1]
            latest_macd = macd.iloc[-1]
            latest_ema_fast = ema_fast.iloc[-1]
            latest_ema_slow = ema_slow.iloc[-1]
            latest_zscore = zscore.iloc[-1]
            latest_atr = atr.iloc[-1]

            if latest_rsi < 40 and latest_zscore < -0.5 and latest_macd > 0:
                signals[symbol] = "buy"
            elif 40 <= latest_rsi <= 60 and abs(latest_zscore) < 0.25 and latest_ema_fast > latest_ema_slow:
                signals[symbol] = "buy"
            elif latest_rsi > 70 and latest_macd < 0:
                signals[symbol] = "sell"
            else:
                signals[symbol] = "hold"

        except Exception as e:
            print(f"Error: Failed for {symbol}: {e}")
            signals[symbol] = "hold"

    return signals
