
import pandas as pd
import os
from alpaca_trade_api.rest import REST
from config import get_api_credentials
from datetime import datetime, timedelta

TRADE_LOG_PATH = "trade_log.csv"

def load_trade_log():
    if os.path.exists(TRADE_LOG_PATH):
        df = pd.read_csv(TRADE_LOG_PATH, parse_dates=["timestamp"])
        return df
    return pd.DataFrame(columns=["timestamp", "symbol", "action", "qty", "price", "gain"])

def save_trade_log(df):
    df.to_csv(TRADE_LOG_PATH, index=False)

def log_trade(symbol, action, qty, price, gain):
    df = load_trade_log()
    new_trade = pd.DataFrame([{
        "timestamp": datetime.now(),
        "symbol": symbol,
        "action": action,
        "qty": qty,
        "price": price,
        "gain": gain
    }])
    df = pd.concat([df, new_trade], ignore_index=True)
    save_trade_log(df)

def log_weekly_performance():
    df = load_trade_log()
    if df.empty:
        return False
    df['week'] = df['timestamp'].dt.isocalendar().week
    current_week = datetime.now().isocalendar().week
    df = df[df['week'] == current_week]
    total_gain = df['gain'].sum()
    total_trades = df.shape[0]
    print(f"📊 Weekly Gain: ${total_gain:.2f}, Trades: {total_trades}")
    return total_gain >= 500 or total_trades >= 30
