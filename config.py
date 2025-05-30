# config.py
import os
import streamlit as st

def get_api_credentials():
    try:
        env = st.secrets.get("TRADING_ENV", "PAPER").upper()

        key = st.secrets.get(f"APCA_API_KEY_ID_{env}")
        secret = st.secrets.get(f"APCA_API_SECRET_KEY_{env}")
        url = st.secrets.get(f"APCA_API_BASE_URL_{env}")

        if not key or not secret or not url:
            raise KeyError("Missing Alpaca secrets in Streamlit config.")

    except Exception:
        # fallback: try OS environment variables
        env = os.getenv("TRADING_ENV", "PAPER").upper()

        key = os.getenv(f"APCA_API_KEY_ID_{env}")
        secret = os.getenv(f"APCA_API_SECRET_KEY_{env}")
        url = os.getenv(f"APCA_API_BASE_URL_{env}")

        if not key or not secret or not url:
            raise EnvironmentError(f"Missing Alpaca credentials for environment: {env}")

    # Set them for Alpaca SDK usage
    os.environ["APCA_API_KEY_ID"] = key
    os.environ["APCA_API_SECRET_KEY"] = secret
    os.environ["APCA_API_BASE_URL"] = url

    return {"key": key, "secret": secret, "url": url}
