import requests
import threading
from datetime import datetime


class MarketData:
    def __init__(self):
        crypto = input('Crypto name: ')
        fiat = input('Fiat name: ')
        self.symbol = crypto + fiat
        self.price = self.get_price()
        print(f'Actual price ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}):', self.price)

    def get_data(self):
        r = requests.get(f'https://api.binance.com/api/v3/avgPrice?symbol={self.symbol}')
        return r.json()

    def get_price(self):
        response = self.get_data()
        try:
            return response['price']
        except Exception:
            raise KeyError("Wrong input data. Try one more time.")

    def run(self):
        new_price = self.get_price()
        if self.price != new_price:
            if new_price > self.price:
                self.price = new_price
                print('\U0001F7E2', f'Actual price ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}):', self.price)
            else:
                self.price = new_price
                print('\U0001F534', f'Actual price ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}):', self.price)
        threading.Timer(30, self.run).start()


MarketData().run()
