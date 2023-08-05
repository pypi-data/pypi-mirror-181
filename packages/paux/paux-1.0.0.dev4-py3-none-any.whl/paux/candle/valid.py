import datetime
import pandas as pd
import numpy as np
from paux import date as _date
from paux.candle import interval as _interval
from typing import Union


# 验证数据间隔
def valid_interval(candle: np.array, interval: Union[int, float] = None, bar: str = None, MINUTE_BAR_INTERVAL=60000):
    if pd.isnull(interval):
        interval = _interval.get_interval(bar=bar, MINUTE_BAR_INTERVAL=MINUTE_BAR_INTERVAL)
    return (np.diff(candle[:, 0]) == interval).all()


# 验证数据的起始时间
def valid_start(candle: np.array, start: Union[int, float, str, datetime.date], timezone: str = None):
    ts = _date.to_ts(date=start, timezone=timezone, default=np.nan)
    if candle[0, 0] == ts:
        return True
    else:
        return False


# 验证数据的终止时间
def valid_end(candle: np.array, end: Union[int, float, str, datetime.date], timezone: str = None):
    ts = _date.to_ts(date=end, timezone=timezone, default=np.nan)
    if candle[-1, 0] == ts:
        return True
    else:
        return False
