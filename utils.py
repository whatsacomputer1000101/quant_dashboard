import pandas as pd

def load_trade_log(path="trade_log.csv"):
    try:
        df = pd.read_csv(path, names=["timestamp", "symbol", "action", "qty", "price"])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load trade log: {e}")
        return pd.DataFrame()

def summarize_trades(df):
    if df.empty:
        print("No trades logged.")
        return
    print(f"Total Trades: {len(df)}")
    print(df.groupby(['symbol', 'action']).size())
    print(f"Average Trade Price:\n{df.groupby('symbol')['price'].mean()}")
