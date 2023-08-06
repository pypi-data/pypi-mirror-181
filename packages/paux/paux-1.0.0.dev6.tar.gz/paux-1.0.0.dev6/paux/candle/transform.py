'''
compress_candle     压缩历史K线
extract_candle      根据时间跨度截取candle
concat_candle       合并数据
to_candle       转换为candle数据
'''

import datetime
import numpy as np
from typing import Union

import pandas as pd

from paux import exception
from paux.candle import bar as _bar
from paux.candle import interval as _interval
from paux import date as _date


# 压缩历史K线
def compress_candle(
        candle: np.array,
        target_bar: str,
        org_bar: str = 'auto'
):
    '''
    :param candle: 历史K线数据
    :param target_bar: 目标K线的bar
    :param org_bar: 原始K线的bar
    :return:转换后的历史K线数据
        array([
            [ts,open,high,low,close,volume],
            [ts,open,high,low,close,volume],
            [ts,open,high,low,close,volume],
        ])
    example：
        将1Minute的K线数据转化成5Minute的K线数据
        transform_candle_by_bar(candle,target_bar='5m',org_bar='1m')

        将1Hour的K线数据转化成1Day的K线数据
        transform_candle_by_bar(candle,target_bar='1d',org_bar='1h'
    '''
    if org_bar == 'auto':
        org_bar = _bar.predict_bar(candle)
    # 目标K线ts间隔
    target_bar_interval = _interval.get_interval(target_bar)
    # 原始K线ts间隔
    org_tar_interval = _interval.get_interval(org_bar)
    # 压缩的数量
    compress_quantity = target_bar_interval / org_tar_interval
    if compress_quantity != int(compress_quantity):
        msg = "Can't transform candle from org_Bar({org_bar}) to target_bar{target_bar}".format(
            org_bar=org_bar,
            target_bar=target_bar,
        )
        raise exception.ParamException(msg)
    compress_quantity = int(compress_quantity)
    # 目标K线数据
    target_datas = []
    candle_shape = candle.shape
    for i in range(0, candle.shape[0], compress_quantity):
        if i + compress_quantity < candle_shape[0]:
            this_data = [
                candle[i, 0],  # ts
                candle[i, 1],  # open
                candle[i:i + compress_quantity, 2].max(),  # high
                candle[i:i + compress_quantity, 3].min(),  # low
                candle[i + compress_quantity - 1, 4],  # close
                candle[i:i + compress_quantity, 5].sum()  # volume
            ]
            # 如果有其他数据
            for i in range(6, candle_shape[1]):
                this_data.append(
                    candle[i:i + compress_quantity, i].sum()
                )
            target_datas.append(this_data)
    # 目标K线Candle
    target_candle = np.array(target_datas)
    return target_candle


# 根据时间跨度截取candle
def extract_candle(
        candle: np.array,
        start: Union[int, float, str, datetime.date, None],
        end: Union[int, float, str, datetime.date, None],
        timezone: Union[str, None] = None,
):
    '''
    :param candle:
    :param start:
    :param end:
    :param timezone:
    :return:
    '''
    start_ts = _date.to_ts(date=start, timezone=timezone, default=0)
    end_ts = _date.to_ts(date=end, timezone=timezone, default=9999 * 9999)
    return candle[candle[:, 0] >= start_ts and candle[:, 0] <= end_ts]


# 转换为candle数据
def to_candle(
        candle: Union[list, tuple, np.ndarray, pd.DataFrame],
        drop_duplicate: bool = True,
        sort: bool = True
):
    # list和tuple
    if isinstance(candle, list) or isinstance(candle, tuple):
        df = pd.DataFrame(candle)
    # DataFrame
    elif isinstance(candle, pd.DataFrame):
        df = candle
    # Array
    elif isinstance(candle, np.ndarray):
        df = pd.DataFrame(candle)
    # 未知类型
    else:
        error_msg = 'candles包含的数据类型应该是：list tuple DataFrame ndarray'
        raise exception.ParamException(error_msg)

    # 时间序列的名字
    ts_column_name = df.columns[0]
    # 时间戳转化为整数
    df[ts_column_name] = df[ts_column_name].astype(int)
    # 去重
    if drop_duplicate:
        df = df.drop_duplicates(subset=ts_column_name)
    # 排序
    if sorted:
        df = df.sort_values(by=ts_column_name)
    # 转化为array对象
    candle = df.to_numpy()
    return candle


# 合并数据
def concat_candle(
        candles: list,
        drop_duplicate: bool = True,
        sort: bool = True
):
    for i in range(len(candles)):
        # list和tuple
        if isinstance(candles[i], list) or isinstance(candles[i], tuple):
            candles[i] = pd.DataFrame(candles[i])
        # DataFrame
        elif isinstance(candles[i], pd.DataFrame):
            pass
        # Array
        elif isinstance(candles[i], np.ndarray):
            candles[i] = pd.DataFrame(candles[i])
        # 未知类型
        else:
            error_msg = 'candles包含的数据类型应该是：list tuple DataFrame ndarray'
            raise exception.ParamException(error_msg)
    # 拼接数据
    df = pd.concat(candles)
    candle = to_candle(candle=df, drop_duplicate=drop_duplicate, sort=sort)
    return candle


# 根据日期，得到K线中的索引
def get_candle_index_by_date(
        candle: np.array,
        date: Union[datetime.datetime, int, float, str,],
        timezone: str = None,
        default: int = 0
):
    if not date:
        return default
    ts = _date.to_ts(date=date, timezone=timezone, default=default)
    index = np.where(
        candle[:, 0] == ts
    )[0][0]
    return index


if __name__ == '__main__':
    pass
