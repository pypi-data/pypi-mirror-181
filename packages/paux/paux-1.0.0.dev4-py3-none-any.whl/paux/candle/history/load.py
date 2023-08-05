import os
import pandas as pd
import datetime
from typing import Union, Literal
from paux.candle.history import lite as _lite
from paux.candle import transform as _transform
from paux.candle import valid as _valid
from paux.candle import interval as _interval
from paux import param as _param
from paux import process as _process
from paux import date as _date
from paux import exception


# 读取candle
def load_candle_by_date(
        instType: str,
        instId: str,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_interval=True,
        valid_start=True,
        valid_end=True,
        minus_bar=1,
):
    if minus_bar:
        end = _date.to_ts(end, timezone) - _interval.get_interval(bar=bar) * minus_bar
    # 检查是否有数据
    if not _lite.check_candle_day_path(
            instType=instType, instId=instId, start=start,
            end=end, timezone=timezone, bar=bar, base_dir=base_dir
    ):
        error_msg = 'candle数据不足'
        raise exception.CandleFileError(error_msg)

    # 获取数据的序列
    date_range = _date.get_range_dates(
        start=start,
        end=end,
        timezone=timezone,
    )
    # 获取数据的路径列表
    paths = [
        _lite.get_candle_day_path(
            instType=instType,
            instId=instId,
            date=date,
            timezone=timezone,
            bar=bar,
            base_dir=base_dir,
        )
        for date in date_range
    ]
    # 读取数据
    dfs = []
    for path in paths:
        df = pd.read_csv(path)
        dfs.append(df)
    # 合并数据
    candle = _transform.concat_candle(candles=dfs, drop_duplicate=True, sort=True)
    if valid_interval and not _valid.valid_interval(candle, bar=bar):
        msg = '{instId}的candle的时间间隔错误'.format(instId=instId)
        raise exception.CandleDiffError(msg)
    if valid_start and not _valid.valid_start(candle=candle, start=start, timezone=timezone):
        msg = '{instId}的candle的时间起始错误'.format(instId=instId)
        raise exception.CandleStartError(msg)
    end = _date.to_datetime(end, timezone)
    if valid_end and not _valid.valid_end(candle=candle, end=end, timezone=timezone):
        msg = '{instId}的candle的时间终止错误'.format(instId=instId)
        raise exception.CandleEndError(msg)
    return candle


'''
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str,
        timezone: str = None,
'''


# 按照日期读取candle_map
def load_candle_map_by_date(
        instType: str,
        instIds: list,
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        base_dir: str,
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        contains='-USDT',
        p_num=4,
        valid_interval=True,
        valid_start=True,
        valid_end=True,
        minus_bar=1,
):
    if minus_bar:
        end = _date.to_ts(end, timezone) - _interval.get_interval(bar=bar) * minus_bar
    # 如果没有产品的名字，获取产品类型数据中，有start_date到end_date中有完整数据的instId
    if not instIds:
        dates = _date.get_range_dates(start=start, end=end, timezone=timezone)
        instIds = set()
        for date in dates:
            date_dirpath = os.path.dirname(
                _lite.get_candle_day_path(
                    base_dir=base_dir, instType=instType, timezone=timezone,
                    date=date, bar=bar, instId=''
                )
            )
            this_instIds = []
            for filename in os.listdir(date_dirpath):
                instId = filename.rsplit('.', maxsplit=1)[0]
                if contains and not contains in instId:
                    continue
                else:
                    this_instIds.append(instId)
            if not instIds:
                instIds = set(this_instIds)
            else:
                instIds = instIds & set(this_instIds)
    instIds = list(instIds)
    candle_map = {}
    if p_num > 1:
        params = []
        for instId in instIds:
            params.append(
                dict(
                    instType=instType,
                    instId=instId,
                    start=start,
                    end=end,
                    timezone=timezone,
                    bar=bar,
                    base_dir=base_dir,
                    valid_interval=valid_interval,
                    valid_start=valid_start,
                    valid_end=valid_end,
                    minus_bar=0,
                )
            )
        results = _process.pool_worker(
            params=params,
            p_num=p_num,
            func=load_candle_by_date,
            skip_exception=False,
        )
        for i, result in enumerate(results):
            if _param.isnull(result):
                continue
            instId = instIds[i]
            candle_map[instId] = result

    else:
        for instId in instIds:
            candle_map[instId] = load_candle_by_date(
                instType=instType,
                instId=instId,
                start=start,
                end=end,
                timezone=timezone,
                bar=bar,
                base_dir=base_dir,
                valid_interval=valid_interval,
                valid_start=valid_start,
                valid_end=valid_end,
            )
    # candle_map排序
    candle_map_sorted = {}
    instIds = sorted([instId for instId in candle_map.keys()])
    for instId in instIds:
        candle_map_sorted[instId] = candle_map[instId]

    for instId, candle in candle_map_sorted.items():
        if valid_interval and not _valid.valid_interval(candle, bar=bar):
            msg = '{instId}的candle的时间间隔错误'.format(instId=instId)
            raise exception.CandleDiffError(msg)
        if valid_start and not _valid.valid_start(candle=candle, start=start, timezone=timezone):
            msg = '{instId}的candle的时间起始错误'.format(instId=instId)
            raise exception.CandleStartError(msg)
        if valid_end and not _valid.valid_end(candle=candle, end=end, timezone=timezone):
            msg = '{instId}的candle的时间终止错误'.format(instId=instId)
            raise exception.CandleEndError(msg)
    return candle_map_sorted


# 通过文件地址读取Candle
def load_candle_by_file(
        instType: str,
        instId: str,
        path: str = None,
        base_dir: str = '',
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_interval: bool = True,
):
    '''
    如果有path路径，按照path路径读取文件
    如果没有path路径，按照base_dir、instId、instType、bar和timezone计算产品路径
    '''
    if path == None:
        path = _lite.get_candle_file_path(
            instType=instType,
            instId=instId,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir,
        )
    df = pd.read_csv(path)
    candle = _transform.to_candle(candle=df, drop_duplicate=True, sort=True)
    if valid_interval and not _valid.valid_interval(candle, bar=bar):
        msg = '{instId}的candle的时间间隔错误'.format(instId=instId)
        return exception.CandleDiffError(msg)
    return candle


# 通过文件夹地址读取Candle_map
def load_candle_map_by_file(
        instType: str,
        instIds: list = [],
        path: str = None,
        base_dir: str = '',
        timezone: str = None,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_interval: bool = True,

):
    # 如果没有文件夹的地址
    if path == None:
        path = os.path.dirname(
            _lite.get_candle_file_path(
                instType=instType,
                base_dir=base_dir,
                timezone=timezone,
                bar=bar,
                instId='xx',
            )
        )
    # 如果没有产品的名字，读取文件夹中全部的产品
    if not instIds:
        filenames = os.listdir(path)
        instIds = []
        for filename in filenames:
            instId = filename.rsplit('.', maxsplit=1)[0]
            instIds.append(instId)
    # 读取数据
    candle_map = {}
    for instId in instIds:
        candle = load_candle_by_file(
            instId=instId,
            instType=instType,
            base_dir=base_dir,
            timezone=timezone,
            bar=bar,
            valid_interval=valid_interval
        )
        candle_map[instId] = candle
    # candle_map排序
    candle_map_sorted = {}
    instIds = sorted([instId for instId in candle_map.keys()])
    for instId in instIds:
        candle_map_sorted[instId] = candle_map[instId]
    return candle_map_sorted
