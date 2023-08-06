import time


def get_time_stamp():
    """
    获取当前时间戳
    :return: 当前时间戳
    """
    time_stamp = time.time()
    return time_stamp


def get_localtime():
    """
    获取当前时间
    :return: 当前时间
    """
    time_stamp = get_time_stamp()
    localtime = time.localtime(time_stamp)
    return localtime


def get_format_time(time_format: str):
    """
    获取当前时间并以指定格式返回
    :param time_format: 时间格式
    :return: 当前时间
    """
    localtime = get_localtime()
    format_time = time.strftime(time_format, localtime)
    return format_time
