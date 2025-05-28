from executor import execute_trades
from screener import get_top_momentum_stocks, calculate_weights
from ml_strategy import generate_signals_ml
from datetime import datetime

if __name__ == "__main__":
    print(f"[{datetime.now()}] 🚀 Starting ML strategy")
    top_stocks = get_top_momentum_stocks()
    signals = generate_signals_ml(top_stocks)
    weights = calculate_weights(top_stocks)
    execute_trades(signals, weights)