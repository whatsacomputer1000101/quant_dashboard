import yfinance as yf
import pandas as pd
import numpy as np

def compute_factors(symbol, period='10y', interval='1d'):
    # Download symbol data
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False, threads=False)

    # Handle MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Validate critical column
    if 'Adj Close' not in df.columns:
        raise ValueError(f"[ERROR] 'Adj Close' column missing for {symbol}")

    df = df.dropna()
    df['returns'] = df['Adj Close'].pct_change()
    df['volatility_6m'] = df['returns'].rolling(window=126).std()
    df['momentum_12m'] = df['Adj Close'].pct_change(periods=252)

    # Fetch SPY for beta calculation
    spy = yf.download('SPY', period=period, interval=interval, auto_adjust=False, progress=False, threads=False)
    if isinstance(spy.columns, pd.MultiIndex):
        spy.columns = spy.columns.get_level_values(0)

    if 'Adj Close' not in spy.columns:
        raise ValueError("[ERROR] 'Adj Close' column missing for SPY")

    spy['spy_returns'] = spy['Adj Close'].pct_change()
    combined = pd.concat([df['returns'], spy['spy_returns']], axis=1).dropna()

    # Calculate beta vs SPY
    cov = combined.cov().iloc[0, 1]
    var = combined['spy_returns'].var()
    beta = cov / var if var != 0 else np.nan
    df['beta_vs_spy'] = beta

    return df[['volatility_6m', 'momentum_12m', 'beta_vs_spy']].dropna()
