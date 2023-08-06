'''
load_candle_by_date | load_candle     按照日期读取指定产品的历史K线

company         str                             交易所 OKX BINANCE HUOBI IB TDA EAST_MONEY
instType        str                             产品类别
instId          str                             产品ID
start           int|float|str|datetime.date     起始日期时间
end             int|float|str|datetime.date     终止日期时间
base_dir        str|None                        数据存储文件夹，默认为None，使用paux中settings的交易所K线路径
timezone        str|None                        时区，默认为None，使用paux中settings的交易所K线时区
bar             str                             时间粒度
valid_interval  bool                            是否验证K线间隔
valid_start     bool                            是否验证K线时间起点必须等于start
valid_end       bool                            是否验证K线时间终点必须等于end
minus_bar       int                             去掉历史K线结尾N个时间粒度，默认为1，表示不包含end时刻的K线数据

load_candle_map_by_date | load_candle_map       按照日期读取多个产品的历史K线

company         str                             交易所 OKX BINANCE HUOBI IB TDA EAST_MONEY
instType        str                             产品类别
instIds         list                            产品ID，instIds=[]，表示读取产品类别中数据完整的全部产品Id
start           int|float|str|datetime.date     起始日期时间
end             int|float|str|datetime.date     终止日期时间
base_dir        str|None                        数据存储文件夹，默认为None，使用paux中settings的交易所K线路径
timezone        str|None                        时区，默认为None，使用paux中settings的交易所K线时区
bar             str                             时间粒度
valid_interval  bool                            是否验证K线间隔
valid_start     bool                            是否验证K线时间起点必须等于start
valid_end       bool                            是否验证K线时间终点必须等于end
minus_bar       int                             去掉历史K线结尾N个时间粒度，默认为1，表示不包含end时刻的K线数据
'''

import datetime
from typing import Union, Literal

from paux.candle.history import candle_okx
from paux.candle.history import candle_binance
from paux.candle.history import candle_huobi
from paux.candle.history import candle_ib
from paux.candle.history import candle_tda
from paux.candle.history import candle_east_money
import paux.settings

settings = paux.settings.read_settings()

COMPANY_MAP = {
    'OKX': {
        'module': candle_okx,
        'base_dir': settings['CANDLE_OKX_BASE_DIR'],
        'timezone': settings['CANDLE_OKX_TIMEZONE'],
    },
    'BINANCE': {
        'module': candle_binance,
        'base_dir': settings['CANDLE_BINANCE_BASE_DIR'],
        'timezone': settings['CANDLE_BINANCE_TIMEZONE'],
    },
    'HUOBI': {
        'module': candle_huobi,
        'base_dir': settings['CANDLE_HUOBI_BASE_DIR'],
        'timezone': settings['CANDLE_HUOBI_TIMEZONE'],
    },
    'IB': {
        'module': candle_ib,
        'base_dir': settings['CANDLE_IB_BASE_DIR'],
        'timezone': settings['CANDLE_IB_TIMEZONE'],
    },
    'TDA': {
        'module': candle_tda,
        'base_dir': settings['CANDLE_TDA_BASE_DIR'],
        'timezone': settings['CANDLE_TDA_TIMEZONE'],
    },
    'EAST_MONEY': {
        'module': candle_east_money,
        'base_dir': settings['CANDLE_EAST_MONEY_BAST_DIR'],
        'timezone': settings['CANDLE_EAST_MONEY_TIMEZONE'],
    },
}


# 按照日期读取指定产品的历史K线
def load_candle_by_date(
        company: Literal['OKX', 'BINANCE', 'HUOBI', 'IB', 'TDA', 'EAST_MONEY'],
        instType: str,
        instId: str,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: Union[str, None] = None,
        timezone: Union[str, None] = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_interval=True,
        valid_start=True,
        valid_end=True,
        minus_bar: int = 1,
):
    '''
        company         str                             交易所 OKX BINANCE HUOBI IB TDA EAST_MONEY
        instType        str                             产品类别
        instId          str                             产品ID
        start           int|float|str|datetime.date     起始日期时间
        end             int|float|str|datetime.date     终止日期时间
        base_dir        str|None                        数据存储文件夹，默认为None，使用paux中settings的交易所K线路径
        timezone        str|None                        时区，默认为None，使用paux中settings的交易所K线时区
        bar             str                             时间粒度
        valid_interval  bool                            是否验证K线间隔
        valid_start     bool                            是否验证K线时间起点必须等于start
        valid_end       bool                            是否验证K线时间终点必须等于end
        minus_bar       int                             去掉历史K线结尾N个时间粒度，默认为1，表示不包含end时刻的K线数据

        如果instIds = []，读取的产品类型中的全部产品ID后，会进行过滤，仅保留从start~end中均有数据的产品ID
    '''
    module = COMPANY_MAP[company.upper()]['module']
    if base_dir == None:
        base_dir = COMPANY_MAP[company.upper()]['base_dir']
    if timezone == None:
        timezone = COMPANY_MAP[company.upper()]['timezone']
    return module.load_candle_by_date(
        instType=instType,
        instId=instId,
        start=start,
        end=end,
        base_dir=base_dir,
        timezone=timezone,
        bar=bar,
        valid_interval=valid_interval,
        valid_start=valid_start,
        valid_end=valid_end,
        minus_bar=minus_bar,
    )


# 按照日期读取多个产品的历史K线
def load_candle_map_by_date(
        company: Literal['OKX', 'BINANCE', 'HUOBI', 'IB', 'TDA', 'EAST_MONEY'],
        instType: str,
        instIds: list,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: Union[str, None] = None,
        timezone: Union[str, None] = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        p_num=4,
        valid_interval=True,
        valid_start=True,
        valid_end=True,
        minus_bar: int = 1,
):
    '''
        company         str                             交易所 OKX BINANCE HUOBI IB TDA EAST_MONEY
        instType        str                             产品类别
        instIds         list                            产品ID，instIds=[]，表示读取产品类别中数据完整的全部产品Id
        start           int|float|str|datetime.date     起始日期时间
        end             int|float|str|datetime.date     终止日期时间
        base_dir        str|None                        数据存储文件夹，默认为None，使用paux中settings的交易所K线路径
        timezone        str|None                        时区，默认为None，使用paux中settings的交易所K线时区
        bar             str                             时间粒度
        valid_interval  bool                            是否验证K线间隔
        valid_start     bool                            是否验证K线时间起点必须等于start
        valid_end       bool                            是否验证K线时间终点必须等于end
        minus_bar       int                             去掉历史K线结尾N个时间粒度，默认为1，表示不包含end时刻的K线数据
    '''
    module = COMPANY_MAP[company.upper()]['module']
    if base_dir == None:
        base_dir = COMPANY_MAP[company.upper()]['base_dir']
    if timezone == None:
        timezone = COMPANY_MAP[company.upper()]['timezone']
    return module.load_candle_map_by_date(
        instType=instType,
        instIds=instIds,
        start=start,
        end=end,
        base_dir=base_dir,
        timezone=timezone,
        bar=bar,
        p_num=p_num,
        valid_interval=valid_interval,
        valid_start=valid_start,
        valid_end=valid_end,
        minus_bar=minus_bar,
    )


# for shortcuts
load_candle = load_candle_by_date
load_candle_map = load_candle_map_by_date
