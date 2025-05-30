import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator
from sklearn.neighbors import KNeighborsClassifier
from factors import compute_factors

def fetch_price_data(symbol, period='10y', interval='1d'):
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False, threads=False)
    df.dropna(inplace=True)
    return df

def generate_ml_signals(symbols):
    signals = {}
    for symbol in symbols:
        try:
            factors = compute_factors(symbol)
            df = fetch_price_data(symbol)

            # Align and intersect common dates
            common_index = df.index.intersection(factors.index)
            df = df.loc[common_index]
            factors = factors.loc[common_index]

            if df.empty or factors.empty or len(df) < 31:
                print(f"[WARN] Insufficient data for {symbol}")
                continue

            # Create label as aligned Series
            label = (df['Adj Close'].shift(-1) > df['Adj Close']).astype(int)
            df = df.iloc[:-1]  # drop last row (no label)
            label = label.iloc[:-1]
            df['label'] = label

            # Technical indicators
            rsi = RSIIndicator(close=df['Adj Close']).rsi()
            macd = MACD(close=df['Adj Close']).macd_diff()
            sma = SMAIndicator(close=df['Adj Close']).sma_indicator()

            df['rsi'] = rsi
            df['macd'] = macd
            df['sma'] = sma

            df = pd.concat([df, factors], axis=1)
            df.dropna(inplace=True)

            if len(df) < 30:
                print(f"[WARN] Skipping {symbol}, insufficient data after cleaning")
                continue

            features = df[['rsi', 'macd', 'sma', 'volatility_6m', 'momentum_12m', 'beta_vs_spy']]
            X_train = features[:-1]
            y_train = df['label'][:-1]
            X_pred = features.iloc[[-1]]

            model = KNeighborsClassifier(n_neighbors=3)
            model.fit(X_train, y_train)
            pred = model.predict(X_pred)[0]

            signals[symbol] = 'buy' if pred == 1 else 'sell'

        except Exception as e:
            print(f"[ERROR] Failed for {symbol}: {e}")
            continue

    return signals
