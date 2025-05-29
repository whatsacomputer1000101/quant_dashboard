# config.py
import os

def get_api_credentials():
    env = os.getenv("TRADING_ENV", "PAPER").upper()

    if env == "LIVE":
        return {
            "key": os.getenv("AKEPWP4ARTWCFMDXWKBC"),
            "secret": os.getenv("QINfX2EjDQlY5HFA5kChON6Yd1gTXK7Ubgr8kelJ"),
            "url": os.getenv("APCA_API_BASE_URL_LIVE", "https://api.alpaca.markets")
        }
    else:
        return {
            "key": os.getenv("PKOZ1KULBUMRJZUPRVJG"),
            "secret": os.getenv("G0EaYtsDmZwY8RHogivfGHGmA4oKNxT9dQx4aG6K"),
            "url": os.getenv("APCA_API_BASE_URL_PAPER", "https://paper-api.alpaca.markets")
        }