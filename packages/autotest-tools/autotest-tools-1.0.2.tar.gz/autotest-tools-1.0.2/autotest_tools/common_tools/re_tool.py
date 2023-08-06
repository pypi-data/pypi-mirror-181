import re


def re_time(text):
    """
    正则表达式匹配时间
    :param text: 需要匹配的文本
    :return: 返回匹配到的时间
    """
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
    result = pattern.findall(text)
    return result
