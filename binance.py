import requests
import threading
from datetime import datetime


def get_inputs():
    return input('Crypto name: ').upper().rstrip().strip(), input('Fiat name: ').upper().rstrip().strip()


def get_price(symbol):
    crypto_and_fiat = symbol[0] + symbol[1]
    r = requests.get(f'https://api.binance.com/api/v3/avgPrice?symbol={crypto_and_fiat}')
    response = r.json()
    try:
        return response['price']
    except KeyError:
        print("Wrong input data. Try one more time.")
        run()


def run():
    symbol = get_inputs()
    price = get_price(symbol)
    print(f'Actual {symbol[0]} price for {symbol[1]} at '
          f'({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}):', f'{float(price):,}')

    def recursion(price):
        new_price = get_price(symbol)
        if price != new_price:
            if new_price > price:
                price = new_price
                print("\U0001F7E2", f'Actual {symbol[0]} price for {symbol[1]} at '
                                    f'({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}):', f'{float(price):,}')
            else:
                price = new_price
                print("\U0001F534", f'Actual {symbol[0]} price for {symbol[1]} at '
                                    f'({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}):', f'{float(price):,}')
        threading.Timer(30, recursion(price)).start()
    recursion(price)


run()
