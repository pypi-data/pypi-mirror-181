from ptrade.simulate.simulate import Simulate
from ptrade.simulate.simulate_multiply import SimulateMultiply


# from typing import Union
# import datetime
# import numpy as np
# import paux.process
# from ptrade.simulate._trade import _Trade as __Trade
# import ptrade.component
#
#
# class Simulate(__Trade):
#     def __init__(
#             self,
#             candle: np.array,
#             rule: object,
#             instId: str = None,
#             warn: bool = True,
#     ):
#         '''
#         :param candle: 历史K线数据
#         :param rule: 规则
#         :param instId: 产品ID
#         :param warn: 是否报告警告
#         '''
#         # 参数与内置模块
#         self.candle = candle  # K线数据
#         self.rule = rule  # 规则
#         self.instId = instId  # 标底
#         self.warn = warn
#         self._order = ptrade.component.Order(accountMoney=rule.ACCOUNT_MONEY)  # 订单模块
#         # 当前K线单位时间内
#         self.index = np.nan  # 被遍历的candle行索引
#         self.open = np.nan  # 开盘价
#         self.low = np.nan  # 最低价
#         self.high = np.nan  # 最高价
#         self.close = np.nan  # 收盘价
#         self.volume = np.nan  # todo
#         self.ts = np.nan  # 开盘时刻的毫秒级时间戳
#         # 当前时刻
#         self.datetime = None
#         self.date = None
#         self.time = None
#         # 前一天的数据
#         self.last_day_open = np.nan  # 昨日开盘价
#         self.last_day_high = np.nan  # 昨日最高价
#         self.last_day_low = np.nan  # 昨日最低价
#         self.last_day_close = np.nan  # 昨日收盘价
#
#         self.setup()
#
#
# def _process_simualte_multiply_worker(
#         simulate,start,end,clear
# ):
#     simulate.run(start=start,end=end,clear=clear)
#     return [simulate.historyOrderDatas,simulate.currentOrderDatas]
#
#
#
# # 执行多个产品的模拟交易
# class SimulateMultiply():
#     def __init__(
#             self,
#             Simulate,
#             candle_map: dict,
#             rule: object,
#             warn: bool = True,
#     ):
#         self.simulate_map = {}
#         for instId, candle in candle_map.items():
#             self.simulate_map[instId] = Simulate(
#                 candle=candle,
#                 rule=rule,
#                 instId=instId,
#                 warn=warn
#             )
#
#     def run(
#             self,
#             start: Union[datetime.date, int, float, str, None] = None,
#             end: Union[datetime.date, int, float, str, None] = None,
#             clear: bool = True,
#             p_num=1,
#             skip_exception=False,
#     ):
#         if p_num <= 1:
#             self.historyOrderDatas = []
#             for instId, simulate in self.simulate_map.items():
#                 simulate.run(start=start, end=end, clear=clear)
#                 self.historyOrderDatas += simulate.historyOrderDatas
#             self.analysis = ptrade.component.Analysis(historyOrderDatas=self.historyOrderDatas)
#         else:
#             # warnings.warn('p_num应该为1，异步执行存在安全性问题，下个版本会更新')
#             params = []
#             index_to_instId = {}
#             for index, (instId, simulate) in enumerate(self.simulate_map.items()):
#                 index_to_instId[index] = instId
#                 params.append(
#                     {
#                         'simulate':simulate,
#                         'start': start,
#                         'end': end,
#                         'clear': clear,
#                     }
#                 )
#             results = paux.process.pool_worker(
#                 params=params,
#                 p_num=p_num,
#                 func=_process_simualte_multiply_worker,
#                 skip_exception=skip_exception
#             )
#             self.historyOrderDatas = []
#             self.currentOrderDatas = []
#             for index, (historyOrderDatas,currentOrderDatas) in enumerate(results):
#                 instId = index_to_instId[index]
#                 self.simulate_map[instId].historyOrderDatas = historyOrderDatas
#                 self.simulate_map[instId].currentOrderDatas = currentOrderDatas
#                 self.historyOrderDatas += historyOrderDatas
#                 self.historyOrderDatas += currentOrderDatas
#             self.analysis = ptrade.component.Analysis(historyOrderDatas=self.historyOrderDatas)
