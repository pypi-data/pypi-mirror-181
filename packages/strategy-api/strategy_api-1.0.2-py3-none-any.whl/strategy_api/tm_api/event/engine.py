# -*- coding:utf-8 -*-
# @Date: 2022-11-01
# @author: 邓大大
# @Desc: winTrader 框架的事件驱动框架。
# @Notice: 事件引擎开始后, 默认启动了一个 计时器
from collections import defaultdict
from queue import Empty, Queue
from threading import Thread
import time
from typing import Any, Callable, List

EVENT_TIMER = "eTimer"


# 事件对象
# 由使用的类型字符串组成,通过事件引擎分发事件，以及一个数据
class Event:

    def __init__(self, type: str, data: Any = None) -> None:
        """"""
        self.type: str = type
        self.data: Any = data


# 定义要在事件引擎中使用的处理函数。
HandlerType: callable = Callable[[Event], None]


# 事件引擎
# 1、根据其类型分发事件对象给那些注册的处理程序。
# 2、它还按间隔秒生成计时器事件，可用于计时目的： 定时器事件默认每 1 秒生成一次，如果未指定间隔。
class EventEngine:

    def __init__(self, interval: int = 1) -> None:
        self._interval: int = interval
        self._queue: Queue = Queue()
        self._active: bool = False
        self._thread: Thread = Thread(target=self._run)
        self._timer: Thread = Thread(target=self._run_timer)
        self._handlers: defaultdict = defaultdict(list)  # 特殊方法对应不同事件类型
        self._general_handlers: List = []  # 一般方法对应所有事件类型

    # 从队列中获取事件然后处理它。
    def _run(self) -> None:
        while self._active:
            try:
                event: Event = self._queue.get(block=True, timeout=1)
                self._process(event)
            except Empty:
                pass

    # 首先将事件分发给那些注册监听的处理程序到这种类型。
    # 然后将事件分发给那些监听的通用处理程序到所有类型。
    def _process(self, event: Event) -> None:
        if event.type in self._handlers:
            # 注册的每个方法都一次处理该对象
            [handler(event) for handler in self._handlers[event.type]]
        if self._general_handlers:
            [handler(event) for handler in self._general_handlers]

    # 定时事件put
    def _run_timer(self) -> None:
        while self._active:
            time.sleep(self._interval)
            event: Event = Event(EVENT_TIMER)
            self.put(event)

    # 开始事件引擎
    def start(self):
        self._active = True
        self._thread.start()
        self._timer.start()

    # 停止事件引擎
    def stop(self):
        self._active = False
        self._thread.join()
        self._timer.join()

    # 事件对象加入到事件队列中待处理
    def put(self, event: Event) -> None:
        self._queue.put(event)

    # 事件注册
    def register(self, type: str, handler: HandlerType) -> None:
        handler_list: list = self._handlers[type]
        if handler not in handler_list:
            handler_list.append(handler)

    # 事件注销
    def unregister(self, type: str, handler: HandlerType) -> None:
        handler_list: list = self._handlers[type]

        if handler in handler_list:
            handler_list.remove(handler)

        if not handler_list:
            self._handlers.pop(type)

    # 一般事件方法注册
    def register_general(self, handler: HandlerType):
        if handler not in self._general_handlers:
            self._general_handlers.append(handler)

    # 一般事件方法注销
    def unregister_general(self, handler: HandlerType):
        if handler in self._general_handlers:
            self._general_handlers.remove(handler)
