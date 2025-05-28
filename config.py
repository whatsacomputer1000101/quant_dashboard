import os
from dotenv import load_dotenv
load_dotenv()

ENV = os.getenv('ENV', 'paper')  # default to paper

API_KEYS = {
    'paper': {
        'key': os.getenv('PKOZ1KULBUMRJZUPRVJG'),
        'secret': os.getenv('G0EaYtsDmZwY8RHogivfGHGmA4oKNxT9dQx4aG6K'),
        'url': 'https://paper-api.alpaca.markets'
    },
    'live': {
        'key': os.getenv('AKEPWP4ARTWCFMDXWKBC'),
        'secret': os.getenv('QINfX2EjDQlY5HFA5kChON6Yd1gTXK7Ubgr8kelJ'),
        'url': 'https://api.alpaca.markets'
    }
}

def get_api_credentials():
    return API_KEYS[ENV]

