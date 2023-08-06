# Python
from asyncio import run

import ccxt.pro as ccxtpro


async def main():
    exchange = ccxtpro.kraken({'newUpdates': False})
    while True:
        # orderbook = await exchange.watch_ohlcv('BTC/USD')
        orderbook = await exchange.watch_trades('BTC/USD')
        # orderbook = await exchange.watch_order_book('BTC/USD')
        # print(orderbook['asks'][0], orderbook['bids'][0])
        print(orderbook)


run(main())
print('3232')
