import numpy as np
from paux import exception

# 得到时间间隔，单位毫秒
def get_interval(bar: str, MINUTE_BAR_INTERVAL=60000) -> float:
    '''

    Get ts interval by bar

    :param bar:
    Time interval of historical k line
        bar = '1m'  1 minute
        bar = '5m'  5 minute
        bar = '1h'  1 hour
        bar = '1d'  1 day
        ... ...

    :param MINUTE_BAR_INTERVAL:
    Number interval per minute, in milliseconds
        MINUTE_BAR_INTERVAL = 60000    Ts is in milliseconds
        MINUTE_BAR_INTERVAL = 60       Ts is in seconds

    :return: interval
    '''
    bar_int = int(bar[0:-1].strip())
    suffix = bar[-1].lower()
    if suffix == 'm':
        interval = MINUTE_BAR_INTERVAL * bar_int
    elif suffix == 'h':
        interval = MINUTE_BAR_INTERVAL * 60 * bar_int
    elif suffix == 'd':
        interval = MINUTE_BAR_INTERVAL * 60 * 24 * bar_int
    elif suffix == 'w':
        interval = MINUTE_BAR_INTERVAL * 60 * 24 * 7 * bar_int
    else:
        raise exception.ParamException(
            "The format of bar should be like ['1m ',' 2m ',' 1h ',' 2h ',' 1d ',' 2d '...]"
        )
    return interval


# 估计K线中的时间粒度间隔
def predict_interval(candle: np.array) -> float:
    '''

    Predict ts interval by candle

    :param candle: History Candle
        array[
            [ts,open,high,low,close,volume],
            [ts,open,high,low,close,volume],
            [ts,open,high,low,close,volume],
        ]

    :return:interval
    '''
    return np.min(np.diff(candle[:, 0]))