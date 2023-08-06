import logging

import colorlog

TAG = "LogTest"

logger = logging.getLogger(TAG)
logger.setLevel(logging.DEBUG)
console_formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s %(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


def log_d(tag, msg):
    """
    打印debug级别日志
    :param tag: 标签
    :param msg: 日志内容
    :return: None
    """
    logger.debug("[{}] {}".format(tag, msg))


def log_i(tag, msg):
    """
    打印info级别日志
    :param tag: 标签
    :param msg: 日志内容
    :return: None
    """
    logger.info("[{}] {}".format(tag, msg))


def log_w(tag, msg):
    """
    打印warning级别日志
    :param tag: 标签
    :param msg: 日志内容
    :return: None
    """
    logger.warning("[{}] {}".format(tag, msg))


def log_e(tag, msg):
    """
    打印error级别日志
    :param tag: 标签
    :param msg: 日志内容
    :return: None
    """
    logger.error("[{}] {}".format(tag, msg))


def log_c(tag, msg):
    """
    打印critical级别日志
    :param tag: 标签
    :param msg: 日志内容
    :return: None
    """
    logger.critical("[{}] {}".format(tag, msg))
