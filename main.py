# main.py — full signal + execution pipeline
from strategy import generate_signals
from executor import execute_trades
from screener import get_top_momentum_stocks, calculate_weights

if __name__ == "__main__":
    print("🚀 Starting strategy execution")
    top_stocks = get_top_momentum_stocks()
    signals = generate_signals(top_stocks)
    weights = calculate_weights(top_stocks)
    execute_trades(signals, weights)
