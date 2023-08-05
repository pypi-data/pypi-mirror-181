'''
交易过程：

tpSell_and_slThrow      止盈止损卖出（优先止损）
smThrow                 爆仓
periodThrow             在抛出时间段卖出
timeoutThrow            超过最大持仓时间卖出
marketThrow             以市场价卖出

run                     运行计算
'''

from typing import Union
import datetime
import warnings
import paux.order
import paux.date
import paux.candle.transform
import paux.order
from ptrade import component
from ptrade import exception
from ptrade.simulate._shortcuts import _ShortCuts


class _Trade(_ShortCuts):
    # 仓位不足，是否发送警告
    warn: bool

    PRIORITY = {
        'periodThrow': 250,  # 在抛出时间段平仓
        'timeoutThrow': 200,  # 超过最大持仓时间平仓
        'smThrow': 150,  # 爆仓
        'slThrow': 125,  # 止损平仓
        # 'sell': 100,  # 用户自定义卖出
        'tpSell': 25,  # 止盈平仓
        'marketThrow': 0,  # 以收盘市场价平仓
        # 'buy': 50,  # 用户自定义买入
    }

    # 多种平仓方式---------------------------------------------------------------------------------------------
    # 止盈止损平仓
    def tpSell_and_slThrow(self):
        '''
        止盈或止损平仓
            悲观策略：如果单位时间内价格剧烈波动，同时达到止盈与止损条件，以止损价格抛出
            止盈价格与止损价格并不一定是实际的卖出价格
            止盈卖出：endType = 'TP'
            止损抛出：endType = 'SL'
        '''
        # 过滤非平仓时间
        if not paux.date.is_period_allowed(
                date=self.time,
                periods=self.rule.SELL_PERIODS,
                timezone=self.rule.TIMEZONE,
        ):
            return None
        # 止盈卖出与止损抛出
        for orderData in self.currentOrderDatasCanBeTraded:
            posSide = orderData['posSide']
            # 如果达到了止损条件
            # 多单：最小价<=止损价格；空单：最大价格>=止损价格
            if orderData['slLine'] and (
                    (posSide == 'long' and self.low <= orderData['slLine']) or
                    (posSide == 'short' and self.high >= orderData['slLine'])):
                # 多单实际止损价格
                if posSide == 'long':
                    realSlLine = min(self.open, orderData['slLine'])
                # 空单实际止损价格
                elif posSide == 'short':
                    realSlLine = max(self.open, orderData['slLine'])
                else:
                    raise exception.PosSideParamError(posSide)
                priority = self.PRIORITY['slThrow']  # 止损平仓优先级，默认125
                # 平仓
                orderData = self.close_orderData(
                    orderData=orderData,
                    sellLine=realSlLine,
                    endType='SL',
                    priority=priority,
                )
                yield orderData
                continue
            # 未达成止损条件，观测是否达到止盈条件
            # 多单：最高价>=止盈价格；空单：最低价<=止盈价格
            if orderData['tpLine'] and (
                    (posSide == 'long' and self.high >= orderData['tpLine']) or
                    (posSide == 'short' and self.low <= orderData['tpLine'])):
                # 多单实际止盈价格
                if posSide == 'long':
                    realTpLine = max(self.open, orderData['tpLine'])
                # 空单实际止盈价格
                elif posSide == 'short':
                    realTpLine = min(self.open, orderData['tpLine'])
                else:
                    raise exception.PosSideParamError(posSide)
                # 平仓
                priority = self.PRIORITY['tpSell']  # 止盈平仓优先级，默认50
                orderData = self.close_orderData(
                    orderData=orderData,
                    sellLine=realTpLine,
                    endType='TP',
                    priority=priority,
                )
                yield orderData
                continue

    # 爆仓
    def smThrow(self):
        '''
        逐仓会自动计算出强制平仓价格
        全仓需要用户手动设置smLine
        endType = 'SM'
        '''
        priority = self.PRIORITY['smThrow']  # 爆仓优先级，默认150
        for orderData in self.currentOrderDatasCanBeTraded:
            if (orderData['posSide'] == 'long' and self.low <= orderData['smLine'] or
                    orderData['posSide'] == 'short' and self.high >= orderData['smLine']):
                yield self.close_orderData(
                    orderData=orderData,
                    sellLine=orderData['smLine'],
                    endType='SM',
                    priority=priority,
                )

    # 在抛出时间段平仓
    def periodThrow(self):
        '''
        时间段满足要求，则全部平仓
        endType = 'PT'
        '''
        priority = self.PRIORITY['periodThrow']  # 在抛出时间段平仓，默认250
        # 是否满足时间段要求
        if not paux.date.is_period_allowed(
                date=self.time,
                periods=self.rule.THROW_PERIODS,
                timezone=self.rule.TIMEZONE,
        ):
            return None
        # 全部持仓以市价平掉
        for orderData in self.currentOrderDatasCanBeTraded:
            orderData = self.close_orderData(
                orderData=orderData,
                sellLine=self.open,
                endType='PT',
                priority=priority,
            )
            yield orderData

    # 超过最大持仓时间平仓
    def timeoutThrow(self):
        '''
        持仓时间超时，以市价平仓
        endType = 'TT'
        '''
        priority = self.PRIORITY['timeoutThrow']  # 超过最大持仓时间平仓，默认200
        # 时间段是否允许卖出
        if not paux.date.is_period_allowed(
                date=self.time,
                periods=self.rule.SELL_PERIODS,
                timezone=self.rule.TIMEZONE,
        ):
            return None
        # 无最大持仓时间限制
        if not self.rule.MAX_HOLD_ORDER_MINUTE:
            return None
        # 遍历全部持仓订单
        for orderData in self.currentOrderDatasCanBeTraded:
            # 持仓时间超过了预设最大时间
            if ((self.ts - orderData['orderTs']) / 60000) >= self.rule.MAX_HOLD_ORDER_MINUTE:
                orderData = self.close_orderData(
                    orderData=orderData,
                    sellLine=self.open,
                    endType='TT',
                    priority=priority,
                )
                yield orderData

    # 以收盘市场价平仓
    def marketThrow(self, orderDatas):
        '''
        :param orderDatas:市价平仓的订单
        endType = 'MT'
        '''
        priority = self.PRIORITY['marketThrow']  # 以收盘市场价平仓，默认0
        if orderDatas:
            for orderData in orderDatas:
                orderData = self.close_orderData(
                    orderData=orderData,
                    sellLine=self.close,
                    endType='MT',
                    priority=priority,
                )
                yield orderData

    # 运行计算---------------------------------------------------------------------------------------------
    def run(
            self,
            start: Union[datetime.date, int, float, str, None] = None,
            end: Union[datetime.date, int, float, str, None] = None,
            clear: bool = True,
    ):
        '''
        :param start: 执行模拟交易的起始日期时间
        :param end: 执行模拟交易的终止日期时间
        :param clear: 是否在遍历后的最后时刻市价平掉全部仓位
        优先级：periodThrow > timeoutThrow > smThrow >  slThrow > tpSell > sell > buy
        '''

        # 起始索引与终止索引
        start_index = paux.candle.transform.get_candle_index_by_date(
            candle=self.candle,
            date=start,
            default=0
        )
        # 终止索引
        end_index = paux.candle.transform.get_candle_index_by_date(
            candle=self.candle,
            date=end,
            default=self.candle.shape[0]
        )
        for index in range(start_index, end_index):
            # 更新数据
            self.index = index
            self.record()
            # 时间段抛出
            periodThrow = self.periodThrow()
            periodThrowDatas = [orderData for orderData in periodThrow if periodThrow]
            # 超时抛出
            timeoutThrow = self.timeoutThrow()
            timeoutThrowDatas = [orderData for orderData in timeoutThrow if timeoutThrow]
            # 爆仓强平
            smThrow = self.smThrow()
            smThrowDatas = [orderData for orderData in smThrow if smThrow]
            # 止盈卖出与止损抛出
            tpSell_and_slThrow = self.tpSell_and_slThrow()
            tpSell_and_slThrowDatas = [orderData for orderData in tpSell_and_slThrow if tpSell_and_slThrow]

            # 自定义卖出
            if paux.date.is_period_allowed(
                    date=self.time,
                    periods=self.rule.SELL_PERIODS,
                    timezone=self.rule.TIMEZONE,
            ):
                sell = self.sell()
                if sell:
                    sellDatas = [orderData for orderData in sell if sell]
                else:
                    sellDatas = []
            else:
                sellDatas = []
            # 自定义买入
            if paux.date.is_period_allowed(
                    date=self.time,
                    periods=self.rule.BUY_PERIODS,
                    timezone=self.rule.TIMEZONE,
            ) and not paux.date.is_period_allowed(
                date=self.time,
                periods=self.rule.THROW_PERIODS,
                timezone=self.rule.TIMEZONE
            ):
                buy = self.buy()
                if buy:
                    buyDatas = [orderData for orderData in buy]
                else:
                    buyDatas = []
            else:
                buyDatas = []
            # 订单排序
            totalOrderDatas = periodThrowDatas + timeoutThrowDatas + smThrowDatas + tpSell_and_slThrowDatas + sellDatas + buyDatas
            totalOrderDatas = sorted(totalOrderDatas, key=lambda d: d['priority'], reverse=True)

            for orderData in totalOrderDatas:
                # 购买订单
                if orderData['sellLine'] == None:
                    self.__to_currentOrderDatas(orderData)
                else:
                    self._order.to_historyOrderDatas(orderDatas=[orderData, ])
        # 未成交订单强平
        if clear:
            marketThrow = self.marketThrow(orderDatas=self._order.currentOrderDatas)
            if marketThrow:
                marketThrowOrderDatas = [orderData for orderData in marketThrow]
            else:
                marketThrowOrderDatas = []

            self._order.to_historyOrderDatas(
                marketThrowOrderDatas
            )
        self.analysis = component.Analysis(historyOrderDatas=self.historyOrderDatas)

    # 根据条件判断是否满足进入持仓
    def __to_currentOrderDatas(self, orderData):

        if self.longPositionLeft == 0 and self.shortPositionLeft == 0:
            return None
        if self.longPositionLeft < 0 or self.shortPositionLeft < 0:
            msg = f'longPositionLeft = {self.longPositionLeft},shortPositionLeft={self.shortPositionLeft}'
            raise exception.TraderError(msg=msg)
        if orderData['posSide'] == 'long':
            if self.longPositionLeft > 0:
                self._order.to_currentOrderDatas(orderDatas=[orderData, ])
            else:
                if self.warn:
                    msg = '多仓仓位不足，orderData无法开仓,orderData={orderData}'.format(orderData=str(orderData))
                    warnings.warn(msg)
        elif orderData['posSide'] == 'short':
            if self.shortPositionLeft > 0:
                self._order.to_currentOrderDatas(orderDatas=[orderData, ])
            else:
                if self.warn:
                    msg = '空仓仓位不足，orderData无法开仓,orderData={orderData}'.format(orderData=str(orderData))
                    warnings.warn(msg)
