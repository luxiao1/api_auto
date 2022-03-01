import logging
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler

def get_logger(name,filename,encoding='utf-8',fmt=None,when='d',interval=1,backup_count=7,debug=False):
    """
    返回一个日志器
    :param name: 日志器名称
    :param filename: 日志文件名
    :param encoding: 日志文件编码格式
    :param fmt: 日志格式
    :param when: 日志轮转时间单位
    :param interval: 时间间隔
    :param backup_count: 轮转文件个数
    :param debug: 调试模式
    :return: 
    """
    # 创建日志器
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # 参数处理
    if debug:
        # 调试模式
        file_level = logging.DEBUG
        console_level = logging.DEBUG
    else:
        # 非调试模式
        file_level = logging.WARNING
        console_level = logging.INFO

    if fmt is None:
        fmt = "%(asctime)s- [%(filename)s-->%(lineno)s]- %(levelname)s: %(message)s"

    # 创建日志处理器
    file_handler = TimedRotatingFileHandler(filename=filename,when=when,interval=interval,backupCount=backup_count,encoding=encoding)
    file_handler.setLevel(file_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    # 创建格式化器
    formatter = logging.Formatter(fmt=fmt)
    # 添加格式化器
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    # 添加日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == '__main__':
    import setting
    print(setting.LOG_CONFIG)