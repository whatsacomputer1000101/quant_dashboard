# Quant Dashboard

This is a deployable Streamlit dashboard for monitoring live trading activity with Alpaca.

## Setup

1. Clone this repo
2. Create a `.env` file using the included `.env.template`
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```
4. Run the dashboard locally:
   ```
   streamlit run dashboard.py
   ```

## Deploy to Streamlit Cloud

Use the secrets manager to add:

```
ALPACA_PAPER_KEY
ALPACA_PAPER_SECRET
ENV = paper
```
