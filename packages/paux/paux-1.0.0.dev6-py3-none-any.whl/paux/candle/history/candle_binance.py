import datetime
import numpy as np
from paux import settings
from paux.candle.history import load as _load
from paux.candle.history import save as _save
from paux import param as _param
from typing import Literal, Union

settings_data = settings.read_settings()

__CANDLE_BASE_DIR = settings_data['CANDLE_BINANCE_BASE_DIR']
__CANDLE_TIMEZONE = settings_data['CANDLE_BINANCE_TIMEZONE']


# 读取candle
def load_candle_by_date(
        instType: str,
        instId: str,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir:str =__CANDLE_BASE_DIR,
        timezone: str = __CANDLE_TIMEZONE,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_interval=True,
        valid_start=True,
        valid_end=True,
        minus_bar:int = 1,
):
    return _load.load_candle_by_date(**_param.to_local(locals()))


# 按照日期读取candle_map
def load_candle_map_by_date(
        instType: str,
        instIds: list,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str = __CANDLE_BASE_DIR,
        timezone: str = __CANDLE_TIMEZONE,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        contains='-USDT',
        p_num=4,
        valid_interval=True,
        valid_start=True,
        valid_end=True,
        minus_bar:int = 1,
):
    return _load.load_candle_map_by_date(**_param.to_local(locals()))


# 通过文件地址读取Candle
def load_candle_by_file(
        instType: str,
        instId: str,
        path: str = None,
        base_dir: str = __CANDLE_BASE_DIR,
        timezone: str = __CANDLE_TIMEZONE,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_interval: bool = True,
):
    return _load.load_candle_by_file(**_param.to_local(locals()))


# 通过文件夹地址读取Candle_map
def load_candle_map_by_file(
        instType: str,
        instIds: list = [],
        path: str = None,
        base_dir: str = __CANDLE_BASE_DIR,
        timezone: str = __CANDLE_TIMEZONE,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_interval: bool = True,

):
    return _load.load_candle_map_by_file(**_param.to_local(locals()))


# 按照日期保存Candle
def save_candle_by_date(
        candle: np.array,
        instType: str,
        instId: str,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str = __CANDLE_BASE_DIR,
        timezone: str = __CANDLE_TIMEZONE,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        drop_duplicate: bool = True,
        sort: bool = True,
        valid_interval: bool = True,
        valid_start: bool = True,
        valid_end: bool = True,
        minus_bar:int = 1,
):
    return _save.save_candle_by_date(**_param.to_local(locals()))


# 按照日期保存candle_map
def save_candle_map_by_date(
        candle_map: dict,
        instType: str,
        instIds: list,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str = __CANDLE_BASE_DIR,
        timezone: str = __CANDLE_TIMEZONE,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        drop_duplicate: bool = True,
        sort: bool = True,
        valid_interval: bool = True,
        valid_start: bool = True,
        valid_end: bool = True,
        minus_bar:int = 1,
):
    return _save.save_candle_map_by_date(**_param.to_local(locals()))


# 按照文件地址保存Candle
def save_candle_by_file(
        candle: np.array,
        instType: str,
        instId: str,
        path: str = None,
        base_dir: str = __CANDLE_BASE_DIR,
        timezone: str = __CANDLE_TIMEZONE,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        sort=True,
        drop_duplicate=True,
        valid_interval=True,
):
    return _save.save_candle_by_file(**_param.to_local(locals()))


# 按照文件地址保存Candle_map
def save_candle_map_by_file(
        candle_map: dict,
        instType: str,
        instIds: list,
        base_dir: str = __CANDLE_BASE_DIR,
        timezone: str = __CANDLE_TIMEZONE,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        sort: bool = True,
        drop_duplicate: bool = True,
        valid_interval: bool = True,
):
    return _save.save_candle_map_by_file(**_param.to_local(locals()))
