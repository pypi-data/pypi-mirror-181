import numpy as np
import ptrade.component
from ptrade.simulate._trade import _Trade as __Trade


class Simulate(__Trade):
    def __init__(
            self,
            candle: np.array,
            rule: object,
            instId: str = None,
            warn: bool = True,
    ):
        '''
        :param candle: 历史K线数据
        :param rule: 规则
        :param instId: 产品ID
        :param warn: 是否报告警告
        '''
        # 参数与内置模块
        self.candle = candle  # K线数据
        self.rule = rule  # 规则
        self.instId = instId  # 标底
        self.warn = warn
        self._order = ptrade.component.Order(accountMoney=rule.ACCOUNT_MONEY)  # 订单模块
        # 当前K线单位时间内
        self.index = np.nan  # 被遍历的candle行索引
        self.open = np.nan  # 开盘价
        self.low = np.nan  # 最低价
        self.high = np.nan  # 最高价
        self.close = np.nan  # 收盘价
        self.volume = np.nan  # 交易量
        self.ts = np.nan  # 开盘时刻的毫秒级时间戳
        # 当前时刻
        self.datetime = None
        self.date = None
        self.time = None
        # 前一天的数据
        self.last_day_open = np.nan  # 昨日开盘价
        self.last_day_high = np.nan  # 昨日最高价
        self.last_day_low = np.nan  # 昨日最低价
        self.last_day_close = np.nan  # 昨日收盘价

        self.setup()
