from strategy_api.tm_api.Binance.futureUsdt import BinanceFutureUsdtGateway
from strategy_api.tm_api.object import Interval

api_setting = {
    "key": "",
    "secret": "",
    "proxy_host": "127.0.0.1",
    "proxy_port": 8010,
}

api = BinanceFutureUsdtGateway()

# 链接api
api.connect(api_setting)

# 订阅 1 分钟 K 线 行情
api.subscribe(symbol="BTCUSDT", interval=Interval.MINUTE)

# 订阅 tick 行情
api.subscribe(symbol="BTCUSDT")

# 下单
api.buy(symbol="BTCUSDT", volume=0.01, price=9999, maker=True, stop_loss=False, stop_profit=False)

# 撤销订单
api.cancel_order(orderid="xl_1111111", symbol="BTCUSDT")

