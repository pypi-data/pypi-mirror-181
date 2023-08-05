'''
get_df      获取历史订单：


orderType       str         订单类型
posSide         str         持仓方向    做多：long 做空：short
instId          str         产品ID
toMode          str         全仓|逐仓   全仓：cross 逐仓：isolated
lever           int         杠杆 现货交易相当于杠杆为1
orderDatetime   str         开仓日期时间  格式：%Y-%m-%d %H:%M:%S
endDatetime     str         平仓日期时间  格式：%Y-%m-%d %H:%M:%S
holdMinute      int         持仓时间（分钟）
endType         str         平仓方式    止盈：TP 止损：SL 爆仓：SM 按照时间段卖出：PT 超过最大持仓时间：TT 模拟交易后以市场价平仓：MT
buyLine         int|float   开仓价格
sellLine        int|float   平仓价格
tpLine          int|float|None   止盈价格
slLine          int|float|None   止损价格
smLine          int|float|None   爆仓价格
buyMoney        int|float   开仓花费的金额
sellMoney       int|float   平仓后得到的金额（以考虑手续费）
commission      int|float   手续费
profit          int|float   利润
profitRate      int|float   利润率
hh              int|float   持仓过程中的最高价格
hhRate          int|float   持仓过程中的最高价格相对于开仓价格的上涨百分比
ll              int|float           持仓过程中的最低价格
llRate          int|float           持仓过程中的最低价格相对于开仓价格的下跌百分比


INFO_COLUMNS
period                  str         时间段
profit_sum              int|float   总利润
profit_mean             int|float   平均单位订单利润
profit_peak             int|float   利润最高峰
profit_valley           int|float   利润最低谷
dprofit                 int|float   最大连续盈利
dloss                   int|float   最大连续亏损
profit_num              int|float   盈利订单数量
loss_num                int|float   亏损订单数量
profit_suc_rate         int|float   盈利订单占比
order_num               int         订单数量
account_money           int|float   时间段结尾账户金额
account_money_peak      int|float   账户金额最高峰
account_money_valley    int|float   账户金额最低谷
'''

'''
|orderType|str|订单类型|
|posSide|str|持仓方向 做多：long 做空：short|
|instId|str|产品ID|
|toMode|str|全仓|逐仓 全仓：cross 逐仓：isolated|
|lever|int|杠杆，现货交易相当于杠杆为1|
|orderDatetime|str|开仓日期时间 格式：%Y-%m-%d %H:%M:%S|
|endDatetime|str|平仓日期时间 格式：%Y-%m-%d %H:%M:%S|
|holdMinute|int|持仓时间（分钟）|
|endType|str|平仓方式，止盈：TP 止损：SL 爆仓：SM 按照时间段卖出：PT 超过最大持仓时间：TT 模拟交易后以市场价平仓：MT|
|buyLine|int \| float|开仓价格|
|sellLine|int \| float|平仓价格|
|tpLine|int \| float \| None|止盈价格|
|slLine|int \| float \| None|止损价格|
|smLine|int \| float \| None|爆仓价格|
|buyMoney|int \| float|开仓花费的金额|
|sellMoney|int \| float|平仓后得到的金额（以考虑手续费）|
|commission|int \| float|手续费|
|profit|int \| float|利润|
|profitRate|int \| float|利润率|
|hh|int \| float|持仓过程中的最高价格|
|hhRate|int \| float|持仓过程中的最高价格相对于开仓价格的上涨百分比|
|ll|int \| float|持仓过程中的最低价格|
|llRate|int \| float|持仓过程中的最低价格相对于开仓价格的下跌百分比|
'''

from typing import Literal, Union
from copy import deepcopy
import numpy as np
import pandas as pd
import datetime
from ptrade import exception

pd.set_option('display.max_rows', 100)  # 最多展示1000行
pd.set_option('display.max_columns', 25)  # 最多展示10列


# 分析模块
class Analysis():
    # 默认展示的DataFrame字段
    DETAIL_COLUMNS = [
        'orderType',
        'posSide',
        'instId',
        'toMode',
        'lever',
        'orderDatetime',
        'endDatetime',
        'holdMinute',
        'endType',
        'buyLine',
        'sellLine',
        'tpLine',
        'slLine',
        'smLine',
        'buyMoney',
        'sellMoney',
        'commission',
        'profit',
        'profitRate',
        'hh',
        'hhRate',
        'll',
        'llRate',
    ]

    # 过程数据中展示的字段
    INFO_COLUMNS = [
        'period',
        'profit_sum',
        'profit_mean',
        'profit_peak',
        'profit_valley',
        'dprofit',
        'dloss',
        'profit_num',
        'loss_num',
        'profit_suc_rate',
        'order_num',
        'account_money',
        'account_money_peak',
        'account_money_valley',
    ]

    def __init__(self, historyOrderDatas: list = []):
        self.historyOrderDatas = historyOrderDatas
        if self.historyOrderDatas:
            self.df = pd.DataFrame(self.historyOrderDatas).sort_values(by='orderDatetime').reset_index(
                drop=True)  # 保留更多的字段
        else:
            self.df = pd.DataFrame([], columns=self.DETAIL_COLUMNS)



    def __get_df_columns(self, **kwargs):
        # 默认字段
        df_columns = deepcopy(self.DETAIL_COLUMNS)
        # 自定义控制字段的显示
        for column, show in kwargs.items():
            if show == True and column not in df_columns:
                df_columns.append(column)
                continue
            if show == False and column in df_columns:
                df_columns.remove(column)
                continue
        return df_columns

    # 获得历史订单的DataFrame对象
    def get_df(
            self,
            historyOrderDatas: list = [],
            **kwargs
    ):
        '''
        :param historyOrderDatas: 历史订单数据
        :param kwargs: 补充字段的显示与隐藏

        优先级：
        historyOrderDatas >>> self.df
        '''
        if not historyOrderDatas:
            df = self.df
        else:
            df = pd.DataFrame(historyOrderDatas).sort_values(by='orderDatetime').reset_index(drop=True)
        # 筛选字段
        df_columns = self.__get_df_columns(**kwargs)
        df = df[df_columns]
        return df

    # 按照仓位计算交易过程DataFrame
    def get_df_by_position(
            self,
            position: int = None,
            longPosition: int = None,
            shortPosition: int = None,
            historyOrderDatas: list = [],
            df: pd.DataFrame = None,
            **kwargs,
    ):
        '''
        :param position: 总仓位
        :param longPosition: 多仓位
        :param shortPosition: 空仓位
        :param historyOrderDatas: 列表类型的历史订单
        :param df: DataFrame类型的历史订单
        :param kwargs: 补充字段的显示与隐藏

        优先级：
            historyOrderDatas >>> df >>> self.df >>> self.historyOrderDatas
        '''
        # >>1 使用historyOrderDatas
        if historyOrderDatas:
            df = self.get_df(historyOrderDatas=historyOrderDatas)
        # >>2 使用df
        elif type(df).__name__ != 'NoneType':
            df = df
        else:
            # >>3 使用self.df
            if hasattr(self, 'df'):
                df = self.df
            # >> 4 获取self.df
            else:
                df = self.get_df()
        # 空数据
        if df.shape[0] == 0:
            return df
        # 日期排序
        df = df.sort_values(by='orderDatetime').reset_index(drop=True)
        # 如果需要过滤仓位
        if position or longPosition or shortPosition:
            # position longPosition shortPosition默认为无穷大
            if position == None:
                position = 9999 * 9999
            if longPosition == None:
                longPosition = 9999 * 9999
            if shortPosition == None:
                shortPosition = 9999 * 9999
            # 初始化
            currentLongOrderDatas = []
            currentShortOrderDatas = []
            currentOrderDatas = []
            historyOrderDatas = []

            for i in df.index:
                # 本次的订单
                thisOrderData = df.loc[i].to_dict()
                # 卖出之前的订单
                removeLongOrderDatas = []
                removeShortOrderDatas = []
                removeOrderDatas = []
                # 找到应该被平仓的订单
                for orderData in currentOrderDatas:
                    if orderData['endDatetime'] <= thisOrderData['orderDatetime']:
                        removeOrderDatas.append(orderData)
                        if orderData['posSide'] == 'long':
                            removeLongOrderDatas.append(orderData)
                        elif orderData['posSide'] == 'short':
                            removeShortOrderDatas.append(orderData)
                # 平仓 删除与添加(总)
                for orderData in removeOrderDatas:
                    historyOrderDatas.append(orderData)
                    currentOrderDatas.remove(orderData)
                # 平仓 删除(多)
                for orderData in removeLongOrderDatas:
                    currentLongOrderDatas.remove(orderData)
                # 平仓 删除(空)
                for orderData in removeShortOrderDatas:
                    currentShortOrderDatas.remove(orderData)
                # 剩余多仓位
                longPositionLeft = min(
                    position - len(currentOrderDatas),
                    longPosition - len(currentLongOrderDatas),
                )
                # 剩余空仓位
                shortPositionLeft = min(
                    position - len(currentOrderDatas),
                    shortPosition - len(currentShortOrderDatas),
                )
                # 按照是否有剩余仓位，决定是否能添加到current
                if thisOrderData['posSide'] == 'long':
                    if longPositionLeft > 0:
                        currentLongOrderDatas.append(thisOrderData)
                        currentOrderDatas.append(thisOrderData)
                elif thisOrderData['posSide'] == 'short':
                    if shortPositionLeft > 0:
                        currentShortOrderDatas.append(thisOrderData)
                        currentOrderDatas.append(thisOrderData)
            # 结尾强制平仓
            historyOrderDatas += currentOrderDatas
            df = pd.DataFrame(historyOrderDatas)
        # 筛选字段
        df_columns = self.__get_df_columns(**kwargs)
        df = df[df_columns]
        return df

    # 计算等比连续投资的DataFrame
    def get_df_sequential_investment(
            self,
            account_money: Union[int, float],
            invest_percentage: Union[int, float] = 0.1,
            position: int = None,
            longPosition: int = None,
            shortPosition: int = None,
            historyOrderDatas: list = [],
            df: pd.DataFrame = None,
            **kwargs,
    ):
        '''
        :param account_money: 账户余额
        :param invest_percentage: 投资金额比
        :param position: 总仓位
        :param longPosition: 多仓位
        :param shortPosition: 空仓位
        :param historyOrderDatas: 列表类型的历史订单
        :param df: DataFrame类型的历史订单
        :param kwargs: 补充字段的显示与隐藏

        优先级：
            historyOrderDatas >>> df >>> self.df >>> self.historyOrderDatas
        '''
        # 按照仓位过滤得到df
        df = self.get_df_by_position(
            position=position,
            longPosition=longPosition,
            shortPosition=shortPosition,
            historyOrderDatas=historyOrderDatas,
            df=df,
        )
        # 空数据
        if not df.shape[0]:
            return df
        # 日期排序
        df = df.sort_values(by='orderDatetime').reset_index(drop=True)
        # 初始化订单列表
        currentOrderDatas = []
        historyOrderDatas = []
        # 逐行遍历
        for i in df.index:
            # 如果当前持仓超过了总仓位，是未知错误
            if position != None and len(currentOrderDatas) > position:
                error_msg = '未知错误，超过了总仓位'
                raise exception.UnexpectError(error_msg)
            # 本次的订单
            thisOrderData = df.loc[i].to_dict()
            # 可以卖出的订单
            removeOrderDatas = []
            for orderData in currentOrderDatas:
                if orderData['endDatetime'] <= thisOrderData['orderDatetime']:
                    removeOrderDatas.append(orderData)
            # 添加与删除，并添加金额到account_money
            for orderData in removeOrderDatas:
                account_money += orderData['profit']
                historyOrderDatas.append(orderData)
                currentOrderDatas.remove(orderData)
            # 如果有余额
            if account_money > 0:
                # 计算购买余额
                buyMoney = min(
                    account_money,
                    (account_money + sum([
                        orderData['buyMoney'] for orderData in currentOrderDatas
                    ])) * invest_percentage
                )
                # alter比例
                alter_rate = buyMoney / thisOrderData['buyMoney']
                # 等比扩大
                thisOrderData['buyMoney'] = round(alter_rate * thisOrderData['buyMoney'], 4)
                thisOrderData['sellMoney'] = round(alter_rate * thisOrderData['sellMoney'], 4)
                thisOrderData['commission'] = round(alter_rate * thisOrderData['commission'], 8)
                thisOrderData['profit'] = round(alter_rate * thisOrderData['profit'], 4)
                currentOrderDatas.append(thisOrderData)
        # 结尾强制平仓
        historyOrderDatas += currentOrderDatas
        # 有订单数据
        if historyOrderDatas:
            df_sequential_investment = pd.DataFrame(historyOrderDatas)
        # 无订单数据
        else:
            df_sequential_investment = pd.DataFrame([], columns=self.DETAIL_COLUMNS)
        df_columns = self.__get_df_columns(**kwargs)
        df_sequential_investment = df_sequential_investment[df_columns]
        return df_sequential_investment

    # 获取交易过程中的分析数据
    def get_df_process_info(
            self,
            account_money: Union[int, float],
            period: Literal['day', 'week', 'month', 'year', 'all'],
            position: int = None,
            longPosition: int = None,
            shortPosition: int = None,
            historyOrderDatas: list = [],
            df: pd.DataFrame = None,
    ):
        '''
        :param account_money: 账户余额
        :param period: 统计的单位时间段
        :param position: 总仓位
        :param longPosition: 多仓位
        :param shortPosition: 空仓位
        :param historyOrderDatas: 列表类型的历史订单
        :param df: DataFrame类型的历史订单

        优先级：
            historyOrderDatas >>> df >>> self.df >>> self.historyOrderDatas
        '''
        # 按照仓位过滤得到df
        df = self.get_df_by_position(
            position=position,
            longPosition=longPosition,
            shortPosition=shortPosition,
            historyOrderDatas=historyOrderDatas,
            df=df
        )
        # 空数据
        if not df.shape[0]:
            return pd.DataFrame([], columns=self.INFO_COLUMNS)
        # 建立单位时间段字段period
        if period == 'day':
            df[period] = df['endDatetime'].apply(lambda d: d[0:10])
        elif period == 'week':
            df[period] = ''
            for index in df.index:
                this_year, this_month = datetime.datetime.strptime(
                    df.loc[index, 'endDatetime'],
                    '%Y-%m-%d %H:%M:%S'
                ).isocalendar()[0:2]
                df.loc[index, period] = '{:0>4d}~{:0>2d}'.format(this_year, this_month)
        elif period == 'month':
            df[period] = df['endDatetime'].apply(lambda d: d[0:7])
        elif period == 'year':
            df[period] = df['endDatetime'].apply(lambda d: d[0:4])
        elif period == 'all':
            df[period] = '{start_date}~{end_date}'.format(
                start_date=df['orderDatetime'].min()[0:10],
                end_date=df['endDatetime'].min()[0:10],
            )
        else:
            msg = f'period = f{period}，period must in ["day","week","month","year","all"]'
            raise exception.ParamError(msg)
        df['isprofit'] = 0
        df['isloss'] = 0
        for index in df.index:
            if df.loc[index, 'profit'] > 0:
                df.loc[index, 'isprofit'] = 1
            else:
                df.loc[index, 'isloss'] = 1
        # 初始化数据
        info_datas = []
        # 订单终止的类型
        endTypes = df['endType'].unique().tolist()
        for this_period, df_gb in df.groupby(period):
            profit_sum = round(df_gb['profit'].sum(), 4)  # 总利润
            profit_mean = round(df_gb['profit'].mean(), 4)  # 订单平均利润
            dprofit = 0  # 最大连续盈利
            dloss = 0  # 最大连续亏损
            profits = df_gb['profit'].values  # 利润序列
            cum_profits = np.cumsum(profits)  # 利润累加
            profit_peak = cum_profits.max()  # 利润最高峰
            profit_valley = cum_profits.min()  # 利润最低谷
            for i in range(df_gb.shape[0]):
                cum_profits = np.cumsum(profits[i:])  # 分段利润累加
                dprofit = max(dprofit, np.max(cum_profits))  # 最大连续盈利
                dloss = min(dloss, np.min(cum_profits))  # 最大连续亏损

            profit_num = df_gb['isprofit'].sum()
            loss_num = df_gb['isloss'].sum()
            profit_suc_rate = round(profit_num / (profit_num + loss_num), 3)
            order_num = df_gb.shape[0]  # 订单数量
            account_money_peak = account_money + profit_peak  # 账户金额最高峰
            account_money_valley = account_money + profit_valley  # 账户金额最低谷
            account_money = account_money + profit_sum  # 交易后的交易金额

            this_data = {
                'period': period,
                period: this_period,
                'profit_sum': profit_sum,
                'profit_mean': profit_mean,
                'profit_peak': profit_peak,
                'profit_valley': profit_valley,
                'dprofit': dprofit,
                'dloss': dloss,
                'profit_num': profit_num,
                'loss_num': loss_num,
                'profit_suc_rate': profit_suc_rate,
                'order_num': order_num,
                'account_money': account_money,
                'account_money_peak': account_money_peak,
                'account_money_valley': account_money_valley,

            }
            # 补充各个endType的次数
            for endType in endTypes:
                if endType != None:
                    this_data[endType] = df_gb.query('endType==@endType').shape[0]
            info_datas.append(this_data)
        return pd.DataFrame(info_datas)