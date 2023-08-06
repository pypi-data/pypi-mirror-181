from notecoin.base.db import BaseTable
from sqlalchemy import (DATETIME, JSON, Column, Float, Identity, Integer,
                        String, Table, text)


class StrategyTable(BaseTable):
    

    def __init__(self,table_name = "strategy", *args, **kwargs):
        super(StrategyTable, self).__init__(*args, **kwargs)
        self.table_name=table_name
        self.table = Table(self.table_name,
                           Column('id', Integer, Identity(start=42, cycle=True), comment='自增ID', primary_key=True),
                           Column('gmt_create', DATETIME, comment='创建时间', server_default=text('NOW()')),
                           Column('gmt_modified', DATETIME, comment='修改时间',
                                  server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
                           Column('ext_json', JSON, comment='拓展'),
                           Column('symbol', String(30), comment='symbol'),
                           Column('amount', Float, comment='amount'),
                           Column('buy_price', Float, comment='买入价格'),
                           Column('sell_price', Float, comment='卖出价格'),
                           extend_existing=True,
                           # autoload=True
                           )
        self.create()
