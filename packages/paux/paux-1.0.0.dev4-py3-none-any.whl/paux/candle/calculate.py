import numpy as np
from paux import exception

'''
计算多种金融指标数据
'''


def history_suc(posSide,candle,buyLine,sellLine):
    this_order_index = 0
    suc_num = 0
    if posSide == 'long':
        while True:
            for index in range(this_order_index, candle.shape[0]):
                if candle[index, 3] <= buyLine:
                    this_order_index = index
                    break
                this_order_index = index
            for index in range(this_order_index + 1, candle.shape[0]):
                if candle[index, 2] >= sellLine:
                    this_order_index = index + 1
                    suc_num += 1
                    break
                this_order_index = index
            if this_order_index >= candle.shape[0] - 1:
                break
        return suc_num
    elif posSide == 'short':
        while True:
            for index in range(this_order_index, candle.shape[0]):
                if candle[index, 2] >= buyLine:
                    this_order_index = index
                    break
                this_order_index = index
            for index in range(this_order_index + 1, candle.shape[0]):
                if candle[index, 3] <= sellLine:
                    this_order_index = index + 1
                    suc_num += 1
                    break
                this_order_index = index
            if this_order_index >= candle.shape[0] - 1:
                break
        return suc_num
    else:
        raise exception.ParamException('posSide 应该为long或short')

# 得到均线
def get_candle_ma(
        candle: np.array,
        n: int
):
    '''
    获取历史均线

    :param candle:历史K线数据
    :param n:间隔
    :return:
        array([
                [ts,mac],
                [ts.mac],
                [ts.mac],
            ])
    '''
    # 均线数据
    mac_datas = []
    candle_shape = candle.shape
    for index in range(candle_shape[0]):
        if index < n - 1:
            this_data = [candle[index, 0]] + [np.nan] * (candle_shape[1] - 1)
            mac_datas.append(
                this_data
            )
        else:
            this_data = [candle[index, 0]] + candle[index - n + 1:index + 1, 1:].mean(axis=0).tolist()
            mac_datas.append(
                this_data
            )
    # 均线Candle
    mac_candle = np.array(mac_datas)
    return mac_candle


# 得到布林带
def get_candle_boll(
        candle: np.array,
        n: int
):
    '''
    获取布林带

    :param candle:历史K线数据
    :param n:间隔
    :return:
        array([
            [ts,mb,up,dn],
            [ts,mb,up,dn],
            [ts,mb,up,dn],
        ])
        (mb:均线 up:上轨 dn:下轨)
    '''
    # 布林带数据
    boll_datas = []
    for index in range(candle.shape[0]):
        if index <= n - 1:
            mb = np.nan
            up = np.nan
            dn = np.nan
        else:
            mb = candle[index - n:index, 4].mean()  # 收盘价均值
            sd = (candle[index - n:index, 4] - mb).std()  # 收盘价标准差
            up = mb + 2 * sd  # 上轨
            dn = mb - 2 * sd  # 下轨
        boll_datas.append(
            [candle[index, 0], mb, up, dn]
        )
    # 布林带Candle
    boll_candle = np.array(boll_datas)
    return boll_candle


# 得到DualThrust中的上轨和下轨
def get_candle_dualThrust(
        candle: np.array,
        n: int,
        ks: float,
        kx: float,
        update_n: int = None
):
    '''
    获取DualThrust Candle

    :param candle:历史K线数据
    :param n:间隔
    :param ks:ks参数
    :param kx:kx参数
    :param update_n:更新的间隔n
    :return:
        array([
            [ts,range_ks,range_kx],
            [ts,range_ks,range_kx],
            [ts,range_ks,range_kx],
        ])
        (range_ks上轨 range_kx下轨)
    '''
    # dualThrust数据
    dualThrust_datas = []
    for i in range(0, candle.shape[0], update_n):
        if i <= n - 1:
            range_kx = np.nan
            range_ks = np.nan
        else:
            last_k_array = candle[i - n:i]  # 前n间隔的数据
            hh = last_k_array[:, 2].max()  # 最高价的最高价
            hc = last_k_array[:, 4].max()  # 最高价的收盘价
            lc = last_k_array[:, 4].min()  # 最低价的收盘价
            ll = last_k_array[:, 3].min()  # 最低价的最低价
            range_ = max(hh - lc, hc - ll)
            o = candle[i, 1]
            range_ks = o + ks * range_  # 上轨
            range_kx = o - kx * range_  # 下轨
        for ts in candle[i:i + update_n, 0]:
            dualThrust_datas.append(
                [ts, range_ks, range_kx]
            )
    # dualThrust Candle
    dualThrust_candle = np.array(dualThrust_datas)
    return dualThrust_candle
