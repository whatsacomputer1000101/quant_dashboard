# config.py
import streamlit as st

def get_api_credentials():
    env = st.secrets["TRADING_ENV"].upper()

    key = st.secrets[f"APCA_API_KEY_ID_{env}"]
    secret = st.secrets[f"APCA_API_SECRET_KEY_{env}"]
    url = st.secrets[f"APCA_API_BASE_URL_{env}"]

    # For Alpaca SDK compatibility
    import os
    os.environ["APCA_API_KEY_ID"] = key
    os.environ["APCA_API_SECRET_KEY"] = secret
    os.environ["APCA_API_BASE_URL"] = url

    return {"key": key, "secret": secret, "url": url}
