'''
订单中包含的数据
start_orderData带有的参数：

orderId             str             订单ID
orderType           str             订单类型
instId              str             产品ID
toMode              str             全仓|逐仓   全仓：cross 逐仓：isolated
posSide             str             持仓方向    做多：long 做空：short
lever               int             杠杆 现货交易相当于杠杆为1
orderDatetime       str             开仓日期时间  格式：%Y-%m-%d %H:%M:%S
buyLine             int|float       开仓价格
buyCommissionRate   int|float       购买时候的手续费率
tpLine              int|float|None  止盈价格
slLine              int|float|None  止损价格
smLine              int|float|None  爆仓价格
buyMoney            int|float       开仓花费的金额

close_orderData计算的参数：

endType             str                 平仓方式    止盈：TP 止损：SL 爆仓：SM 按照时间段卖出：PT 超过最大持仓时间：TT 模拟交易后以市场价平仓：MT
endDatetime         str                 平仓日期时间  格式：%Y-%m-%d %H:%M:%S
sellLine            int|float           平仓价格
sellCommissionRate  int|float           卖出时候的手续费率
sellMoney           int|float           平仓后得到的金额（以考虑手续费）
holdMinute          int                 持仓时间（分钟）
commission          int|float           手续费
profit              int|float           利润
profitRate          int|float           利润率
hh                  int|float           持仓过程中的最高价格
hhRate              int|float           持仓过程中的最高价格相对于开仓价格的上涨百分比
ll                  int|float           持仓过程中的最低价格
llRate              int|float           持仓过程中的最低价格相对于开仓价格的下跌百分比

辅助字段：
orderIndex          int                 开仓Candle索引
endIndex            int                 平仓Candle索引
orderTs             float               开仓毫秒时间戳
endTs               float               平仓毫秒时间戳
'''
from typing import Literal, Union
import datetime
import paux.order
from ptrade import exception


class Order():
    def __init__(self, accountMoney: Union[int, float]):
        # 持仓总订单
        self.currentOrderDatas = []
        # 持仓多单
        self.currentLongOrderDatas = []
        # 持仓空单
        self.currentShortOrderDatas = []
        # 历史订单
        self.historyOrderDatas = []
        # 账户余额
        self.accountMoney = accountMoney

    @staticmethod
    def get_empty_orderData():
        orderData = {
            # start_orderData带有的参数：
            # orderId             str             订单ID
            'orderId': None,
            # orderType           str             订单类型
            'orderType': None,
            # instId              str             产品ID
            'instId': None,
            # toMode              str             全仓|逐仓   全仓：cross 逐仓：isolated
            'toMode': None,
            # posSide             str             持仓方向    做多：long 做空：short
            'posSide': None,
            # lever               int             杠杆 现货交易相当于杠杆为1
            'lever': None,
            # orderDatetime       str             开仓日期时间  格式：%Y-%m-%d %H:%M:%S
            'orderDatetime': None,
            # buyLine             int|float       开仓价格
            'buyLine': None,
            # buyCommissionRate   int|float       购买时候的手续费率
            'buyCommissionRate': None,
            # tpLine              int|float|None  止盈价格
            'tpLine': None,
            # slLine              int|float|None  止损价格
            'slLine': None,
            # smLine              int|float|None  爆仓价格
            'smLine': None,
            # buyMoney            int|float       开仓花费的金额
            'buyMoney': None,

            # close_orderData计算的参数：
            # endType             str                 平仓方式    止盈：TP 止损：SL 爆仓：SM 按照时间段卖出：PT 超过最大持仓时间：TT 模拟交易后以市场价平仓：MT
            'endType': None,
            # endDatetime         str                 平仓日期时间  格式：%Y-%m-%d %H:%M:%S
            'endDatetime': None,
            # sellLine            int|float           平仓价格
            'sellLine': None,
            # sellCommissionRate  int|float           卖出时候的手续费率
            'sellCommissionRate': None,
            # sellMoney           int|float           平仓后得到的金额（以考虑手续费）
            'sellMoney': None,
            # holdMinute          int                 持仓时间（分钟）
            'holdMinute': None,
            # commission          int|float           手续费
            'commission': None,
            # profit              int|float           利润
            'profit': None,
            # profitRate          int|float           利润率
            'profitRate': None,
            # hh                  int|float           持仓过程中的最高价格
            'hh': None,
            # hhRate              int|float           持仓过程中的最高价格相对于开仓价格的上涨百分比
            'hhRate': None,
            # ll                  int | float           持仓过程中的最低价格
            'll': None,
            # llRate              int|float           持仓过程中的最低价格相对于开仓价格的下跌百分比
            'llRate': None,

            # 辅助字段：
            # orderIndex          int                 开仓Candle索引
            'orderIndex': None,
            # endIndex            int                 平仓Candle索引
            'endIndex': None,
            # orderTs             float               开仓毫秒时间戳
            'orderTs': None,
            # endTs               float               平仓毫秒时间戳
            'endTs': None,
        }
        return orderData

    # 开仓
    def start_orderData(
            self,
            orderId: str,
            instId: str,
            toMode: Literal['cross', 'isolated'],
            posSide: Literal['long', 'short'],
            lever: int,
            orderDatetime: object,
            buyLine: Union[int, float],
            buyCommissionRate: Union[int, float],
            buyMoney: Union[int, float],
            tpRate: Union[int, float, None] = None,
            tpLine: Union[int, float, None] = None,
            slRate: Union[int, float, None] = None,
            slLine: Union[int, float, None] = None,
            smLine: Union[int, float, None] = None,
            orderType: object = None,
            **kwargs
    ):
        '''
        开仓
        关键字               类型            说明
        orderId             str             订单ID
        instId              str             产品ID
        toMode              str             全仓|逐仓   全仓：cross 逐仓：isolated
        posSide             str             持仓方向    做多：long 做空：short
        lever               int             杠杆 现货交易相当于杠杆为1
        orderDatetime       str             开仓日期时间  格式：%Y-%m-%d %H:%M:%S
        buyLine             int|float       开仓价格
        buyCommissionRate   int|float       购买时候的手续费率
        buyMoney            int|float       开仓花费的金额
        tpRate              int|float|None  止盈率
        tpLine              int|float|None  止盈价格（优先级：止盈价格 >>> 止盈率）
        slRate              int|float       止损率
        slLine              int|float|None  止损价格（优先级：止损价格 >>> 止损率）
        smLine              int|float|None  爆仓价格（逐仓会自动计算出强制平仓价格，全仓需要用户手动设置smLine）
        orderType           str             订单类型
        '''
        # 获得一个初始化的订单
        orderData = self.get_empty_orderData()
        # 如果没有tpLine，则使用tpRate计算tpLine
        if not tpLine and tpRate:
            if posSide == 'long':
                tpLine = buyLine * (1 + abs(tpRate))
            elif posSide == 'short':
                tpLine = buyLine * (1 - abs(tpRate))
            else:
                raise exception.PosSideParamError(posSide)

        # 如果没有slLine，则使用slRate计算slLine
        if not slLine and slRate:
            if posSide == 'long':
                slLine = buyLine * (1 - abs(slRate))
            elif posSide == 'short':
                slLine = buyLine * (1 + abs(slRate))
            else:
                raise exception.PosSideParamError(posSide)
        # 计算smLine
        if toMode == 'isolated':
            if posSide == 'long':
                smLine = buyLine * (1 - 1 / lever)  # stock market
            elif posSide == 'short':
                smLine = buyLine * (1 + 1 / lever)  # stock market
            else:
                raise exception.PosSideParamError(posSide)
        elif toMode == 'cross':
            smLine = smLine
        else:
            raise exception.ToModeParamError(toMode)
        # 赋值
        orderData['orderId'] = orderId
        orderData['orderType'] = orderType
        orderData['instId'] = instId
        orderData['toMode'] = toMode
        orderData['posSide'] = posSide
        orderData['lever'] = lever
        orderData['orderDatetime'] = orderDatetime
        orderData['buyLine'] = paux.order.round_simulate(buyLine)
        orderData['buyCommissionRate'] = buyCommissionRate
        # 保留位数
        orderData['tpLine'] = paux.order.round_simulate(tpLine) if tpLine != None else None
        orderData['slLine'] = paux.order.round_simulate(slLine) if slLine != None else None
        orderData['smLine'] = paux.order.round_simulate(smLine) if smLine != None else None
        orderData['buyMoney'] = buyMoney
        # 补充字段
        for key, value in kwargs.items():
            orderData[key] = value
        return orderData

    # 平仓
    def close_orderData(
            self,
            orderData: dict,
            sellLine: Union[int, float],
            sellCommissionRate: Union[int, float],
            endDatetime: str,
            endType: str = None,
            **kwargs
    ):
        '''
        平仓
        参数                 类型                 说明
        orderData           dict                待平仓订单
        sellLine            int|float           平仓价格
        sellCommissionRate  int|float           卖出时候的手续费率
        endDatetime         str                 平仓日期时间  格式：%Y-%m-%d %H:%M:%S
        endType             str                 平仓方式    止盈：TP 止损：SL 爆仓：SM 按照时间段卖出：PT 超过最大持仓时间：TT 模拟交易后以市场价平仓：MT
        '''
        # 卖出价格
        sellLine = paux.order.round_simulate(sellLine)
        # 是否需要考虑爆仓
        if orderData['toMode'] == 'cross':
            pass
        elif orderData['toMode'] == 'isolated':
            # 多仓爆仓
            if orderData['posSide'] == 'long' and sellLine <= orderData['smLine']:
                sellLine = orderData['smLine']
                endType = 'SM'
            # 空仓爆仓
            elif orderData['posSide'] == 'short' and sellLine >= orderData['smLine']:
                sellLine = orderData['smLine']
                endType = 'SM'
        else:
            raise exception.ToModeParamError(orderData['toMode'])
        # 持仓时间（分钟）
        holdMinute = int(
            (datetime.datetime.strptime(endDatetime, '%Y-%m-%d %H:%M:%S', ).timestamp() - datetime.datetime.strptime(
                orderData['orderDatetime'], '%Y-%m-%d %H:%M:%S').timestamp()) / 60)
        commission_data = paux.order.get_commission_data(
            posSide=orderData['posSide'],
            buyMoney=orderData['buyMoney'],
            buyLine=orderData['buyLine'],
            sellLine=sellLine,
            lever=orderData['lever'],
            buyCommissionRate=orderData['buyCommissionRate'],
            sellCommissionRate=sellCommissionRate
        )

        commission = commission_data['commission']
        sellMoney = commission_data['sellMoney']
        profitRate = commission_data['profitRate']
        profit = round(profitRate * orderData['buyMoney'], 4)

        # 赋值
        orderData['endType'] = endType
        orderData['endDatetime'] = endDatetime
        orderData['sellLine'] = sellLine
        orderData['holdMinute'] = holdMinute
        orderData['commission'] = commission
        orderData['sellMoney'] = sellMoney
        orderData['profitRate'] = profitRate
        orderData['profit'] = profit
        orderData['sellCommissionRate'] = sellCommissionRate
        # 补充字段
        for key, value in kwargs.items():
            orderData[key] = value
        return orderData

    # 处理平仓数据
    def to_historyOrderDatas(self, orderDatas: Union[list, tuple, None]):
        '''
        按照orderId，删除currentOrderDatas、currentLongOrderDatas、currentShortOrderDatas
        添加到historyOrderDatas中
        账户金额如果出现负数，会报告异常

        orderDatas          list        待平仓订单列表
        '''

        if orderDatas:
            for orderData in orderDatas:
                # 总持仓中的orderId
                currentOrderIds = [orderData['orderId'] for orderData in self.currentOrderDatas]
                # 待平仓的订单Id
                orderId = orderData['orderId']
                # 此订单不在持仓中
                if not orderId in currentOrderIds:
                    continue

                # 删除总持仓中的orderId订单
                del self.currentOrderDatas[currentOrderIds.index(orderId)]
                # 删除多仓持仓中的orderId订单
                if orderData['posSide'] == 'long':
                    # 多仓持仓中的orderId
                    currentLongOrderIds = [orderData['orderId'] for orderData in self.currentLongOrderDatas]
                    del self.currentLongOrderDatas[currentLongOrderIds.index(orderId)]
                # 删除空仓持仓中的orderId订单
                elif orderData['posSide'] == 'short':
                    # 空仓持仓中的orderId
                    currentShortOrderIds = [orderData['orderId'] for orderData in self.currentShortOrderDatas]
                    del self.currentShortOrderDatas[currentShortOrderIds.index(orderId)]
                # 添加到历史订单中
                self.historyOrderDatas.append(orderData)
                # 维护账户余额
                self.accountMoney += orderData['sellMoney']
                if self.accountMoney < 0:
                    raise exception.OrderError('账户余额不能小于零')

    # 进入持仓数据
    def to_currentOrderDatas(self, orderDatas: Union[list, tuple, None]):
        '''
        添加到currentOrderDatas、currentLongOrderDatas、currentShortOrderDatas
        账户金额如果出现负数，会报告异常

        orderDatas          list        开仓订单列表
        '''
        if orderDatas:
            for orderData in orderDatas:
                # 添加持仓
                self.currentOrderDatas.append(orderData)
                if orderData['posSide'] == 'long':
                    self.currentLongOrderDatas.append(orderData)
                elif orderData['posSide'] == 'short':
                    self.currentShortOrderDatas.append(orderData)
                # 维护账户余额
                self.accountMoney -= orderData['buyMoney']
                if self.accountMoney < 0:
                    raise exception.OrderError('账户余额不能小于零')
