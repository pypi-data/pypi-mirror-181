'''
记录数据：
属性                 类型         说明
index               int         被遍历的candle行索引
open                float       开盘价（以时间粒度为单位，如bar='1m'，open为每分钟的开盘价格）
low                 float       最低价
high                float       最高价
close               float       收盘价
volume              float       交易量
ts                  float       开盘时刻的毫秒时间戳

datetime            datetime    当前日期时间
date                date        当前日期
time                time        当前时间

this_day_open       float       今日开盘价
this_day_open_ts    float       今日开盘毫秒时间戳

last_day_open       float       昨日开盘价
last_day_high       float       昨日最高价
last_day_low        float       昨日最低价
last_day_close      float       昨日收盘价
last_day_volume     float       昨日成交量
last_day_open_ts    float       昨日开盘毫秒时间戳

last_day_candle     np.array    昨日K线数据
'''

import datetime
import numpy as np
import paux.order
import paux.date
import paux.candle.transform
from ptrade.simulate._property import _Property


class _Record(_Property):
    # 当前K线单位时间内
    index: int  # 被遍历的candle行索引
    open = float  # 开盘价（以时间粒度为单位，如bar='1m'，open为每分钟的开盘价格）
    low = float  # 最低价
    high = float  # 最高价
    close = float  # 收盘价
    volume = float  # 交易量
    ts: float  # 开盘时刻的毫秒时间戳
    # 当前时刻
    datetime: datetime.datetime  # 当前日期时间
    date: datetime.date  # 当前日期
    time: datetime.time  # 当前时间
    # 当天数据
    this_day_open: float  # 今日开盘价
    this_day_open_ts: float  # 今日开盘毫秒时间戳
    # 前一天的数据
    last_day_open: float  # 昨日开盘价
    last_day_high: float  # 昨日最高价
    last_day_low: float  # 昨日最低价
    last_day_close: float  # 昨日收盘价
    last_day_volume: float  # 昨日成交额
    last_day_open_ts: float  # 昨日开盘毫秒时间戳

    # 记录数据
    def record(self):
        '''
        更新:
        1. 每个时刻的价格数据
        2. 每日开盘价
        3. 昨日的开盘、最高、最低与收盘价
        '''
        # 当前颗粒度中的数据
        self.ts = self.candle[self.index, 0]  # 开盘时刻毫秒级时间戳
        self.open = self.candle[self.index, 1]  # 开盘价
        self.high = self.candle[self.index, 2]  # 最高价
        self.low = self.candle[self.index, 3]  # 最低价
        self.close = self.candle[self.index, 4]  # 收盘价
        self.volume = self.candle[self.index, 5]  # 交易量
        # 当前日期时间
        self.datetime = paux.date.to_datetime(
            date=self.ts,
            timezone=self.rule.TIMEZONE,
        )
        # 当前日期
        self.date = self.datetime.date()
        # 当前时间
        self.time = self.datetime.time()

        if not hasattr(self, 'last_date'):
            self.__last_date = self.date
            self.last_date = None
            self.last_day_open = np.nan  # 昨日开盘价
            self.last_day_high = np.nan  # 昨日最高价
            self.last_day_low = np.nan  # 昨日最低价
            self.last_day_close = np.nan  # 昨日收盘价
            self.last_day_volume = np.nan  # 昨日成交额

        if self.date != self.__last_date:
            self.last_date = self.__last_date
            self.__last_date = self.date
            self.this_day_open = self.open  # 今日开盘价
            self.this_day_open_ts = self.ts  # 今日开盘毫秒时间戳
            # 昨日开盘毫秒时间戳
            self.last_day_open_ts = paux.date.to_ts(
                date=self.last_date,
                timezone=self.rule.TIMEZONE,
            )
            # 昨日历史K线
            self.last_day_candle = self.candle[
                (self.candle[:, 0] >= self.last_day_open_ts) & (self.candle[:, 0] < self.this_day_open_ts)
                ]
            self.last_day_open = self.last_day_candle[0, 1]  # 昨日开盘价
            self.last_day_high = self.last_day_candle[:, 2].max()  # 昨日最高价
            self.last_day_low = self.last_day_candle[:, 3].min()  # 昨日最低价
            self.last_day_close = self.last_day_candle[:, 4]  # 昨日收盘价
            self.last_day_volume = self.last_day_candle[:, 5].sum()  # 昨日成交额
