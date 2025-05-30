import os
from dotenv import load_dotenv

# Try .env first
load_dotenv()

def get_api_credentials():
    env = os.getenv("TRADING_ENV", "PAPER").upper()

    key = os.getenv(f"APCA_API_KEY_ID_{env}") or os.environ.get(f"SECRETS_APCA_API_KEY_ID_{env}")
    secret = os.getenv(f"APCA_API_SECRET_KEY_{env}") or os.environ.get(f"SECRETS_APCA_API_SECRET_KEY_{env}")
    url = os.getenv(f"APCA_API_BASE_URL_{env}") or os.environ.get(f"SECRETS_APCA_API_BASE_URL_{env}")

    if not key or not secret or not url:
        raise EnvironmentError(f"Missing Alpaca credentials for environment: {env}")

    os.environ["APCA_API_KEY_ID"] = key
    os.environ["APCA_API_SECRET_KEY"] = secret
    os.environ["APCA_API_BASE_URL"] = url

    return {"key": key, "secret": secret, "url": url}
