import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator
from sklearn.preprocessing import StandardScaler

def get_features_labels(ticker, period="2y", interval="1d"):
    df = yf.download(ticker, period=period, interval=interval)
    df.dropna(inplace=True)

    df['RSI'] = RSIIndicator(close=df['Close']).rsi()
    macd = MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['Signal'] = macd.macd_signal()
    df['SMA'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()

    df['Future Return'] = df['Close'].pct_change().shift(-1)
    df['Label'] = np.where(df['Future Return'] > 0.01, 1, np.where(df['Future Return'] < -0.01, -1, 0))

    df.dropna(inplace=True)

    features = df[['RSI', 'MACD', 'Signal', 'SMA']]
    labels = df['Label']
    return features, labels, df.index

def train_model(features, labels):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_scaled, labels)
    return model, scaler

def generate_signals_ml(tickers):
    signals = {}
    for ticker in tickers:
        try:
            features, labels, idx = get_features_labels(ticker)
            model, scaler = train_model(features, labels)
            latest_features = scaler.transform([features.iloc[-1]])
            prediction = model.predict(latest_features)[0]
            if prediction == 1:
                signals[ticker] = 'buy'
            elif prediction == -1:
                signals[ticker] = 'sell'
            else:
                signals[ticker] = 'hold'
        except Exception as e:
            print(f"[ML ERROR] {ticker}: {e}")
            signals[ticker] = 'hold'
    return signals