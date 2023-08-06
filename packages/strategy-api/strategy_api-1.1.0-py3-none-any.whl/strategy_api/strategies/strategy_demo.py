# 策略
import time
import datetime
from strategy_api.strategies.template import StrategyTemplate
from strategy_api.tm_api.Binance.futureUsdt import BinanceFutureUsdtGateway
from strategy_api.tm_api.object import Interval, BarData, OrderData, Status


# 策略类
class StrategyDemo(StrategyTemplate):
    # 属性 作者(标志该策略的开发人员)
    author = "DYX"

    # 属性 设置链接网关需要的参数参数
    api_setting = {
        "key": "",
        "secret": "",
        "proxy_host": "127.0.0.1",
        "proxy_port": 8010,
    }

    # 初始化方法
    def __init__(self, gate_way, symbol: str, interval: Interval, tick_nums: int):
        super(StrategyDemo, self).__init__(gate_way, symbol, interval, tick_nums)

    # 初始化策略参数
    def init_parameters(self):
        # 是否下单
        self.is_order = False
        # 下单量
        self.order_value = 0.001
        # 下单时间
        self.current: datetime = None

        # 下单的订单号
        self.buy_order_id = ""
        # 记录止盈的订单号
        self.buy_profit_order_id = ""
        # 记录止损的订单号
        self.buy_loss_order_id = ""

        # 止盈止损比例
        self.profit_num, self.loss_num = 0.0005, 0.0005

        # 止盈止损价格
        self.profit_price, self.loss_price = 0, 0

    # k 线数据的回调, 可以在该方法里面记录 k 线数据、分析k线数据
    def on_bar(self, bar: BarData):
        # 记录数据
        self.record_bar(bar)

        # 分析处理数据
        self.deal_data(bar)

    def deal_data(self, bar):
        if not self.is_order:
            self.is_order = True
            # 下单方法自带一个返回值，返回值为自定义的订单号
            self.buy_order_id = self.api.buy(self.symbol, volume=self.order_value, price=0,
                                             maker=False, stop_loss=False, stop_profit=False)

            # 记录交易时间
            current = bar.endTime + datetime.timedelta(minutes=1)
            self.current = current.replace(second=0, microsecond=0)
            print("暂停3秒，等待最新交易价的收集")
            time.sleep(0.5)

    # 计算 止盈止损
    def calculate_profit_loss(self, order_time: datetime):
        tick = self.get_tick(30)
        tick_data = None
        for i in tick:
            if i.datetime >= order_time:
                tick_data = i
                break
        self.profit_price = round(tick_data.last_price * (self.profit_num + 1), 1)
        self.loss_price = round(tick_data.last_price * (1 - self.loss_num),
                                1)  # tick 数据的回调, 可以在该方法里面记录 tick 数据、分析 tick 数据

        print("当前分钟最新tick: {}".format(tick_data))
        print("止盈价: {}".format(self.profit_price))
        print("止损价: {}".format(self.loss_price))

    # 订单 数据的回调，订单状态的改变都会通过websoket 推送到这里，例如 从提交状态 改为 全成交状态，或者提交状态 改为 撤销状态 都会推送
    # 可以在这里对仓位进行一个记录
    def on_order(self, order: OrderData):
        if order.orderid == self.buy_order_id and order.status == Status.ALLTRADED:
            print("当前订单已全部成交，接下来下止盈止损单")
            self.calculate_profit_loss(self.current)  # 计算止盈止损

            self.buy_profit_order_id = self.api.sell(self.symbol,
                                                     volume=self.order_value,
                                                     price=self.profit_price,
                                                     maker=False,
                                                     stop_profit=True,
                                                     stop_loss=False
                                                     )
            self.buy_loss_order_id = self.api.sell(self.symbol,
                                                   volume=self.order_value,
                                                   price=self.loss_price,
                                                   maker=False,
                                                   stop_profit=False,
                                                   stop_loss=True
                                                   )
            self.buy_order_id = ""

        elif (order.orderid == self.buy_loss_order_id or order.orderid == self.buy_profit_order_id) and \
                order.status == Status.ALLTRADED:
            self.is_order = False
            if order.orderid == self.buy_loss_order_id:
                print("止损了")
                # 撤销止盈单
                self.api.cancel_order(self.buy_profit_order_id, self.symbol)
            elif order.orderid == self.buy_profit_order_id:
                print("止盈了")
                # 撤销止损单
                self.api.cancel_order(self.buy_loss_order_id, self.symbol)


def start_strategy():
    s = StrategyDemo(gate_way=BinanceFutureUsdtGateway(), symbol="BTCUSDT", interval=Interval.MINUTE, tick_nums=200)
    s.start()
    print("策略运行中")
    while True:
        time.sleep(10)


if __name__ == '__main__':
    print("启动量化系统: 等待策略运行")
    start_strategy()
