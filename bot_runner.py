import os
os.environ["USE_MULTITASKING"] = "False"
import multitasking
multitasking.set_max_threads(1)

from ml_strategy import generate_ml_signals
from screener import get_top_momentum_stocks, calculate_weights
import traceback

if __name__ == "__main__":
    print("🚀 Running ML-enhanced strategy with extended historical factors")

    try:
        top_stocks = get_top_momentum_stocks()
        print("Top Stocks:", top_stocks)

        signals = generate_ml_signals(top_stocks)
        print("Signals:", signals)

        weights = calculate_weights(signals)
        print("Weights:", weights)

    except Exception as e:
        print(f"[FATAL ERROR] bot_runner.py failed: {e}")
        traceback.print_exc()
