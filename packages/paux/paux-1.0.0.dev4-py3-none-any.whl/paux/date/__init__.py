import pendulum
import datetime
import re
import pandas as pd
from paux import exception
from typing import Union

# 日期时间
date_patterns = [
    ['YYYY-MM-DD HH:mm:ss', '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'],
    ['YYYY-MM-DD HH:mm', '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$'],
    ['YYYY-MM-DD HH', '^\d{4}-\d{2}-\d{2} \d{2}$'],
    ['YYYY-MM-DD', '^\d{4}-\d{2}-\d{2}$'],

    ['DD/MM/YYYY HH:mm:ss', '^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$'],
    ['DD/MM/YYYY HH:mm', '^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$'],
    ['DD/MM/YYYY HH', '^\d{2}/\d{2}/\d{4} \d{2}$'],
    ['DD/MM/YYYY', '^\d{2}/\d{2}/\d{4}$'],
]
# 时间
time_patterns = [
    ['HH:mm:ss', '^\d{2}:\d{2}:\d{2}$'],
]

def __to_datetime_by_pattern(date: str, fmt_patterns: list, timezone: str = None):
    for fmt, pattern in fmt_patterns:
        if re.match(pattern, date):
            return pendulum.from_format(date, fmt, tz=timezone)
    return None


# 得到毫秒时间戳
def to_ts(
        date: Union[int, float, str, datetime.date, None],
        timezone: str = None,
        default: Union[int, float] = 0
) -> int:
    '''
    :param date: 日期
    :param timezone: 时区
    :param default: 默认值


    例如：
        to_ts(date=pendulum.now(), timezone=None, default=0)
        to_ts(date=pendulum.now().date(), timezone=None, default=0)
        to_ts(date=datetime.datetime.now(), timezone=None, default=0)
        to_ts(date=datetime.datetime.now().date(), timezone=None, default=0)
        to_ts(date=datetime.datetime.now().timestamp() * 1000, timezone=None, default=0)
        to_ts(date='2022-01-02 03:04:05', timezone=None, default=0)
        to_ts(date='2022-01-02 03:04', timezone=None, default=0)
        to_ts(date='2022-01-02 03', timezone=None, default=0)
        to_ts(date='2022-01-02', timezone=None, default=0)
        to_ts(date='01/02/2022 03:04:05', timezone=None, default=0)
        to_ts(date='01/02/2022 03:04', timezone=None, default=0)
        to_ts(date='01/02/2022 03', timezone=None, default=0)
        to_ts(date='01/02/2022', timezone=None, default=0)
        to_ts(date=None, timezone=None, default=0)
        to_ts(date=np.nan, timezone=None, default=0)
    '''
    # 没有date，返回默认值
    if pd.isna(date):
        ts = default
    # 数字对象
    elif isinstance(date, int) or isinstance(date, float):
        ts = int(date)
    # 日期时间
    elif isinstance(date, datetime.datetime):
        ts = int(date.timestamp() * 1000)
    # 日期
    elif isinstance(date, datetime.date):
        ts = int(pendulum.datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            tz=timezone,
        ).timestamp() * 1000)
    # 字符串
    elif isinstance(date, str):
        ret_date = __to_datetime_by_pattern(date, date_patterns, timezone)
        # 转换成功
        if ret_date:
            ts = int(ret_date.timestamp() * 1000)
        # 转化失败
        else:
            error_msg = '参数date无法转换：{date}\n支持的时间格式有：{date_pattern}'.format(
                date=date,
                date_pattern='\n\t'.join(
                    [fmt for fmt, pattern in date_patterns]
                )
            )
            raise exception.ParamException(error_msg)
    # 未知数据类型
    else:
        error_msg = '参数date类型错误，支持的类型有：int float datetime.date datetime.datetime str'
        raise exception.ParamException(error_msg)
    return ts


# 得到时期对象
def to_datetime(
        date: Union[int, float, str, datetime.date],
        timezone: str = None,
):
    '''
    :param date: 日期
    :param timezone: 时区
    :return: 日期对象
    例子:
        to_datetime(date=pendulum.now(), timezone='America/New_York')
        to_datetime(date=pendulum.now().date(), timezone='America/New_York')
        to_datetime(date=datetime.datetime.now(), timezone='America/New_York')
        to_datetime(date=datetime.datetime.now().date(), timezone='America/New_York')
        to_datetime(date=datetime.datetime.now().timestamp() * 1000, timezone='America/New_York')
        to_datetime(date='2022-01-02 03:04:05', timezone='America/New_York')
        to_datetime(date='2022-01-02 03:04', timezone='America/New_York')
        to_datetime(date='2022-01-02 03', timezone='America/New_York')
        to_datetime(date='2022-01-02', timezone='America/New_York')
        to_datetime(date='01/02/2022 03:04:05', timezone='America/New_York')
        to_datetime(date='01/02/2022 03:04', timezone='America/New_York')
        to_datetime(date='01/02/2022 03', timezone='America/New_York')
        to_datetime(date='01/02/2022', timezone='America/New_York')
    '''
    # 数字对象
    if isinstance(date, int) or isinstance(date, float):
        ret_date = pendulum.from_timestamp(int(date) / 1000, tz=timezone)
    # 字符串对象
    elif isinstance(date, str):
        ret_date = __to_datetime_by_pattern(date, date_patterns, timezone)
        if not ret_date:
            error_msg = '参数date无法转换：{date}\n支持的时间格式有：{date_pattern}'.format(
                date=date,
                date_pattern='\n\t'.join(
                    [fmt for fmt, pattern in date_patterns]
                )
            )
            raise exception.ParamException(error_msg)
    # 日期时间
    elif isinstance(date, datetime.datetime):
        ret_date = pendulum.from_timestamp(
            date.timestamp(),
            tz=timezone
        )
        pass
    # 日期
    elif isinstance(date, datetime.date):
        ret_date = pendulum.datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=0,
            minute=0,
            second=0,
            tz=timezone
        )
    # 未知类型
    else:
        error_msg = '参数date类型错误，支持的类型有：int float str datetime.date'
        raise exception.ParamException(error_msg)
    return ret_date


# 转换为时间对象
def to_time(
        date: Union[int, float, str, datetime.date, datetime.time],
        timezone: str = None
):
    '''
    :param date: 日期或时间
    :param timezone: 时区
    :return: 时间对象
    例子:
        to_time(date=pendulum.now(), timezone=None)
        to_time(date=pendulum.now().date(), timezone=None)
        to_time(date=pendulum.now().time(), timezone=None)
        to_time(date=datetime.datetime.now(), timezone=None)
        to_time(date=datetime.datetime.now().date(), timezone=None)
        to_time(date=datetime.datetime.now().time(), timezone=None)
        to_time(date=datetime.datetime.now().timestamp() * 1000, timezone=None)
        to_time(date='2022-01-02 03:04:05', timezone=None)
        to_time(date='2022-01-02 03:04', timezone=None)
        to_time(date='2022-01-02 03', timezone=None)
        to_time(date='2022-01-02', timezone=None)
        to_time(date='01/02/2022 03:04:05', timezone=None)
        to_time(date='01/02/2022 03:04', timezone=None)
        to_time(date='01/02/2022 03', timezone=None)
        to_time(date='01/02/2022', timezone=None)
        to_time(date='01:02:03', timezone=None)
    '''
    if isinstance(date, datetime.time):
        time = pendulum.time(
            hour=date.hour,
            minute=date.minute,
            second=date.second
        )
    elif isinstance(date, str) and re.match(time_patterns[0][1], date):
        time = pendulum.from_format(
            date, time_patterns[0][0], tz=timezone
        )
    elif isinstance(date, int) or isinstance(date, float) or isinstance(date, str) or isinstance(date, datetime.date):
        time = to_datetime(date, timezone).time()
    else:
        error_msg = '参数date类型错误，支持的类型有：int float str datetime.date datetime.time'
        raise exception.ParamException(error_msg)
    return time


# 得到日期序列
def get_range_dates(
        start: Union[int, float, str, datetime.date],
        end: Union[int, float, str, datetime.date],
        timezone: str = None,
):
    start_datetime = to_datetime(date=start, timezone=timezone)
    end_datetime = to_datetime(date=end, timezone=timezone)

    start_date = start_datetime.date()
    end_date = end_datetime.date()

    dates: list = [
        (start_date + datetime.timedelta(days=day)).strftime('%Y-%m-%d')
        for day in range((end_date - start_date).days + 1)
    ]
    return dates


# 格式化输出时间
def to_fmt(
        date: Union[int, float, str, datetime.date],
        timezone: str = None,
        fmt='%Y-%m-%d %H:%M:%S'
) -> str:
    return to_datetime(date, timezone).strftime(fmt)


# 是否在时间段中
def is_period_allowed(
        date: Union[int, float, str, datetime.date,datetime.time],
        periods: list,
        timezone: str = None
):
    '''
    :param date: 日期
    :param periods: 允许的时间段
    :param timezone: 时区
    :return: True|False

    '''
    if not periods:
        return False
    time = to_time(date, timezone).strftime('%H:%M:%S')
    for period in periods:
        if time >= period[0] and time <= period[1]:
            return True
    return False


if __name__ == '__main__':
    print(isinstance(datetime.datetime.now().time(), datetime.time))
    # print(pendulum.from_format('01:02:03', fmt='HH:mm:ss'))
    # 测试to_ts
    # print(to_ts(date=pendulum.now(), timezone=None, default=0))
    # print(to_ts(date=pendulum.now().date(), timezone=None, default=0))
    # print(to_ts(date=datetime.datetime.now(), timezone=None, default=0))
    # print(to_ts(date=datetime.datetime.now().date(), timezone=None, default=0))
    # print(to_ts(date=datetime.datetime.now().timestamp() * 1000, timezone=None, default=0))
    # print(to_ts(date='2022-01-02 03:04:05', timezone=None, default=0))
    # print(to_ts(date='2022-01-02 03:04', timezone=None, default=0))
    # print(to_ts(date='2022-01-02 03', timezone=None, default=0))
    # print(to_ts(date='2022-01-02', timezone=None, default=0))
    # print(to_ts(date='01/02/2022 03:04:05', timezone=None, default=0))
    # print(to_ts(date='01/02/2022 03:04', timezone=None, default=0))
    # print(to_ts(date='01/02/2022 03', timezone=None, default=0))
    # print(to_ts(date='01/02/2022', timezone=None, default=0))
    # print(to_ts(date=None, timezone=None, default=0))
    # print(to_ts(date=np.nan, timezone=None, default=0))

    # 测试to_datetime
    # print(to_datetime(date=pendulum.now(), timezone='America/New_York'))
    # print(to_datetime(date=pendulum.now().date(), timezone='America/New_York'))
    # print(to_datetime(date=datetime.datetime.now(), timezone='America/New_York'))
    # print(to_datetime(date=datetime.datetime.now().date(), timezone='America/New_York'))
    # print(to_datetime(date=datetime.datetime.now().timestamp() * 1000, timezone='America/New_York'))
    # print(to_datetime(date='2022-01-02 03:04:05', timezone='America/New_York'))
    # print(to_datetime(date='2022-01-02 03:04', timezone='America/New_York'))
    # print(to_datetime(date='2022-01-02 03', timezone='America/New_York'))
    # print(to_datetime(date='2022-01-02', timezone='America/New_York'))
    # print(to_datetime(date='01/02/2022 03:04:05', timezone='America/New_York'))
    # print(to_datetime(date='01/02/2022 03:04', timezone='America/New_York'))
    # print(to_datetime(date='01/02/2022 03', timezone='America/New_York'))
    # print(to_datetime(date='01/02/2022', timezone='America/New_York'))

    # 测试to_time
    # print(to_time(date=pendulum.now(), timezone=None))
    # print(to_time(date=pendulum.now().date(), timezone=None))
    # print(to_time(date=pendulum.now().time(), timezone=None))
    # print(to_time(date=datetime.datetime.now(), timezone=None))
    # print(to_time(date=datetime.datetime.now().date(), timezone=None))
    # print(to_time(date=datetime.datetime.now().time(), timezone=None))
    # print(to_time(date=datetime.datetime.now().timestamp() * 1000, timezone=None))
    # print(to_time(date='2022-01-02 03:04:05', timezone=None))
    # print(to_time(date='2022-01-02 03:04', timezone=None))
    # print(to_time(date='2022-01-02 03', timezone=None))
    # print(to_time(date='2022-01-02', timezone=None))
    # print(to_time(date='01/02/2022 03:04:05', timezone=None))
    # print(to_time(date='01/02/2022 03:04', timezone=None))
    # print(to_time(date='01/02/2022 03', timezone=None))
    # print(to_time(date='01/02/2022', timezone=None))
    # print(to_time(date='01:02:03', timezone=None))
