import yfinance as yf
import pandas as pd
import numpy as np

def compute_factors(symbol, period='10y', interval='1d'):
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False, threads=False)

    # Flatten MultiIndex if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Ensure critical columns are present
    required = ['Adj Close', 'High', 'Low', 'Close']
    if not all(col in df.columns for col in required):
        raise ValueError(f"{symbol} missing required columns: {df.columns.tolist()}")

    df.dropna(inplace=True)

    df['returns'] = df['Adj Close'].pct_change()
    df['volatility_6m'] = df['returns'].rolling(window=126).std()
    df['momentum_12m'] = df['Adj Close'].pct_change(periods=252)

    # Compute beta vs SPY
    spy = yf.download('SPY', period=period, interval=interval, auto_adjust=False, progress=False, threads=False)
    if isinstance(spy.columns, pd.MultiIndex):
        spy.columns = spy.columns.get_level_values(0)

    if 'Adj Close' not in spy.columns:
        raise ValueError(f"'Adj Close' missing for SPY.")

    spy['spy_returns'] = spy['Adj Close'].pct_change()
    combined = pd.concat([df['returns'], spy['spy_returns']], axis=1).dropna()
    cov = combined.cov().iloc[0, 1]
    var = combined['spy_returns'].var()
    df['beta_vs_spy'] = cov / var if var != 0 else np.nan

    return df  # Return all price data + factors for downstream logic
