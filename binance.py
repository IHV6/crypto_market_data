import requests
import threading
import matplotlib.pyplot as plt
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


def create_plot():
    global graph
    global date_time
    global ax
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    graph = []
    date_time = []


def get_graph(price, date, symbol):
    graph.append(float(price))
    date_time.append(date)
    ax.clear()
    ax.plot(date_time, graph)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title(f'{symbol} Price history')
    plt.ylabel('Price')
    plt.xlabel('Time')
    plt.draw()
    plt.pause(15)


def run():
    symbol = get_inputs()
    price = get_price(symbol)
    print(f'Actual {symbol[0]} price for {symbol[1]} at '
          f'({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}):', f'{float(price):,}')
    create_plot()

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
        get_graph(price, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), symbol[0])
        threading.Timer(15, recursion(price)).start()
    recursion(price)


run()
