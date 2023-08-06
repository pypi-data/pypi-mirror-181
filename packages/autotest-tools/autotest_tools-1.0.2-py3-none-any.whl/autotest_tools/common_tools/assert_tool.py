from autotest_tools.common_tools.log_tool import log_d, log_e

TAG = "Assertion"


def assert_equals(var1, var2, msg=None):
    """
    断言相等
    :param var1: var1
    :param var2: var2
    :param msg: 描述信息
    :return: None
    """
    log_d(TAG, "AssertEquals: var1 = {}, var2 = {}".format(var1, var2))
    res = var1 == var2
    log_e(TAG, "AssertEquals Failed: var1 = {}, var2 = {}".format(var1, var2)) if not res else None
    assert res, msg


def assert_not_equals(var1, var2, msg=None):
    """
    断言不相等
    :param var1: var1
    :param var2: var2
    :param msg: 描述信息
    :return: None
    """
    log_d(TAG, "AssertNotEquals: var1 = {}, var2 = {}".format(var1, var2))
    res = var1 != var2
    log_e(TAG, "AssertNotEquals Failed: var1 = {}, var2 = {}".format(var1, var2)) if not res else None
    assert res, msg


def assert_true(var, msg=None):
    """
    断言条件为真
    :param var: var
    :param msg: 描述信息
    :return: None
    """
    log_d(TAG, "AssertTrue: var = {}".format(var))
    res = bool(var)
    log_e(TAG, "AssertTrue Failed: var = {}".format(var)) if not res else None
    assert res, msg


def assert_false(var, msg=None):
    """
    断言条件为假
    :param var: var
    :param msg: 描述信息
    :return: None
    """
    log_d(TAG, "AssertFalse: var = {}".format(var))
    res = not bool(var)
    log_e(TAG, "AssertFalse Failed: var = {}".format(var)) if not res else None
    assert res, msg


def assert_none(var, msg=None):
    """
    断言为None
    :param var: var
    :param msg: 描述信息
    :return: None
    """
    log_d(TAG, "AssertNone: var = {}".format(var))
    res = var is None
    log_e(TAG, "AssertNone Failed: var = {}".format(var)) if not res else None
    assert res, msg


def assert_not_none(var, msg=None):
    """
    断言不为None
    :param var: var
    :param msg: 描述信息
    :return: None
    """
    log_d(TAG, "AssertNotNone: var = {}".format(var))
    res = var is not None
    log_e(TAG, "AssertNotNone Failed: var = {}".format(var)) if not res else None
    assert res, msg


def assert_contains(var1, var2, msg=None):
    """
    断言存在
    :param var1: var1
    :param var2: var2
    :param msg: 描述信息
    :return: None
    """
    log_d(TAG, "AssertContains: var1 = {}, var2 = {}".format(var1, var2))
    res = var2 in var1
    log_e(TAG, "AssertContains Failed: var1 = {}, var2 = {}".format(var1, var2)) if not res else None
    assert res, msg


def assert_not_contains(var1, var2, msg=None):
    """
    断言不存在
    :param var1: var1
    :param var2: var2
    :param msg: 描述信息
    :return: None
    """
    log_d(TAG, "AssertNotContains: var1 = {}, var2 = {}".format(var1, var2))
    res = var2 not in var1
    log_e(TAG, "AssertNotContains Failed: var1 = {}, var2 = {}".format(var1, var2)) if not res else None
    assert res, msg
