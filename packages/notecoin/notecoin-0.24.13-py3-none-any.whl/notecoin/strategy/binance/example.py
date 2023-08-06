import pandas as pd
from notecoin.base.tables.strategy import StrategyTable
from notecoin.task import BaseTask


class StrategyTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super(StrategyTask, self).__init__(*args, **kwargs)
        self.table = StrategyTable(db_suffix=self.exchange.name)
        self.table.create()

    def refresh(self):
        param = {"type": "MINI"}
        df = pd.DataFrame(self.exchange.public_get_ticker_24hr(param))
        df.to_sql(name=self.table_name, con=self.engine.connect(), if_exists='replace')


task = StrategyTask()
