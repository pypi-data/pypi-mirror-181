import os.path
import sys

# simulate_jupyter_content = '''{
#  "cells": [
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "0b323301",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "import ptrade"
#    ]
#   },
#   {
#    "cell_type": "markdown",
#    "id": "9d9779ee",
#    "metadata": {},
#    "source": [
#     "## Rule"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "35a23da8",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "class MyRule():\\n",
#     "    # [交易规则] -----------------------------------------------------------\\n",
#     "    # T = 0 -> T0交易\\n",
#     "    # T = 1 -> T1交易 ...\\n",
#     "    T = 0\\n",
#     "    # [时区] --------------------------------------------------------------\\n",
#     "    TIMEZONE = 'Asia/Shanghai'  \\n",
#     "    # TIMEZONE = 'America/New_York' \\n",
#     "    # [账户余额] -----------------------------------------------------------\\n",
#     "    ACCOUNT_MONEY = 1000\\n",
#     "    # [购买金额] -----------------------------------------------------------\\n",
#     "    # 单次开仓的默认金额占比\\n",
#     "    BUY_MONEY_RATE = None  \\n",
#     "    # 单次开仓的默认金额\\n",
#     "    BUY_MONEY = 100  \\n",
#     "    # [止盈止损] -----------------------------------------------------------\\n",
#     "    # 多单止盈，挂单价格\\n",
#     "    LONG_TP_RATE = None  \\n",
#     "    # 多单止损，出发止损价格，以市价单平仓\\n",
#     "    LONG_SL_RATE = None  \\n",
#     "    # 空单止盈，挂单价格\\n",
#     "    SHORT_TP_RATE = None  \\n",
#     "    # 空单止损，出发止损价格，以市价单平仓\\n",
#     "    SHORT_SL_RATE = None  \\n",
#     "    # [杠杆] ---------------------------------------------------------------\\n",
#     "    # 多单杠杆\\n",
#     "    LONG_LEVER = 1  \\n",
#     "    # 空单杠杆\\n",
#     "    SHORT_LEVER = 1  \\n",
#     "    # [仓位] ---------------------------------------------------------------\\n",
#     "    # 多单仓位\\n",
#     "    LONG_POSITION = 5\\n",
#     "    # 空单仓位\\n",
#     "    SHORT_POSITION = 5  \\n",
#     "    # 总仓位\\n",
#     "    POSITION = 10  \\n",
#     "    # [最长订单时间（分钟）] ---------------------------------------------------\\n",
#     "    # 可以执行开仓的时间\\n",
#     "    BUY_PERIODS = [\\n",
#     "        ['00:00:00', '23:59:59']  # 可以开仓时间段为00:00:00 ~ 23:59:59\\n",
#     "    ]\\n",
#     "    # 可以执行平仓的时间\\n",
#     "    SELL_PERIODS = [\\n",
#     "        ['00:00:00', '23:59:59']  # 可以平仓时间段为00:00:00 ~ 23:59:59\\n",
#     "    ]\\n",
#     "    # 运行抛出的时间\\n",
#     "    THROW_PERIODS = []\\n",
#     "    # [最长订单时间（分钟）] ---------------------------------------------------\\n",
#     "    MAX_HOLD_ORDER_MINUTE = None\\n",
#     "    # [手续费率] -------------------------------------------------------------\\n",
#     "    # 开仓的手续费\\n",
#     "    BUY_COMMISSION_RATE = 0.00035  \\n",
#     "    # 平仓的手续费\\n",
#     "    SELL_COMMISSION_RATE = 0.00035  "
#    ]
#   },
#   {
#    "cell_type": "markdown",
#    "id": "9d1e9934",
#    "metadata": {},
#    "source": [
#     "##  Simulate"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "49d99812",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "class MySimulate(ptrade.Simulate):\\n",
#     "    \\n",
#     "    def setup(self):\\n",
#     "        # do something\\n",
#     "        pass\\n",
#     "\\n",
#     "    def buy(self):\\n",
#     "        # do something\\n",
#     "        pass\\n",
#     "    \\n",
#     "    def sell(self):\\n",
#     "        # do something\\n",
#     "        pass"
#    ]
#   },
#   {
#    "cell_type": "markdown",
#    "id": "f51d677e",
#    "metadata": {},
#    "source": [
#     "## Load Candle"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "7e20f53e",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "candle = ptrade.load.load_candle(\\n",
#     "    company = '【交易所】',\\n",
#     "    instType = '【产品类别】',\\n",
#     "    instId = '【产品ID】',\\n",
#     "    start = '【起始日期】',\\n",
#     "    end = '【终止日期】',\\n",
#     "    bar = '【时间粒度】',\\n",
#     ")"
#    ]
#   },
#   {
#    "cell_type": "markdown",
#    "id": "fcd5b23e",
#    "metadata": {},
#    "source": [
#     "## Run "
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "fd402462",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "ms = MySimulate(\\n",
#     "    candle = candle,\\n",
#     "    rule = Rule,\\n",
#     "    instId = None,\\n",
#     "    warn = True,\\n",
#     ")"
#    ]
#   },
#   {
#    "cell_type": "markdown",
#    "id": "aecd38a3",
#    "metadata": {},
#    "source": [
#     "## Analysis"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "ca41a7dc",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "# 完整历史交易数据\\n",
#     "df = ms.analysis.get_df()\\n",
#     "df.head()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "b6882cd1",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "df_by_position = ms.analysis.get_df_by_position(\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     ")\\n",
#     "df_by_position.head()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "9180a9eb",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "df_sequential_investment = ms.analysis.get_df_sequential_investment(\\n",
#     "    account_money=1000,  # 初始账户金额\\n",
#     "    invest_percentage=0.1,  # 投资金额比\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     ")\\n",
#     "df_sequential_investment.head()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "0c3c16d5",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "df_info_day = ms.analysis.get_df_process_info(\\n",
#     "    account_money=1000,  # 初始账户金额\\n",
#     "    period='day',  # 统计的单位时间段\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     ")\\n",
#     "df_info_day.head()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "8789944e",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "df_info_week = ms.analysis.get_df_process_info(\\n",
#     "    account_money=1000,  # 初始账户金额\\n",
#     "    period='week',  # 统计的单位时间段\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     ")\\n",
#     "df_info_week.head()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "834fc512",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "df_info_month= ms.analysis.get_df_process_info(\\n",
#     "    account_money=1000,  # 初始账户金额\\n",
#     "    period='month',  # 统计的单位时间段\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     ")\\n",
#     "df_info_month.head()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "id": "862d1eae",
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "df_info_all= ms.analysis.get_df_process_info(\\n",
#     "    account_money=1000,  # 初始账户金额\\n",
#     "    period='all',  # 统计的单位时间段\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     ")\\n",
#     "df_info_all.head()"
#    ]
#   }
#  ],
#  "metadata": {
#   "kernelspec": {
#    "display_name": "Python 3 (ipykernel)",
#    "language": "python",
#    "name": "python3"
#   },
#   "language_info": {
#    "codemirror_mode": {
#     "name": "ipython",
#     "version": 3
#    },
#    "file_extension": ".py",
#    "mimetype": "text/x-python",
#    "name": "python",
#    "nbconvert_exporter": "python",
#    "pygments_lexer": "ipython3",
#    "version": "3.8.4"
#   }
#  },
#  "nbformat": 4,
#  "nbformat_minor": 5
# }'''
#
# project_analysis_jupyter_content = '''{
#  "cells": [
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "import pandas as pd\\n",
#     "from ptrade.component.analysis import Analysis"
#    ]
#   },
#   {
#    "cell_type": "markdown",
#    "metadata": {},
#    "source": [
#     "## 读取交易数据"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "pycharm": {
#      "name": "#%%\\n"
#     }
#    },
#    "outputs": [],
#    "source": [
#     "filepath = './simulate.csv' # 数据路径\\n",
#     "df = pd.read_csv(filepath)\\n",
#     "df.head(2)"
#    ]
#   },
#   {
#    "cell_type": "markdown",
#    "metadata": {},
#    "source": [
#     "## 分析"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "pycharm": {
#      "name": "#%%\\n"
#     }
#    },
#    "outputs": [],
#    "source": [
#     "ans = Analysis()"
#    ]
#   },
#   {
#    "cell_type": "markdown",
#    "metadata": {},
#    "source": [
#     "### 按照仓位计算交易过程"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "pycharm": {
#      "name": "#%%\\n"
#     }
#    },
#    "outputs": [],
#    "source": [
#     "df_by_position = ans.get_df_by_position(\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     "    df=df,  # 数据\\n",
#     ")\\n",
#     "df_by_position.head()"
#    ]
#   },
#   {
#    "cell_type": "markdown",
#    "metadata": {},
#    "source": [
#     "### 按照等比投资计算交易过程"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "pycharm": {
#      "name": "#%%\\n"
#     }
#    },
#    "outputs": [],
#    "source": [
#     "df_sequential_investment = ans.get_df_sequential_investment(\\n",
#     "    account_money=1000,  # 初始账户金额\\n",
#     "    invest_percentage=0.1,  # 投资金额比\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     "    df=df,  # 数据\\n",
#     ")\\n",
#     "df_sequential_investment.head()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "### 按阶段分析交易过程数据"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "pycharm": {
#      "name": "#%%\\n"
#     }
#    },
#    "outputs": [],
#    "source": [
#     "df_info_day = ans.get_df_process_info(\\n",
#     "    account_money=1000,  # 初始账户金额\\n",
#     "    period='day',  # 统计的单位时间段\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     "    df=df,  # 数据\\n",
#     ")\\n",
#     "df_info_day.head()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "pycharm": {
#      "name": "#%%\\n"
#     }
#    },
#    "outputs": [],
#    "source": [
#     "df_info_week = ans.get_df_process_info(\\n",
#     "    account_money=1000,  # 初始账户金额\\n",
#     "    period='week',  # 统计的单位时间段\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     "    df=df,  # 数据\\n",
#     ")\\n",
#     "df_info_week.head()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "pycharm": {
#      "name": "#%%\\n"
#     }
#    },
#    "outputs": [],
#    "source": [
#     "df_info_month= ans.get_df_process_info(\\n",
#     "    account_money=1000,  # 初始账户金额\\n",
#     "    period='month',  # 统计的单位时间段\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     "    df=df,  # 数据\\n",
#     ")\\n",
#     "df_info_month.head()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "pycharm": {
#      "name": "#%%\\n"
#     }
#    },
#    "outputs": [],
#    "source": [
#     "df_info_all= ans.get_df_process_info(\\n",
#     "    account_money=1000,  # 初始账户金额\\n",
#     "    period='all',  # 统计的单位时间段\\n",
#     "    position=None,  # 最大总仓位\\n",
#     "    longPosition=None,  # 最大多仓位\\n",
#     "    shortPosition=None,  # 最大空仓位\\n",
#     "    df=df,  # 数据\\n",
#     ")\\n",
#     "df_info_all.head()"
#    ]
#   },
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {
#     "pycharm": {
#      "name": "#%%\\n"
#     }
#    },
#    "outputs": [],
#    "source": []
#   }
#  ],
#  "metadata": {
#   "kernelspec": {
#    "display_name": "Python 3 (ipykernel)",
#    "language": "python",
#    "name": "python3"
#   },
#   "language_info": {
#    "codemirror_mode": {
#     "name": "ipython",
#     "version": 3
#    },
#    "file_extension": ".py",
#    "mimetype": "text/x-python",
#    "name": "python",
#    "nbconvert_exporter": "python",
#    "pygments_lexer": "ipython3",
#    "version": "3.8.4"
#   }
#  },
#  "nbformat": 4,
#  "nbformat_minor": 1
# }'''
#
# project_rule_content = '''import ptrade.component.rule
#
#
# class MyRule(ptrade.component.rule.Rule):
#     # [交易规则] -----------------------------------------------------------
#     # T = 0 -> T0交易
#     # T = 1 -> T1交易 ...
#     T = 0
#     # [时区] --------------------------------------------------------------
#     TIMEZONE = 'Asia/Shanghai'
#     # TIMEZONE = 'America/New_York'
#     # [账户余额] -----------------------------------------------------------
#     ACCOUNT_MONEY = 1000
#     # [购买金额] -----------------------------------------------------------
#     # 单次开仓的默认金额占比
#     BUY_MONEY_RATE = None
#     # 单次开仓的默认金额
#     BUY_MONEY = 100
#     # [止盈止损] -----------------------------------------------------------
#     # 多单止盈，挂单价格
#     LONG_TP_RATE = None
#     # 多单止损，出发止损价格，以市价单平仓
#     LONG_SL_RATE = None
#     # 空单止盈，挂单价格
#     SHORT_TP_RATE = None
#     # 空单止损，出发止损价格，以市价单平仓
#     SHORT_SL_RATE = None
#     # [杠杆] ---------------------------------------------------------------
#     # 多单杠杆
#     LONG_LEVER = 1
#     # 空单杠杆
#     SHORT_LEVER = 1
#     # [仓位] ---------------------------------------------------------------
#     # 多单仓位
#     LONG_POSITION = 5
#     # 空单仓位
#     SHORT_POSITION = 5
#     # 总仓位
#     POSITION = 10
#     # [最长订单时间（分钟）] ---------------------------------------------------
#     # 可以执行开仓的时间
#     BUY_PERIODS = [
#         ['00:00:00', '23:59:59']  # 可以开仓时间段为00:00:00 ~ 23:59:59
#     ]
#     # 可以执行平仓的时间
#     SELL_PERIODS = [
#         ['00:00:00', '23:59:59']  # 可以平仓时间段为00:00:00 ~ 23:59:59
#     ]
#     # 运行抛出的时间
#     THROW_PERIODS = []
#     # [最长订单时间（分钟）] ---------------------------------------------------
#     MAX_HOLD_ORDER_MINUTE = None
#     # [手续费率] -------------------------------------------------------------
#     # 开仓的手续费
#     BUY_COMMISSION_RATE = 0.00035
#     # 平仓的手续费
#     SELL_COMMISSION_RATE = 0.00035'''
#
# project_simulate_content = '''import ptrade
# from rule import MyRule
#
#
# class MySimulate(ptrade.Simulate):
#     def __init__(
#             self,
#             candle,
#             rule,
#             instId: str = None,
#             warn: bool = True,
#     ):
#         super(MySimulate, self).__init__(candle, rule, instId, warn)
#
#     def setup(self):
#         # do something
#         pass
#
#     def buy(self):
#         # do something
#         pass
#
#     def sell(self):
#         # do something
#         pass
#
#
# if __name__ == '__main__':
#     # ------------------------------------------------------
#     instId = '【产品ID】'
#     load_candle_param = dict(
#         company='【交易所】',
#         instType='【产品类别】',
#         instId=instId,
#         start='【起始日期】',
#         end='【终止日期】',
#         bar='【时间粒度】',
#     )
#     filepath = './simulate.csv'  # 交易数据存储路径
#     # ------------------------------------------------------
#     candle = ptrade.load.load_candle(**load_candle_param)
#     ms = MySimulate(
#         candle=candle,
#         rule=MyRule,
#         instId=instId,
#         warn=True
#     )
#     ms.run()
#     df = ms.analysis.get_df()
#     df.to_csv(filepath)
#     print(df.head())'''
#
# project_simulate_multiply_content = '''import ptrade
# from rule import MyRule
# from simulate import MySimulate
#
#
#
# if __name__ == '__main__':
#     # ------------------------------------------------------
#     instIds = [] # 产品ID列表
#     load_candle_map_param = dict(
#         company='【交易所】',
#         instType='【产品类别】',
#         instIds=instIds,
#         start='【起始日期】',
#         end='【终止日期】',
#         bar='【时间粒度】',
#     )
#
#     filepath = './simulate_multiply.csv'  # 交易数据存储路径
#     # ------------------------------------------------------
#     candle_map = ptrade.load.load_candle_map(**load_candle_map_param)
#     sm = ptrade.SimulateMultiply(
#         Simulate=MySimulate,
#         candle_map=candle_map,
#         rule = MyRule,
#         warn= True
#     )
#     sm.run(p_num=4)
#     df = sm.analysis.get_df()
#     df.to_csv(filepath)
#     print(df.head())'''

# def execute():
#     commands = sys.argv
#     if len(commands) == 2 and commands[1].lower() == '--help':
#         msg = 'ptrade jupyter <name>    创建jupyter shortcuts\nptrade startproject <name>    创建 ptrade项目'
#         print(msg)
#     elif commands[1].lower() == 'jupyter':
#         filename = commands[2]
#         if not filename.endswith('.ipynb'):
#             filename = filename + '.ipynb'
#         with open(filename, 'w') as f:
#             f.write(simulate_jupyter_content)
#     elif commands[1].lower() == 'startproject':
#         dirname = commands[2]
#         if not os.path.isdir(dirname):
#             os.makedirs(dirname)
#         with open(os.path.join(dirname, 'analysis.ipynb'), 'w') as f:
#             f.write(project_analysis_jupyter_content)
#         with open(os.path.join(dirname, 'rule.py'), 'w') as f:
#             f.write(project_rule_content)
#         with open(os.path.join(dirname, 'simulate.py'), 'w') as f:
#             f.write(project_simulate_content)
#         with open(os.path.join(dirname, 'simulate_multiply.py'), 'w') as f:
#             f.write(project_simulate_multiply_content)

FILE = os.path.join(os.path.dirname(__file__), 'file')

with open(os.path.join(FILE, 'jupyter_content.ipynb'), 'r') as f:
    simulate_jupyter_content = f.read()

with open(os.path.join(FILE, 'project', 'analysis.ipynb'), 'r') as f:
    project_analysis_jupyter_content = f.read()

with open(os.path.join(FILE, 'project', 'rule.py'), 'r') as f:
    project_rule_content = f.read()

with open(os.path.join(FILE, 'project', 'simulate.py'), 'r') as f:
    project_simulate_content = f.read()

with open(os.path.join(FILE, 'project', 'simulate_multiply.py'), 'r') as f:
    project_simulate_multiply_content = f.read()


def execute():
    commands = sys.argv
    if len(commands) == 2 and commands[1].lower() == '--help':
        msg = 'ptrade jupyter <name>    创建jupyter shortcuts\nptrade startproject <name>    创建 ptrade项目'
        print(msg)
    elif commands[1].lower() == 'jupyter':
        filename = commands[2]
        if not filename.endswith('.ipynb'):
            filename = filename + '.ipynb'

        with open(filename, 'w') as f:
            f.write(simulate_jupyter_content)

    elif commands[1].lower() == 'startproject':
        dirname = commands[2]
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(os.path.join(dirname, 'analysis.ipynb'), 'w') as f:
            f.write(project_analysis_jupyter_content)
        with open(os.path.join(dirname, 'rule.py'), 'w') as f:
            f.write(project_rule_content)
        with open(os.path.join(dirname, 'simulate.py'), 'w') as f:
            f.write(project_simulate_content)
        with open(os.path.join(dirname, 'simulate_multiply.py'), 'w') as f:
            f.write(project_simulate_multiply_content)
