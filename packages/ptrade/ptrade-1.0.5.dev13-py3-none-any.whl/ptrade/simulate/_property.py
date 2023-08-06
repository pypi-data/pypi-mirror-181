'''
模拟交易中的属性:

属性                                 返回类型     说明
accountMoney                        int|float   账户可用余额
positionAccountMoney                int|float   持仓余额估计
longPositionAccountMoney            int|float   多单持仓余额估计
shortPositionAccountMoney           int|float   空单持仓余额估计

currentOrderDatas                   list        持仓订单数据
currentLongOrderDatas               list        持仓多单数据
currentShortOrderDatas              list        持仓空单数据

currentOrderDatasCanBeTraded        list        可以被交易的订单
currentLongOrderDatasCanBeTraded    list        可以被交易的多单
currentShortOrderDatasCanBeTraded   list        可以被交易的空单

currentTodayOrderDatas              list        今天的仓位数据
currentTodayLongOrderDatas          list        今天的多仓位数据
currentTodayShortOrderDatas         list        今天的空仓位数据

historyOrderDatas                   list        历史订单数据
historyLongOrderDatas               list        历史多单数据
historyShortOrderDatas              list        历史空单数据

currentPosition                     int         获得持仓的总订单数量
currentLongPosition                 int         获得持仓的多单数量
currentShortPosition                int         获得持仓的空单数量

longPositionLeft                    int         剩余多仓数量
shortPositionLeft                   int         剩余空仓数量
'''

import numpy as np
import datetime
from ptrade.component.order import Order as _Order
from ptrade.component.rule import Rule
import paux.order


class _Property():
    candle: np.array
    instId: str
    rule: Rule
    _order: _Order
    date: datetime.date

    # 余额 ------------------------------------------------------------------------------------------------
    # 账户可用余额
    @property
    def accountMoney(self):
        return self._order.accountMoney

    @accountMoney.setter
    def accountMoney(self, value):
        self._order.accountMoney = value

    # 持仓余额估计
    def __positionAccountMoney(self, orderDatas):
        accountMoney_in_position = 0
        for orderData in orderDatas:
            sellMoney = paux.order.get_commission_data(
                posSide=orderData['posSide'],
                buyMoney=orderData['buyMoney'],
                buyLine=orderData['buyLine'],
                sellLine=orderData['sellLine'],
                lever=orderData['lever'],
                buyCommissionRate=self.rule.BUY_COMMISSION_RATE,
                sellCommissionRate=self.rule.SELL_COMMISSION_RATE,
            )['sellMoney']
            accountMoney_in_position += sellMoney
        return accountMoney_in_position

    # 持仓余额估计
    @property
    def positionAccountMoney(self):
        orderDatas = self.currentOrderDatas
        return self.__positionAccountMoney(orderDatas)

    # 多单持仓余额估计
    @property
    def longPositionAccountMoney(self):
        orderDatas = self.currentLongOrderDatas
        return self.__positionAccountMoney(orderDatas)

    # 空单持仓余额估计
    @property
    def shortPositionAccountMoney(self):
        orderDatas = self.currentShortOrderDatas
        return self.__positionAccountMoney(orderDatas)

    # 持仓订单数据---------------------------------------------------------------------------------------------
    # 持仓订单数据
    @property
    def currentOrderDatas(self):
        return self._order.currentOrderDatas

    @currentOrderDatas.setter
    def currentOrderDatas(self, value):
        self._order.currentOrderDatas = value

    # 持仓多单数据
    @property
    def currentLongOrderDatas(self):
        return self._order.currentLongOrderDatas

    # 持仓空单数据
    @property
    def currentShortOrderDatas(self):
        return self._order.currentShortOrderDatas

    # 可以被交易的订单
    def __currentOrderDatasCanBeTraded(self, orderDatas):
        if self.rule.T == 0:
            return orderDatas
        dateCanBeTrade = (self.date + datetime.timedelta(days=self.rule.T)).strftime('%Y-%m-%d')

        orderDatas = []
        for orderData in orderDatas:
            if dateCanBeTrade >= orderData['orderDatetime']:
                orderDatas.append(orderData)
        return orderDatas

    # 可以被交易的订单
    @property
    def currentOrderDatasCanBeTraded(self):
        orderDatas = self.currentOrderDatas
        return self.__currentOrderDatasCanBeTraded(orderDatas)

    # 可以被交易的多单
    @property
    def currentLongOrderDatasCanBeTraded(self):
        orderDatas = self.currentLongOrderDatas
        return self.__currentOrderDatasCanBeTraded(orderDatas)

    # 以被交易的空单
    @property
    def currentShortOrderDatasCanBeTraded(self):
        orderDatas = self.currentShortOrderDatas
        return self.__currentOrderDatasCanBeTraded(orderDatas)

    # 今天的仓位
    def __currentTodayOrderDatas(self, orderDatas):
        return [
            orderData for orderData in orderDatas if
            orderData['orderDatetime'][0:10] == self.date.strftime('%Y-%m-%d')
        ]

    # 今天的仓位数据
    @property
    def currentTodayOrderDatas(self):
        orderDatas = self.currentOrderDatas
        return self.__currentTodayOrderDatas(orderDatas)

    # 今天的多仓位数据
    @property
    def currentTodayLongOrderDatas(self):
        orderDatas = self.currentLongOrderDatas
        return self.__currentTodayOrderDatas(orderDatas)

    # 今天的空仓位数据
    @property
    def currentTodayShortOrderDatas(self):
        orderDatas = self.currentShortOrderDatas
        return self.__currentTodayOrderDatas(orderDatas)

    # 历史订单数据---------------------------------------------------------------------------------------------
    # 历史订单数据
    @property
    def historyOrderDatas(self):
        return self._order.historyOrderDatas

    @historyOrderDatas.setter
    def historyOrderDatas(self, value):
        self._order.historyOrderDatas = value

    # 历史多单数据
    @property
    def historyLongOrderDatas(self):
        return [
            orderData for orderData in self._order.historyOrderDatas if orderData['posSide'] == 'long'
        ]

    # 历史空单数据
    @property
    def historyShortOrderDatas(self):
        return [
            orderData for orderData in self._order.historyOrderDatas if orderData['posSide'] == 'short'
        ]

    # 仓位数量---------------------------------------------------------------------------------------------
    # 获得持仓的总订单数量
    @property
    def currentPosition(self):
        return len(self._order.currentOrderDatas)

    # 获得持仓的多单数量
    @property
    def currentLongPosition(self):
        return len(self._order.currentLongOrderDatas)

    # 获得持仓的空单数量
    @property
    def currentShortPosition(self):
        return len(self._order.currentShortOrderDatas)

    # 剩余多仓数量
    @property
    def longPositionLeft(self):
        longPositionLeft = min(
            self.rule.LONG_POSITION - self.currentLongPosition,
            self.rule.POSITION - self.currentPosition,
        )
        return longPositionLeft

    # 剩余空仓数量
    @property
    def shortPositionLeft(self):
        # 剩余仓位数量
        shortPositionLeft = min(
            self.rule.SHORT_POSITION - self.currentShortPosition,
            self.rule.POSITION - self.currentPosition,
        )
        return shortPositionLeft
