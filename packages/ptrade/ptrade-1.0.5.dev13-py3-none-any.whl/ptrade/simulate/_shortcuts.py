'''
1. 可以重写的函数：

1.1 init后执行的方法
setup()

1.2 买入策略
buy()
    return None # 结束函数
    yield self.start_orderData(...) # 开仓

1.3 卖出策略
sell()
    return None # 结束函数
    yield self.close_orderData(...) # 平仓


2. 可以调用的函数
2.1 开仓
start_orderData(
    self,
    buyLine: Union[int, float],
    posSide: Literal['long', 'short'],
    buyMoney: Union[int, float,Literal['rule']] = 'rule',
    buyCommissionRate: Union[int, float, Literal['rule']] = 'rule',
    lever: Union[int, Literal['rule']] = 'rule',
    tpRate: Union[int, float, Literal['rule']] = 'rule',
    tpLine: Union[int, float, None] = None,
    slRate: Union[int, float, Literal['rule']] = 'rule',
    slLine: Union[int, float, None] = None,
    orderType: str = None,
    toMode: Literal['isolated', 'cross'] = 'isolated',
    priority=100,
    **kwargs
)

参数                 类型             说明
buyLine             int|float       开仓价格
posSide             str             持仓方向，多仓：long 空仓：short
buyMoney            int|float|str   开仓金额，默认值：rule
buyCommissionRate   int|float|str   开仓手续费率，默认值：rule
lever               int|str         杠杆
tpRate              int|float|str   止盈率，默认值：rule
tpLine              int|float|None  止盈价格，默认值为None，tpLine与tpRate同时存在，优先级：tpLine >>> tpRate
slRate              int|float|str   止损率，默认值：rule
slLine              int|float|None  止损价格，默认值为None，slLine与slRate同时存在，优先级：slLine >>> slRate
smLine              int|float|None  爆仓价格，默认值为None，逐仓的爆仓价格会自动算出，无需填写，全仓的爆仓价格需要用户指定，否则不会考虑全仓爆仓
orderType           str             订单类型，默认值：''
toMode              str             持仓类型，全仓：cross 逐仓：isolated
priority            int             订单优先级（用于订单任务调度排序，默认值：100）

2.2 平仓
close_orderData(
    self,
    orderData: dict,
    sellLine: Union[int, float],
    sellCommissionRate: Union[int, float, Literal['rule']] = 'rule',
    endType: object = None,
    priority=50,
    **kwargs
)
参数                     类型             说明
orderData               dict            待平仓的持仓订单
sellLine                int|float       平仓价格
sellCommissionRate      int|float|str   平仓手续费率，默认值：rule
endType                 str             平仓类型，用户调用平仓：CS 止盈：TP 止损：SL 爆仓：SM 按照时间段卖出：PT 超过最大持仓时间：TT 模拟交易后以市场价平仓：MT
priority                int             订单优先级（用于订单任务调度排序，默认值：50）
'''

from typing import Union, Literal
from copy import deepcopy
import uuid
import numpy as np
import paux.order
import paux.date
import paux.candle.transform
import paux.order
from ptrade import exception
from ptrade.simulate._record import _Record


class _ShortCuts(_Record):

    # 用户重写 --------------------------------------------------------------------------------------------
    # init后执行的方法
    def setup(self):
        # to overwrite
        pass

    # 买入策略
    def buy(self):
        # to overwrite
        pass

    # 卖出策略
    def sell(self):
        pass

    # 获取近期指定数量的历史K线数据
    def get_latest_candle(self, length: int, include_now: bool = False):
        '''
        :param length: 长度
        :param include_now: 是否包含当前时刻
        '''
        start_index = self.index - length
        end_index = self.index
        if include_now:
            start_index += 1
            end_index += 1
        return self.candle[start_index:end_index]

    # 获取当天的历史K线数据
    def get_today_candle(self, include_now: bool = False):
        '''
        :param include_now:  是否包含当前时刻
        '''
        this_day_open_ts = paux.date.to_ts(date=self.date, timezone=self.rule.TIMEZONE)
        end_ts = self.datetime.timestamp() * 1000
        if not include_now:
            end_ts -= 1
        return self.candle[
            (self.candle[:, 0] >= this_day_open_ts) & (self.candle[:, 0] <= end_ts)
            ]

    # 开仓订单---------------------------------------------------------------------------------------------
    def start_orderData(
            self,
            buyLine: Union[int, float],
            posSide: Literal['long', 'short'],
            buyMoney: Union[int, float, Literal['rule']] = 'rule',
            buyCommissionRate: Union[int, float, Literal['rule']] = 'rule',
            lever: Union[int, Literal['rule']] = 'rule',
            tpRate: Union[int, float, Literal['rule']] = 'rule',
            tpLine: Union[int, float, None] = None,
            slRate: Union[int, float, Literal['rule']] = 'rule',
            slLine: Union[int, float, None] = None,
            orderType: str = '',
            toMode: Literal['isolated', 'cross'] = 'isolated',
            priority=50,
            **kwargs
    ):
        '''
        发起订单
        字段                 类型             说明
        buyLine             int|float       开仓价格
        posSide             str             持仓方向，多仓：long 空仓：short
        buyMoney            int|float|str   开仓金额，默认值：rule
        buyCommissionRate   int|float|str   开仓手续费率，默认值：rule
        lever               int|str         杠杆
        tpRate              int|float|str   止盈率，默认值：rule
        tpLine              int|float|None  止盈价格，默认值为None，tpLine与tpRate同时存在，优先级：tpLine >>> tpRate
        slRate              int|float|str   止损率，默认值：rule
        slLine              int|float|None  止损价格，默认值为None，slLine与slRate同时存在，优先级：slLine >>> slRate
        smLine              int|float|None  爆仓价格，默认值为None，逐仓的爆仓价格会自动算出，无需填写，全仓的爆仓价格需要用户指定，否则不会考虑全仓爆仓
        orderType           str             订单类型，默认值：''
        toMode              str             持仓类型，全仓：cross 逐仓：isolated
        priority            int             订单优先级（用于订单任务调度排序，默认值：100）

        随机生成32位长度的orderId
        '''
        orderId = uuid.uuid4().hex[0:32]
        # 杠杆
        if lever == 'rule':
            if posSide == 'long':
                lever = self.rule.LONG_LEVER
            elif posSide == 'short':
                lever = self.rule.SHORT_LEVER
            else:
                raise exception.PosSideParamError(posSide)
        # 止盈率
        if tpRate == 'rule':
            if posSide == 'long':
                tpRate = self.rule.LONG_TP_RATE
            elif posSide == 'short':
                tpRate = self.rule.SHORT_TP_RATE
        # 止损率
        if slRate == 'rule':
            if posSide == 'long':
                slRate = self.rule.LONG_SL_RATE
            elif posSide == 'short':
                slRate = self.rule.SHORT_SL_RATE
        # 当前订单的candle行索引
        orderIndex = self.index
        # 开仓价格，修正价格属于最小值和最大值之间
        buyLine = paux.order.round_simulate(np.clip(buyLine, self.low, self.high))
        # 开仓手续费率
        if buyCommissionRate == 'rule':
            buyCommissionRate = self.rule.BUY_COMMISSION_RATE
        # 如果没有buyMoney
        if buyMoney == 'rule':
            if self.rule.BUY_MONEY_RATE:
                buyMoney = np.clip(
                    (self.positionAccountMoney + self.accountMoney) * self.rule.BUY_COMMISSION_RATE,
                    0, self.accountMoney
                )
            else:
                buyMoney = self.rule.BUY_MONEY

        return self._order.start_orderData(
            orderId=orderId,  # 订单ID
            orderType=orderType,  # 订单类型
            instId=self.instId,  # 产品ID
            lever=lever,  # 杠杆
            toMode=toMode,  # 持仓类型
            posSide=posSide,  # 持仓方向
            buyMoney=buyMoney,  # 开仓金额
            orderDatetime=self.datetime.strftime('%Y-%m-%d %H:%M:%S'),  # 开仓日期时间
            buyLine=buyLine,  # 开仓价格
            buyCommissionRate=buyCommissionRate,  # 开仓手续费率
            tpLine=tpLine,  # 止盈率
            tpRate=tpRate,  # 止盈价格
            slLine=slLine,  # 止损率
            slRate=slRate,  # 止损价格
            smLine=None,  # 爆仓价格
            orderTs=self.ts,  # 补充字段
            orderIndex=orderIndex,  # 补充字段
            priority=priority,  # 优先级
            **kwargs,
        )

    # 平仓订单---------------------------------------------------------------------------------------------
    def close_orderData(
            self,
            orderData: dict,
            sellLine: Union[int, float],
            sellCommissionRate: Union[int, float, Literal['rule']] = 'rule',
            endType: str = 'CS',
            priority=100,
            **kwargs
    ):
        '''
        结束订单
        orderData               dict            待平仓的持仓订单
        sellLine                int|float       平仓价格
        sellCommissionRate      int|float|str   平仓手续费率，默认值：rule
        endType                 str             平仓类型，用户调用平仓：CS 止盈：TP 止损：SL 爆仓：SM 按照时间段卖出：PT 超过最大持仓时间：TT 模拟交易后以市场价平仓：MT
        priority                int             订单优先级（用于订单任务调度排序，默认值：50）

        辅助字段：
            endIndex        int         平仓时刻的candle索引
            endTs           float       平仓时刻的毫秒时间戳
        通过计算产生的字段：
            commission      int|float   手续费
            holdMinute      int         持仓时间（分钟）
            sellMoney       int|float   平仓后得到的金额（以考虑手续费）
            profitRate      int|float   利润率
            profit          int|float   利润
        补充的过程数据：
            hh              int|float   持仓过程中的最高价格
            hhRate          int|float   持仓过程中的最高价格相对于开仓价格的上涨百分比
            hh              int|float   持仓过程中的最低价格
            hhRate          int|float   持仓过程中的最低价格相对于开仓价格的下跌百分比
        '''
        orderData = deepcopy(orderData)
        # 手续费
        if sellCommissionRate == 'rule':
            sellCommissionRate = self.rule.SELL_COMMISSION_RATE
        # 开始与终止索引
        endIndex = self.index
        orderIndex = orderData['orderIndex']
        # 过程中的最高价与最低价
        if orderIndex != endIndex:
            hh = self.candle[orderIndex:endIndex, 2].max()
            ll = self.candle[orderIndex:endIndex, 3].min()
        else:
            hh = self.candle[endIndex, 2]
            ll = self.candle[endIndex, 3]
        # 最高价与最低价相对于buyLine的增长下跌比例
        hhRate = round((hh - orderData['buyLine']) / orderData['buyLine'], 4)
        llRate = round((ll - orderData['buyLine']) / orderData['buyLine'], 4)
        # 平仓
        return self._order.close_orderData(
            orderData=orderData,  # 待平仓的持仓订单
            sellLine=sellLine,  # 平仓价格
            endDatetime=self.datetime.strftime('%Y-%m-%d %H:%M:%S'),  # 平仓日期时间
            sellCommissionRate=sellCommissionRate,  # 平仓手续费率
            endType=endType,  # 平仓类型
            # 补充的字段
            endIndex=endIndex,  # 平仓时刻的candle索引
            endTs=self.ts,  ## 平仓时刻的毫秒时间戳
            hh=hh,  # 持仓过程中的最高价格
            hhRate=hhRate,  # 持仓过程中的最高价格相对于开仓价格的上涨百分比
            ll=ll,  # 持仓过程中的最低价格
            llRate=llRate,  # 持仓过程中的最低价格相对于开仓价格的下跌百分比
            priority=priority,  # 订单优先级
            **kwargs
        )
