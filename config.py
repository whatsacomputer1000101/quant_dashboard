ENV = 'paper'

API_KEYS = {
    'paper': {
        'key': 'YOUR_PAPER_API_KEY',
        'secret': 'YOUR_PAPER_SECRET_KEY',
        'url': 'https://paper-api.alpaca.markets'
    },
    'live': {
        'key': 'YOUR_LIVE_API_KEY',
        'secret': 'YOUR_LIVE_SECRET_KEY',
        'url': 'https://api.alpaca.markets'
    }
}

def get_api_credentials():
    return API_KEYS[ENV]
