from abc import ABC
from typing import Dict, Any, List

from strategy_api.tm_api.object import OrderData, BarData, TickData, Interval, OrderRequest, HistoryRequest


class BaseGateway(ABC):

    # Default name for the gateway.
    default_setting: Dict[str, Any] = {}

    def __init__(self) -> None:
        pass

    def connect(self, setting: dict) -> None:
        pass

    def register_handler(self, tick_handler: callable, bar_handler: callable, order_handler: callable):
        self.on_tick_handler = tick_handler
        self.on_bar_handler = bar_handler
        self.on_order_handler = order_handler

    def buy(self,
            symbol: str,
            volume: float,  # 数量
            price: float = 0,  # 价格
            maker: bool = False,  # 限价单
            stop_loss: bool = False,  # 止损
            stop_profit: bool = False,  # 止盈
            ) -> str:
        pass

    def sell(self,
             symbol: str,
             volume: float,  # 数量
             price: float = 0,  # 价格
             maker: bool = False,  # 限价单
             stop_loss: bool = False,  # 止损
             stop_profit: bool = False,  # 止盈
             ) -> str:
        pass

    def short(self,
              symbol: str,
              volume: float,  # 数量
              price: float = 0,  # 价格
              maker: bool = False,  # 限价单
              stop_loss: bool = False,  # 止损
              stop_profit: bool = False,  # 止盈
              ) -> str:
        pass

    def cover(self,
              symbol: str,
              volume: float,  # 数量
              price: float = 0,  # 价格
              maker: bool = False,  # 限价单
              stop_loss: bool = False,  # 止损
              stop_profit: bool = False,  # 止盈
              ) -> str:
        pass

    def send_order(self, req: OrderRequest) -> str:
        pass

    def cancel_order(self, orderid: str, symbol: str) -> None:
        pass

    def query_history(self, symbol: str, hour: int, interval: Interval) -> List[BarData]:
        pass

    def subscribe(self, symbol: str, interval: Interval = None) -> None:
        pass

    def on_tick(self, tick: TickData):
        pass

    def on_bar(self, bar: BarData):
        pass

    def on_order(self, order: OrderData):
        pass

    def close(self) -> None:
        pass