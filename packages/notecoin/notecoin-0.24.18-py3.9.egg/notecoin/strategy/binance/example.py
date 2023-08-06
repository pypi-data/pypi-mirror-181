import json

import pandas as pd
from notecoin.base.tables.strategy import StrategyTable
from notecoin.task import AccountTask, BaseTask, MarketTask, Ticker24HTask
from notecoin.utils import logger

logger.set
class StrategyTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super(StrategyTask, self).__init__(*args, **kwargs)
        self.table = StrategyTable(db_suffix=self.exchange.name)
        self.table.create()

    def refresh(self):
        account = pd.read_sql(sql=f"select * from {AccountTask.table_name}", con=self.engine.connect())
        curr = 0
        for symbol in json.loads(account.to_json(orient='records')):
            if symbol['symbol'] == 'BUSD':
                curr = symbol['free']
        if curr < 12:
            logger.info("account<12")
            return
        market = pd.read_sql(sql=f"select * from {MarketTask.table_name}", con=self.engine.connect())
        ticker24h = pd.read_sql(sql=f"select * from {Ticker24HTask.table_name}", con=self.engine.connect())
        ticker24h = ticker24h.sort_values(['quoteVolume'], ascending=False).reset_index(drop=True)
        for symbol in json.loads(ticker24h.to_json(orient='records')):
            if symbol['symbol'].endswith('BUSD'):
                tmp = market[market['id'] == symbol]
                if len(tmp) == 1:
                    self.buy_market(tmp['symbol'].values[0])
                    break
        logger.info("done")

    def buy_market(self, symbol, total=12):
        price = self.current_price(symbol)
        if price == 0:
            return
        logger.info(f"buy {symbol}")

        amount = total / price
        # self.exchange.create_order(symbol, 'market', 'buy', amount)
        value = {
            "symbol": symbol,
            "amount": amount,
            "buy_price": price,
        }

        self.table.upsert(values=[value])


task = StrategyTask()
task.refresh()
