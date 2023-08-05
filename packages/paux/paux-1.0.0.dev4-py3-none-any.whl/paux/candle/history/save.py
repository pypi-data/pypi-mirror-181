import os
import numpy as np
import pandas as pd
import datetime
from typing import Union, Literal
from paux.candle.history import lite as _lite
from paux.candle import transform as _transform
from paux.candle import valid as _valid
from paux.candle import interval as _interval
from paux import date as _date
from paux import exception


# 按照日期保存Candle
def save_candle_by_date(
        candle: np.array,
        instType: str,
        instId: str,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        drop_duplicate: bool = True,
        sort: bool = True,
        valid_interval: bool = True,
        valid_start: bool = True,
        valid_end: bool = True,
        minus_bar=1,
):
    '''
    边按照日期写入，边进行valid，如果valid报告错误，之前的数据可以成功写入，后面的数据则不会继续写入
    '''
    if minus_bar:
        end = _date.to_ts(end, timezone) - _interval.get_interval(bar=bar) * minus_bar
    # 如果需要去重或者需要排序
    if drop_duplicate or sort:
        candle = _transform.to_candle(candle, drop_duplicate=True, sort=True)
    dates = _date.get_range_dates(start=start, end=end, timezone=timezone)
    # 验证数据
    for date in dates:
        start_ts = _date.to_ts(date=date, timezone=timezone)
        end_ts = start_ts + 1000 * 60 * 60 * 24 - _interval.get_interval(bar=bar)
        candle_date = candle[
            (candle[:, 0] >= start_ts) & (candle[:, 0] <= end_ts)
            ]
        if valid_interval and not _valid.valid_interval(candle_date, bar=bar):
            msg = '{instId}的candle的时间间隔错误'.format(instId=instId)
            raise exception.CandleDiffError(msg)
        if valid_start and not _valid.valid_start(candle=candle_date, start=start_ts, timezone=timezone):
            msg = '{instId}的candle的时间起始错误'.format(instId=instId)
            raise exception.CandleStartError(msg)
        if valid_end and not _valid.valid_end(candle=candle_date, end=end_ts, timezone=timezone):
            msg = '{instId}的candle的时间终止错误'.format(instId=instId)
            raise exception.CandleEndError(msg)
        path = _lite.get_candle_day_path(
            instType=instType,
            instId=instId,
            date=date,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir
        )
        dirpath = os.path.dirname(path)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        df_date = pd.DataFrame(candle_date)
        df_date.to_csv(path, index=False)
    return True


# 按照日期保存candle_map
def save_candle_map_by_date(
        candle_map: dict,
        instType: str,
        instIds: list,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str = '',
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        drop_duplicate: bool = True,
        sort: bool = True,
        valid_interval: bool = True,
        valid_start: bool = True,
        valid_end: bool = True,
        minus_bar=1,
):
    '''
    如果写入的时候出现了错误，报错之前写入成功，报错后面的则不能正常写入
    '''
    if minus_bar:
        end = _date.to_ts(end, timezone) - _interval.get_interval(bar=bar) * minus_bar
    if not instIds:
        instIds = [instId for instId in candle_map.keys()]
    for instId in instIds:
        candle = candle_map[instId]
        save_candle_by_date(
            instType=instType,
            instId=instId,
            candle=candle,
            start=start,
            end=end,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir,
            drop_duplicate=drop_duplicate,
            sort=sort,
            valid_interval=valid_interval,
            valid_start=valid_start,
            valid_end=valid_end,
            minus_bar=minus_bar
        )


# 按照文件地址保存Candle
def save_candle_by_file(
        candle: np.array,
        instType: str,
        instId: str,
        path: str = None,
        base_dir='',
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        sort=True,
        drop_duplicate=True,
        valid_interval=True,
):
    # 验证间隔
    if valid_interval and not _valid.valid_interval(candle=candle, bar=bar):
        msg = '{instId}的candle的时间间隔错误'.format(instId=instId)
        raise exception.CandleDiffError(msg)
    # 得到路径
    if path == None:
        path = _lite.get_candle_file_path(
            instType=instType,
            instId=instId,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir,
        )
    # 排序与去重
    if sort or valid_interval:
        candle = _transform.to_candle(candle=candle, drop_duplicate=drop_duplicate, sort=sort)
    # 文件夹与路径
    dirpath = os.path.dirname(path)
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    df = pd.DataFrame(candle)
    # 写入文件
    df.to_csv(path, index=False)


# 按照文件地址保存Candle_map
def save_candle_map_by_file(
        candle_map: dict,
        instType: str,
        instIds: list,
        base_dir: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        sort: bool = True,
        drop_duplicate: bool = True,
        valid_interval: bool = True,
):
    if not instIds:
        instIds = [instId for instId in candle_map.keys()]

    for instId in instIds:
        candle = candle_map[instId]
        save_candle_by_file(
            candle=candle,
            instType=instType,
            instId=instId,
            path=None,
            base_dir=base_dir,
            timezone=timezone,
            bar=bar,
            sort=sort,
            drop_duplicate=drop_duplicate,
            valid_interval=valid_interval,
        )
