import requests
import threading
from datetime import datetime


crypto = input('Crypto name: ')
fiat = input('Fiat name: ')
symbol = crypto + fiat


def get_data():
    r = requests.get(f'https://api.binance.com/api/v3/avgPrice?symbol={symbol}')
    return r.json()


def get_price():
    response = get_data()
    return response['price']


price = get_price()
print(f'Actual price ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}):', price)


def run():
    global price
    new_price = get_price()
    if price != new_price:
        price = new_price
        print(f'Actual price ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}):', price)
    threading.Timer(30, run).start()


run()
