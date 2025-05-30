import os
os.environ["USE_MULTITASKING"] = "False"

import multitasking
multitasking.set_max_threads(1)

from ml_strategy import generate_ml_signals
from executor import execute_trades
from screener import get_top_momentum_stocks, calculate_weights

if __name__ == "__main__":
    print("🚀 Running ML-enhanced strategy with extended historical factors")

    try:
        top_stocks = get_top_momentum_stocks()
        if not top_stocks:
            print("[WARNING] No stocks returned by momentum screener.")
            exit()

        signals = generate_ml_signals(top_stocks)
        if not signals:
            print("[WARNING] No signals generated.")
            exit()

        weights = calculate_weights(signals)
        if not weights:
            print("[WARNING] No valid buy signals. Skipping trade execution.")
            exit()

        execute_trades(signals, weights)

    except Exception as e:
        print(f"[FATAL ERROR] bot_runner.py failed: {e}")
