
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator
from sklearn.neighbors import KNeighborsClassifier
from factors import compute_factors

def fetch_price_data(symbol, period='10y', interval='1d'):
    df = yf.download(symbol, period=period, interval=interval)
    df.dropna(inplace=True)
    return df

def generate_ml_signals(symbols):
    signals = {}
    for symbol in symbols:
        df = fetch_price_data(symbol)
        if df.empty:
            continue

        rsi = RSIIndicator(close=df['Adj Close']).rsi()
        macd = MACD(close=df['Adj Close']).macd_diff()
        sma = SMAIndicator(close=df['Adj Close']).sma_indicator()

        factors = compute_factors(symbol)
        df = df[-len(factors):]
        df['rsi'] = rsi[-len(factors):].values
        df['macd'] = macd[-len(factors):].values
        df['sma'] = sma[-len(factors):].values

        df = pd.concat([df, factors], axis=1).dropna()

        features = df[['rsi', 'macd', 'sma', 'volatility_6m', 'momentum_12m', 'beta_vs_spy']]
        df['label'] = (df['Adj Close'].shift(-1) > df['Adj Close']).astype(int)

        if len(df) < 30:
            continue

        X_train = features[:-1]
        y_train = df['label'][:-1]
        X_pred = features.iloc[[-1]]

        model = KNeighborsClassifier(n_neighbors=3)
        model.fit(X_train, y_train)
        pred = model.predict(X_pred)[0]

        signals[symbol] = 'buy' if pred == 1 else 'sell'
    return signals
