
from ml_strategy import generate_ml_signals
from executor import execute_trades
from screener import get_top_momentum_stocks, calculate_weights

if __name__ == "__main__":
    print("🚀 Running ML-enhanced strategy with extended historical factors")
    top_stocks = get_top_momentum_stocks()
    signals = generate_ml_signals(top_stocks)
    weights = calculate_weights(signals)
    execute_trades(signals, weights)
