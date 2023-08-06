import datetime
import time
from abc import ABC
from typing import List
from strategy_api.event.engine import EventEngine, Event
from strategy_api.tm_api.base import BaseGateway
from strategy_api.tm_api.object import TickData, BarData, OrderData, Interval


class StrategyTemplate(ABC):
    author: str = ""

    api_setting = {}

    def __init__(self, gate_way: BaseGateway, symbol: str, interval: Interval, tick_nums: int) -> None:
        self.api: "BaseGateway" = gate_way  # 实例化 Binance api类
        self.api.connect(self.api_setting)  # 链接网关
        time.sleep(5)
        self.api.register_handler(self.process_tick_event, self.process_bar_event, self.process_order_event)
        self.symbol = symbol
        self.interval = interval

        self.tick_times: int = tick_nums
        self.tick_data: List[TickData] = []
        self.init_parameters()

    def process_tick_event(self, event: Event):
        tick: TickData = event.data
        self.on_tick(tick)

    def process_bar_event(self, event: Event):
        bar: BarData = event.data
        self.on_bar(bar)

    def process_order_event(self, event: Event):
        order: OrderData = event.data
        self.on_order(order)

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
