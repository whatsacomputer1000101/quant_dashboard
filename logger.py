import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def log_trade_to_sheet(symbol, action, qty, price, status="executed"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Replace with your actual Google Sheet name
    sheet = client.open("Trade Log").sheet1  

    # Append trade row
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, symbol, action, qty, price, status]
    sheet.append_row(row)
