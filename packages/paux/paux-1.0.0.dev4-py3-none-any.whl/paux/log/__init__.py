import logging
import os
import datetime
import traceback


class Log():
    LOG_DIRPATH = './LOG_DATA'
    FILE_LEVEL = 'DEBUG'
    CONSOLE_LEVEL = 'DEBUG'

    def __init__(self):
        if not os.path.isdir(self.LOG_DIRPATH):
            os.makedirs(self.LOG_DIRPATH)

    def get_logger(self, level):
        log_filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        log_filepath = os.path.join(self.LOG_DIRPATH, log_filename)
        file_handler = logging.FileHandler(log_filepath)  # 输出到文件
        console_handler = logging.StreamHandler()  # 输出到控制台
        file_handler.setLevel(self.FILE_LEVEL)  # FILE_LEVEL以上才输出到文件
        console_handler.setLevel(self.CONSOLE_LEVEL)  # CONSOLE_LEVEL以上才输出到控制台
        fmt = '''-----------------------------------------------
        datetime:   %(asctime)s
        level:      %(levelname)s
        filePath:   {filepath}
        funcName:   %(funcName)s
        line:       %(lineno)d
        messge:     {message}
        traceback:  {traceback}
        '''.format(filepath=__file__, message='%(message)s', traceback=str(traceback.format_exc()))
        formatter = logging.Formatter(fmt)
        file_handler.setFormatter(formatter)  # 设置文件内容格式
        console_handler.setFormatter(formatter)  # 设置控制台内容格式
        logger = logging.getLogger('updateSecurity')
        logger.setLevel(level)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger

    def log_info(self, msg):
        LEVEL = 'INFO'
        self.get_logger(level=LEVEL).info(msg)

    def log_debug(self, msg):
        LEVEL = 'DEBUG'
        self.get_logger(level=LEVEL).info(msg)

    def log_error(self, msg):
        LEVEL = 'ERROR'
        self.get_logger(level=LEVEL).info(msg)

    def log_warn(self, msg):
        LEVEL = 'warn'
        self.get_logger(level=LEVEL).info(msg)

# if __name__ == '__main__':
#     l = Log()
#     l.log_info(msg='123')
