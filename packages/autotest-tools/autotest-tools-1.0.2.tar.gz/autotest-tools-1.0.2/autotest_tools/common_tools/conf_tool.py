import configparser


def get_config(config_path):
    """
    获取config文件
    :param config_path: config文件路径
    :return: config
    """
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    config.read(config_path, encoding="utf-8")
    return config


def get_sections_list(config_path):
    """
    获取config文件中的section
    :param config_path: config文件路径
    :return: config文件section列表
    """
    config = get_config(config_path)
    sections_list = config.sections()
    return sections_list


def get_options_name(config_path, section_name):
    """
    获取config文件中对应section下的所有option
    :param config_path: config文件路径
    :param section_name: section名称
    :return: section下的所有option列表
    """
    config = get_config(config_path)
    options_list = config.options(section_name)
    return options_list


def get_option_value(config_path, section_name, option_name):
    """
    获取config文件中对应option的value值
    :param config_path: config文件路径
    :param section_name: section名称
    :param option_name: option名称
    :return: option对应的值
    """
    config = get_config(config_path)
    option_value = config.get(section_name, option_name)
    return option_value


def get_section_dict(config_path, section_name):
    """
    获取config文件中section内容
    :param config_path: config文件路径
    :param section_name: section名称
    :return: section内容
    """
    config = get_config(config_path)
    section_content = dict([(key, value) for key, value in config.items(section_name)])
    return section_content


def set_option_value(config_path, section_name, option_name, option_value):
    """
    设置config文件中对应option的value值
    :param config_path: config文件路径
    :param section_name: section名称
    :param option_name: option名称
    :param option_value: option值
    :return: None
    """
    config = get_config(config_path)
    config.set(section_name, option_name, option_value)
    with open(config_path, "a") as f:
        config.write(f)
