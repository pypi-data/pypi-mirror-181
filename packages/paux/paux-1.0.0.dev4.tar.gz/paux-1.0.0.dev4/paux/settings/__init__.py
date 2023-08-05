'''
get_setting_filepath    获取配置文件的路径
read_settings           读取配置文件
save_settings           保存配置文件
'''

import os
from paux import exception
from paux import system as _system
import json


# 初始化settings文件中的内容

def init_settings(settings_path=None):
    CANDLE_DIRNAME = 'CANDLE_DATA'
    platform = _system.get_platform()
    if platform == 'WINDOWS':
        CANDLE_BASE_DIR = os.path.join(os.getenv("SystemDrive"), CANDLE_DIRNAME)
    elif platform == 'MACOS':
        CANDLE_BASE_DIR = os.path.join(_system.get_maxOs_documents_path(), CANDLE_DIRNAME)
    elif platform == 'LINUX':
        CANDLE_BASE_DIR = os.path.join('/root/', CANDLE_DIRNAME)
    else:
        error_msg = f'未知系统 {platform}'
        raise exception.PlatformError(error_msg)

    init_data = {
        'CANDLE_OKX_BASE_DIR': os.path.join(CANDLE_BASE_DIR, 'OKX'),
        'CANDLE_OKX_TIMEZONE': 'Asia/Shanghai',
        'CANDLE_BINANCE_BASE_DIR': os.path.join(CANDLE_BASE_DIR, 'BINANCE'),
        'CANDLE_BINANCE_TIMEZONE': 'America/New_York',
        'CANDLE_HUOBI_BASE_DIR': os.path.join(CANDLE_BASE_DIR, 'HUOBI'),
        'CANDLE_HUOBI_TIMEZONE': 'Asia/Shanghai',
        'CANDLE_TDA_BASE_DIR': os.path.join(CANDLE_BASE_DIR, 'TDA'),
        'CANDLE_TDA_TIMEZONE': 'America/New_York',
        'CANDLE_IB_BASE_DIR': os.path.join(CANDLE_BASE_DIR, 'IB'),
        'CANDLE_IB_TIMEZONE': 'America/New_York',
        'CANDLE_EAST_MONEY_BAST_DIR': os.path.join(CANDLE_BASE_DIR, 'MONEY_EAST'),
        'CANDLE_EAST_MONEY_TIMEZONE': 'Asia/Shanghai',
    }
    # for key, value in init_data.items():
    #     msg = f'{key} = {value} (Y|N)\n'
    #     command = input(msg)
    #     if command.lower() == 'y':
    #         pass
    #     elif command.lower() == 'n':
    #         msg = f'{key} : \n'
    #         value = input(msg)
    #         init_data[key] = value
    save_settings(data=init_data, settings_path=settings_path)


# 获取配置文件路径
def get_settings_filepath(
        dirpath: str = None, filename: str = 'SETTINGS.JSON'
):
    '''
    :param dirpath: 配置文件的文件夹地址，如果没有本项目会使用paux的路径作为dirpath
    :param filename: 配置文件的名字
    :return: 配置文件路径
    '''
    if not dirpath:
        dirpath = os.path.dirname(os.path.dirname(__file__))
    elif not os.path.isdir(dirpath):
        raise exception.ParamException('dirpath应该是文件夹而非文件')
    settings_path = os.path.join(dirpath, filename)
    return settings_path


# 读取配置文件
def read_settings(settings_path: str = None):
    '''
    :param settings_path: 配置文件路径，不填写用默认
    :return: 配置文件字典

        如果没有配置文件，会返回空字典
    '''
    if not settings_path:
        settings_path = get_settings_filepath()
    if not os.path.isfile(settings_path):
        init_settings(settings_path)
    return json.load(open(settings_path, 'rb'))


# 保存配置文件
def save_settings(data: dict, settings_path: str = None):
    '''
    :param data: 配置数据
    :param settings_path: 配置文件路径，不填写用默认
    '''
    if not settings_path:
        settings_path = get_settings_filepath()
    return json.dump(data, open(settings_path, 'w'))


if __name__ == '__main__':
    init_settings()
# if __name__ == '__main__':
#     # print(os.getenv("SystemDrive"))
#     # init_settings()
#     import os
#     # command = f'vi {path}'
#     # os.popen(command)
#     os.system("open -a Terminal .")
#     path = get_settings_filepath()
#     command = f'open {path}'
#     os.system(command)
