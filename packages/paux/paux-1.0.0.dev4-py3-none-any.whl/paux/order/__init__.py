from typing import Literal, Union
from paux import exception
import math


# 计算手续费
def get_commission_data(
        posSide: Literal['long', 'short'],
        buyMoney: Union[int, float],
        buyLine: Union[int, float],
        sellLine: Union[int, float],
        lever: Union[int, float],
        buyCommissionRate: Union[int, float],
        sellCommissionRate: Union[int, float]
):
    if posSide == 'long':
        buyCommission = buyMoney * lever * buyCommissionRate
        sellCommission = (sellLine / buyLine) * buyMoney * lever * sellCommissionRate
        commission = round(buyCommission + sellCommission, 4)
        sellMoney = round((sellLine - buyLine) / buyLine * lever * buyMoney + buyMoney - commission, 4)
        profitRate = round((sellMoney - buyMoney) / buyMoney, 4)
        return dict(
            sellMoney=sellMoney,
            commission=commission,
            profitRate=profitRate,
        )
    elif posSide == 'short':
        buyCommission = buyMoney * lever * buyCommissionRate
        sellCommission = (2 * buyLine - sellLine) / buyLine * buyMoney * lever * sellCommissionRate
        commission = round(buyCommission + sellCommission, 4)
        sellMoney = (buyLine - sellLine) / buyLine * buyMoney * lever + buyMoney - commission
        profitRate = round((sellMoney - buyMoney) / buyMoney, 4)
        return dict(
            sellMoney=sellMoney,
            commission=commission,
            profitRate=profitRate,
        )


def round_simulate(num):
    if num == 0:
        return num
    px_0_00001 = 0.00001 * num
    if px_0_00001 < 1:
        ndigits = len(str(int(1 / px_0_00001)))
        px_round = round(num, ndigits)
    else:
        px_round = round(num, 1)
    if abs((px_round - num) / num) >= 0.00001:
        raise Exception(
            'px_round={px_round},px={px}'.format(
                px_round=px_round,
                px=num
            )
        )
    else:
        return px_round


def round_floor(num, decimal: int = None, precise: Union[str, int, float] = None):
    if decimal != None:
        if decimal > 0:
            num_floor = math.floor(num * (10 ** decimal)) / (10 ** decimal)
            num_floor = round(num_floor, decimal)
        else:
            num_floor = math.floor(num)
    elif precise != None:
        precise = float(precise)
        decimal = len(str(round(1 / precise) - 1))
        num_floor = math.floor(num / precise) * precise
        if precise >= 1:
            num_floor = round(num_floor)
        else:
            num_floor = round(num_floor, decimal)
        if num_floor > num:
            error_msg = '数字向下取元整出错'
            raise exception.UnexpectError(error_msg)
        if num - num_floor >= precise:
            error_msg = '数字向下取元整出错'
            raise exception.UnexpectError(error_msg)
    else:
        error_msg = 'decimal和precise不能同时为空'
        raise exception.ParamException(error_msg)
    return num_floor


def round_up(num, decimal: int = None, precise: Union[str, int, float] = None):
    if decimal != None:
        if decimal > 0:
            num_up = math.ceil(num * (10 ** decimal)) / (10 ** decimal)
            num_up = round(num_up, decimal)
        else:
            num_up = math.ceil(num)
    elif precise != None:
        precise = float(precise)
        decimal = len(str(round(1 / precise) - 1))
        num_up = math.ceil(num / precise) * precise

        if precise >= 1:
            num_up = round(num_up)
        else:
            num_up = round(num_up, decimal)
        if num_up < num:
            error_msg = '数字向上取元整出错'
            raise exception.UnexpectError(error_msg)
        if num_up - num >= precise:
            error_msg = '数字向上取元整出错'
            raise exception.UnexpectError(error_msg)
    else:
        error_msg = 'decimal和precise不能同时为空'
        raise exception.ParamException(error_msg)
    return num_up


def to_f(num, decimal: int = None, precise: Union[int, float, str] = None, valid: bool = True):
    if decimal != None:
        pass
    elif precise != None:
        precise = float(precise)
        decimal = len(str(round(1 / precise) - 1))
    else:
        error_msg = 'decimal和precise不能同时为空'
        raise exception.ParamException(error_msg)
    fmt = '{:.' + f'{decimal}f' + '}'
    num_str = fmt.format(num)
    if valid:
        if float(num_str) != num:
            error_msg = '验证出错'
            raise exception.UnexpectError(error_msg)
    return num_str




# def to_f(num, valid: bool = True):
#     decimal_max = 30
#     fmt = '{:.' + f'{decimal_max}f' + '}'
#     num_str = fmt.format(num)
#     print(num_str)
#     decimal_str = num_str.split('.')[-1]
#     minus_decimal = 0
#     for s in decimal_str[::-1]:
#         if s == '0':
#             minus_decimal += 1
#         else:
#             break
#     fmt = '{:.' + '{decimal}f'.format(decimal=decimal_max - minus_decimal) + '}'
#     return fmt.format(num)


if __name__ == '__main__':
    import numpy as np

    # a = round_floor(num=123123.67287676767676767, decimal=0)
    # print(a)
    # precise = 11
    # a = round_floor(num=123123.6767676767676767, precise=precise)
    # print(a)
    # print(a / precise)
    # a = round_floor(num=0.1, precise=10)
    # print(a)

    # a = round_up(num=123123.67287676767676767, decimal=0)
    # print(a)
    precise = 0.00000000000000000000007
    a = round_up(num=0.00000000000000000123567, precise=precise)
    print(a)
    print(to_f(a,precise=precise))
    # print(a)
    # a = round_up(num=123123.6767676767676767, precise=0.01)
    # print(a)
    # a = round_up(num=0.1, precise=0.01)
