import yfinance as yf
import pandas as pd
import numpy as np

def compute_factors(symbol, period='10y', interval='1d'):
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False, threads=False)

    # Flatten MultiIndex if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Ensure 'Adj Close' exists
    if 'Adj Close' not in df.columns:
        raise ValueError(f"'Adj Close' missing for {symbol}. Available columns: {df.columns.tolist()}")

    df.dropna(inplace=True)

    df['returns'] = df['Adj Close'].pct_change()
    df['volatility_6m'] = df['returns'].rolling(window=126).std()  # ~6 months
    df['momentum_12m'] = df['Adj Close'].pct_change(periods=252)   # ~1 year

    # Dummy beta to SPY for now
    spy = yf.download('SPY', period=period, interval=interval, auto_adjust=False, progress=False, threads=False)
    if isinstance(spy.columns, pd.MultiIndex):
        spy.columns = spy.columns.get_level_values(0)

    if 'Adj Close' not in spy.columns:
        raise ValueError(f"'Adj Close' missing for SPY.")

    spy['spy_returns'] = spy['Adj Close'].pct_change()
    combined = pd.concat([df['returns'], spy['spy_returns']], axis=1).dropna()
    cov = combined.cov().iloc[0, 1]
    var = combined['spy_returns'].var()
    beta = cov / var if var != 0 else np.nan
    df['beta_vs_spy'] = beta

    return df[['Adj Close', 'volatility_6m', 'momentum_12m', 'beta_vs_spy']]
