from auto import Strategy, refresh_account, refresh_markets
from notecoin.base.database.oss import oss_upload

# strategy = Strategy()
# strategy.refresh_markets()
# strategy.refresh_account()
# strategy.refresh_data_2hh()
# for key in ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'][::-1]:
#     strategy.update_ohlcv(timeframe=key)

# # strategy.auto_oco()
# strategy.save_ohlcv_to_csv(table='binance_ohlcv_1m')
# strategy.save_ohlcv_to_csv(table='binance_ohlcv_1d')
# strategy.save_ohlcv_to_csv(table='binance_ohlcv_1h')
# #osss_upload("/notechats/data.csv", "/notecoin", tar=True)

refresh_account.delay()
