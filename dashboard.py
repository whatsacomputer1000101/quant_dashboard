import streamlit as st
from utils import load_trade_log
from config import get_api_credentials
import alpaca_trade_api as tradeapi
import os

st.set_page_config(page_title="Quant Trading Dashboard", layout="wide")
st.title("📈 Quant Trading System Dashboard")

# Display environment mode
ENV = os.getenv("ENV", "paper")
env_color = "green" if ENV == "paper" else "red"
env_label = "🧪 Paper Trading" if ENV == "paper" else "🚨 LIVE Trading"

st.sidebar.markdown("### Environment Status")
st.sidebar.markdown(
    f"<div style='color:{env_color}; font-weight:bold; font-size:16px'>{env_label}</div>",
    unsafe_allow_html=True
)

if ENV == "live":
    st.sidebar.warning("⚠️ You are in LIVE trading mode. Be cautious!")

# Account summary via Alpaca
creds = get_api_credentials()
api = tradeapi.REST(
    key_id=creds['key'],
    secret_key=creds['secret'],
    base_url=creds['url'],
    raw_data=True  # ensures no env lookup fallback
)
account = api.get_account()

st.sidebar.header("Alpaca Account Summary")
st.sidebar.metric("Equity", f"${float(account.equity):,.2f}")
st.sidebar.metric("Cash", f"${float(account.cash):,.2f}")
st.sidebar.metric("Buying Power", f"${float(account.buying_power):,.2f}")

# Open positions
positions = api.list_positions()
if positions:
    st.subheader("Current Positions")
    pos_data = [{
        "symbol": p.symbol,
        "qty": int(p.qty),
        "avg_price": float(p.avg_entry_price),
        "market_price": float(p.current_price),
        "unrealized_pl": float(p.unrealized_pl)
    } for p in positions]
    st.dataframe(pos_data)
else:
    st.info("No open positions")

# Trade log and summaries
st.subheader("Trade Log")
df = load_trade_log()
if df.empty:
    st.warning("No trade data available yet.")
else:
    st.dataframe(df.sort_values(by="timestamp", ascending=False))

    st.subheader("Trade Summary")
    summary = df.groupby(['symbol', 'action']).agg(count=('qty', 'size'), avg_price=('price', 'mean')).reset_index()
    st.dataframe(summary)

    st.subheader("Daily Trade Activity")
    df['date'] = df['timestamp'].dt.date
    daily_summary = df.groupby('date').size().reset_index(name='trades')
    st.bar_chart(data=daily_summary, x='date', y='trades')
