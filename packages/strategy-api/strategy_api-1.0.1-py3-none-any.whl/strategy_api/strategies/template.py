import datetime
import time
from abc import ABC
from typing import List
from strategy_api.tm_api.base import BaseGateway
from strategy_api.tm_api.object import TickData, BarData, OrderData, Interval


class StrategyTemplate(ABC):
    author: str = ""

    api_setting = {}

    def __init__(self, gate_way: BaseGateway, symbol: str, interval: Interval, tick_nums: int) -> None:
        self.api: "BaseGateway" = gate_way  # 实例化 Binance api类
        self.api.connect(self.api_setting)  # 链接网关
        time.sleep(5)
        self.api.register_handler(self.on_tick, self.on_bar, self.on_order)
        self.symbol = symbol
        self.interval = interval

        self.tick_times: int = tick_nums
        self.tick_data: List[TickData] = []
        self.init_parameters()

    # 策略参数设置
    def init_parameters(self):
        pass

    # 策略启动时的回调。
    def on_start(self) -> None:
        pass

    # 新的tick数据更新回调。
    def on_tick(self, tick: TickData) -> None:
        self.tick_data.append(tick)
        if len(self.tick_data) > self.tick_times:
            self.tick_data.pop(0)

    # 获取新的最近几秒的tick data
    def get_tick(self, seconds: int) -> List[TickData]:
        now_time = datetime.datetime.now()
        now_time -= datetime.timedelta(seconds=seconds)
        new_data: List[TickData] = []
        for i in self.tick_data:
            if i.datetime >= now_time:
                new_data.append(i)
        return new_data

    # 新的bar数据更新回调。
    def on_bar(self, bar: BarData) -> None:
        # volume = 0.001  # 下单量
        # price = 999  # 下单价格
        # maker = False  # 限价 or 市价
        # stop_loss = False  # 止损
        # stop_profit = False  # 止盈

        # 多头下单
        # self.api.buy(self.parameters['symbol'],
        #              volume=volume,
        #              price=price,
        #              maker=maker,
        #              stop_loss=stop_loss,
        #              stop_profit=stop_profit
        #              )

        # 多头平单
        # self.api.sell(self.parameters['symbol'],
        #              volume=volume,
        #              price=price,
        #              maker=maker,
        #              stop_loss=stop_loss,
        #              stop_profit=stop_profit
        #              )

        # 空头下单
        # self.api.short(self.parameters['symbol'],
        #              volume=volume,
        #              price=price,
        #              maker=maker,
        #              stop_loss=stop_loss,
        #              stop_profit=stop_profit
        #              )

        # 空头平单
        # self.api.cover(self.parameters['symbol'],
        #              volume=volume,
        #              price=price,
        #              maker=maker,
        #              stop_loss=stop_loss,
        #              stop_profit=stop_profit
        #              )

        pass

    # 新订单数据更新回调。
    def on_order(self, order: OrderData) -> None:
        pass

    # 记录数据
    def record_bar(self, bar: BarData):
        pass

    # 数据分析
    def deal_data(self, bar: BarData):
        pass

    def start(self):
        print(f"订阅 合约 {self.symbol} 数据")
        self.api.subscribe(self.symbol, self.interval)
        self.api.subscribe(self.symbol)
