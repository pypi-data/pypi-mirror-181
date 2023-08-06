import selenium.webdriver.support.expected_conditions as ec

from autotest_tools.common_tools.log_tool import log_d
from autotest_tools.selenium_tools.driver_tool import DriverTool

TAG = "EcTool"


class EcTool(DriverTool):
    def __init__(self, driver):
        super().__init__(driver)

    def verify_title_is(self, title):
        """
        验证标题为
        :param title: 标题
        :return: True or False
        """
        var = ec.title_is(title)(self.driver)
        log_d(TAG, "Verify title is: {}, result: {}".format(title, var))
        return var

    def verify_title_contains(self, title):
        """
        验证标题包含
        :param title: 标题
        :return: True or False
        """
        var = ec.title_contains(title)(self.driver)
        log_d(TAG, "Verify title contains: {}, result: {}".format(title, var))
        return var

    def verify_presence_of_element_located(self, loc):
        """
        验证元素存在
        :param loc: 元素定位
        :return: True or False
        """
        var = ec.presence_of_element_located(loc)(self.driver)
        log_d(TAG, "Verify element located: {}, result: {}".format(loc, var))
        return var

    def verify_url_contains(self, url):
        """
        验证url包含
        :param url: url
        :return: True or False
        """
        var = ec.url_contains(url)(self.driver)
        log_d(TAG, "Verify url contains: {}, result: {}".format(url, var))
        return var

    def verify_url_matches(self, pattern):
        """
        验证url匹配
        :param pattern: 匹配字段
        :return: True or False
        """
        var = ec.url_matches(pattern)(self.driver)
        log_d(TAG, "Verify url matches: {}, result: {}".format(pattern, var))
        return var

    def verify_url_to_be(self, url):
        """
        验证url等于
        :param url: url
        :return: True or False
        """
        var = ec.url_to_be(url)(self.driver)
        log_d(TAG, "Verify url to be: {}, result: {}".format(url, var))
        return var

    def verify_url_changes(self, url):
        """
        验证url变化
        :param url: url
        :return: True or False
        """
        var = ec.url_changes(url)(self.driver)
        log_d(TAG, "Verify url changes: {}, result: {}".format(url, var))
        return var

    def verify_visibility_of(self, loc):
        """
        验证元素可见
        :param loc: 元素定位
        :return: True or False
        """
        element = self.browser_locate(loc)
        var = ec.visibility_of(element)(self.driver)
        log_d(TAG, "Verify element visibility: {}, result: {}".format(loc, var))
        return var

    def verify_presence_of_all_elements_located(self, loc):
        """
        验证所有元素存在
        :param loc: 元素定位
        :return: True or False
        """
        var = ec.presence_of_all_elements_located(loc)(self.driver)
        log_d(TAG, "Verify all elements located: {}, result: {}".format(loc, var))
        return var

    def verify_visibility_of_any_elements_located(self, loc):
        """
        验证任意元素可见
        :param loc: 元素定位
        :return: True or False
        """
        var = ec.visibility_of_any_elements_located(loc)(self.driver)
        log_d(TAG, "Verify any element visibility: {}, result: {}".format(loc, var))
        return var

    def verify_visibility_of_all_elements_located(self, loc):
        """
        验证所有元素可见
        :param loc: 元素定位
        :return: True or False
        """
        var = ec.visibility_of_all_elements_located(loc)(self.driver)
        log_d(TAG, "Verify all elements visibility: {}, result: {}".format(loc, var))
        return var

    def verify_text_to_be_present_in_element(self, loc, text):
        """
        验证元素文本包含
        :param loc: 元素定位
        :param text: 文本
        :return: True or False
        """
        var = ec.text_to_be_present_in_element(loc, text)(self.driver)
        log_d(TAG, "Verify text to be present in element: {}, result: {}".format(loc, var))
        return var

    def verify_text_to_be_present_in_element_value(self, loc, text):
        """
        验证元素value包含
        :param loc: 元素定位
        :param text: 文本
        :return: True or False
        """
        var = ec.text_to_be_present_in_element_value(loc, text)(self.driver)
        log_d(TAG, "Verify text to be present in element value: {}, result: {}".format(loc, var))
        return var

    def verify_text_to_be_present_in_element_attribute(self, loc, attribute, text):
        """
        验证元素属性包含
        :param loc: 元素定位
        :param attribute: 属性
        :param text: 文本
        :return: True or False
        """
        var = ec.text_to_be_present_in_element_attribute(loc, attribute, text)(self.driver)
        log_d(TAG, "Verify text to be present in element attribute: {}, result: {}".format(loc, var))
        return var

    def verify_frame_to_be_available_and_switch_to_it(self, loc):
        """
        验证frame可用并切换
        :param loc: 元素定位
        :return: True or False
        """
        var = ec.frame_to_be_available_and_switch_to_it(loc)(self.driver)
        log_d(TAG, "Verify frame to be available and switch to it: {}, result: {}".format(loc, var))
        return var

    def verify_invisibility_of(self, loc):
        """
        验证元素不可见
        :param loc: 元素定位
        :return: True or False
        """
        element = self.browser_locate(loc)
        var = ec.invisibility_of_element(element)(self.driver)
        log_d(TAG, "Verify element invisibility: {}, result: {}".format(loc, var))
        return var

    def verify_element_to_be_clickable(self, loc):
        """
        验证元素可点击
        :param loc: 元素定位
        :return: True or False
        """
        element = self.browser_locate(loc)
        var = ec.element_to_be_clickable(element)(self.driver)
        log_d(TAG, "Verify element to be clickable: {}, result: {}".format(loc, var))
        return var

    def verify_staleness_of(self, loc):
        """
        验证元素不可用
        :param loc: 元素定位
        :return: True or False
        """
        element = self.browser_locate(loc)
        var = ec.staleness_of(element)(self.driver)
        log_d(TAG, "Verify element staleness: {}, result: {}".format(loc, var))
        return var

    def verify_element_to_be_selected(self, loc):
        """
        验证元素被选中
        :param loc: 元素定位
        :return: True or False
        """
        element = self.browser_locate(loc)
        var = ec.element_to_be_selected(element)(self.driver)
        log_d(TAG, "Verify element to be selected: {}, result: {}".format(loc, var))
        return var

    def verify_element_selection_state_to_be(self, loc, state):
        """
        验证元素选中状态
        :param loc: 元素定位
        :param state: 选中状态
        :return: True or False
        """
        element = self.browser_locate(loc)
        var = ec.element_selection_state_to_be(element, state)(self.driver)
        log_d(TAG, "Verify element selection state to be: {}, result: {}".format(loc, var))
        return var

    def verify_number_of_windows_to_be(self, num):
        """
        验证窗口数量
        :param num: 窗口数量
        :return: True or False
        """
        var = ec.number_of_windows_to_be(num)(self.driver)
        log_d(TAG, "Verify number of windows to be: {}, result: {}".format(num, var))
        return var

    def verify_new_window_is_opened(self, handles):
        """
        验证新窗口打开
        :param handles: 窗口句柄
        :return: True or False
        """
        var = ec.new_window_is_opened(handles)(self.driver)
        log_d(TAG, "Verify new window is opened: {}, result: {}".format(handles, var))
        return var

    def verify_alert_is_present(self):
        """
        验证alert弹窗存在
        :return: True or False
        """
        var = ec.alert_is_present()(self.driver)
        log_d(TAG, "Verify alert is present: {}".format(var))
        return var

    def verify_element_attribute_to_include(self, loc, attribute):
        """
        验证元素属性包含
        :param loc: 元素定位
        :param attribute: 属性
        :return: True or False
        """
        element = self.browser_locate(loc)
        var = ec.element_attribute_to_include(element, attribute)(self.driver)
        log_d(TAG, "Verify element attribute to include: {}, result: {}".format(loc, var))
        return var
