from abc import ABC
from typing import Dict, Any, List
from strategy_api.event.engine import EVENT_TICK, EVENT_BAR, EVENT_ORDER
from strategy_api.event.engine import EventEngine, Event
from strategy_api.tm_api.object import OrderData, BarData, TickData, Interval, OrderRequest, HistoryRequest


class BaseGateway(ABC):
    # Default name for the gateway.
    default_setting: Dict[str, Any] = {}

    def __init__(self) -> None:
        self.event_engine: EventEngine = EventEngine()
        self.event_engine.start()

    def register_handler(self, tick_handler: callable, bar_handler: callable, order_handler: callable):
        self.event_engine.register(EVENT_TICK, tick_handler)
        self.event_engine.register(EVENT_BAR, bar_handler)
        self.event_engine.register(EVENT_ORDER, order_handler)

    def connect(self, setting: dict) -> None:
        pass

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

    def query_history(self, symbol: str, interval: Interval, hour: int = 0, minutes: int = 0) -> List[BarData]:
        pass

    def subscribe(self, symbol: str, interval: Interval = None) -> None:
        pass

    # 一般事件推送。
    def on_event(self, type: str, data: Any = None) -> None:
        event: Event = Event(type, data)
        self.event_engine.put(event)

    # tick 数据推送
    def on_tick(self, tick: TickData) -> None:
        self.on_event(EVENT_TICK, tick)

    # K线数据回调
    def on_bar(self, bar: BarData):
        self.on_event(EVENT_BAR, bar)

    # 定单事件推送
    def on_order(self, order: OrderData) -> None:
        self.on_event(EVENT_ORDER, order)

    def close(self) -> None:
        pass
