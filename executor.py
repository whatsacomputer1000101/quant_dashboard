# ---- MODULE: executor.py ----
# Execute trades via Alpaca (ATR-based stop-loss)
import os
import alpaca_trade_api as tradeapi
from config import get_api_credentials
from datetime import datetime
import time
import yfinance as yf
import pandas as pd

TRADE_LOG = "trade_log.csv"
TRADE_LIMIT = 10  # Max trades per week

def get_atr(symbol, period=14):
    df = yf.download(symbol, period="2mo", interval="1d")
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=period).mean()
    return round(df['ATR'].iloc[-1], 2)

def execute_trades(signals, weights):
    creds = get_api_credentials()
    api = tradeapi.REST(creds['key'], creds['secret'], creds['url'])

    trade_count = count_trades_this_week()
    print(f"[INFO] Trades executed this week: {trade_count}")
    
    for symbol, signal in signals.items():
        if trade_count >= TRADE_LIMIT:
            print("[LIMIT] Weekly trade cap reached. Skipping further trades.")
            break
        if signal == 'hold':
            continue

        qty = calculate_qty(api, symbol, weights.get(symbol, 0))
        if qty == 0:
            continue

        price = float(api.get_last_trade(symbol).price)
        atr = get_atr(symbol)
        stop_loss = round(price - 1.5 * atr, 2)
        take_profit = round(price + 2.5 * atr, 2)

        try:
            side = 'buy' if signal == 'buy' else 'sell'
            api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type='market',
                time_in_force='gtc',
                order_class='bracket',
                stop_loss={'stop_price': stop_loss},
                take_profit={'limit_price': take_profit}
            )
            log_trade(datetime.now(), symbol, side, qty, price)
            print(f"[TRADE] {side.upper()} {qty} shares of {symbol} @ ${price}")
            trade_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to execute {signal} on {symbol}: {e}")
            continue

def calculate_qty(api, symbol, weight):
    try:
        account = api.get_account()
        cash = float(account.cash)
        alloc = cash * weight
        price = float(api.get_last_trade(symbol).price)
        qty = int(alloc // price)
        return qty
    except:
        return 0

def log_trade(timestamp, symbol, action, qty, price):
    with open(TRADE_LOG, "a") as f:
        f.write(f"{timestamp},{symbol},{action},{qty},{price}
")

def count_trades_this_week():
    from datetime import datetime, timedelta
    if not os.path.exists(TRADE_LOG):
        return 0
    count = 0
    week_ago = datetime.now() - timedelta(days=7)
    with open(TRADE_LOG, "r") as f:
        for line in f:
            try:
                timestamp = datetime.strptime(line.split(',')[0], '%Y-%m-%d %H:%M:%S.%f')
                if timestamp >= week_ago:
                    count += 1
            except:
                continue
    return count