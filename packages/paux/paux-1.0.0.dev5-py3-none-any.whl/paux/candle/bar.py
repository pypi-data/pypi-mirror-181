import numpy as np
from paux import exception

# 估计K线中的时间粒度
def predict_bar(candle: np.array, MINUTE_BAR_INTERVAL=60000) -> str:
    '''
    :param candle: np.array
    :return: bar
    '''
    bar_interval = np.min(np.diff(candle[:, 0]))
    bar_int = bar_interval / MINUTE_BAR_INTERVAL
    if bar_int <= 59:
        suffix = 'm'
        bar_int = bar_int
    elif bar_int <= 60 * 23:
        suffix = 'h'
        bar_int = bar_int / 60
    else:
        bar_int = bar_int / 60 * 24
        suffix = 'd'

    if not bar_int == int(bar_int):
        raise exception.ParamException('Unable to predict bar')
    return '{bar_int}{suffix}'.format(bar_int=int(bar_int), suffix=suffix)


if __name__ == '__main__':
    pass
