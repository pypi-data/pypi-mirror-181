from autotest_tools.common_tools.log_tool import log_d
from autotest_tools.selenium_tools.driver_tool import DriverTool

TAG = "ElementTool"


class ElementTool(DriverTool):

    def __init__(self, driver):
        super().__init__(driver)

    def get_tag_name(self, loc):
        """
        获取元素的标签名
        :param loc: 元素定位
        :return: 标签名
        """
        element = self.browser_locate(loc)
        var = element.tag_name
        log_d(TAG, "Get element {} tag name: {}".format(loc, var))
        return var

    def get_text(self, loc):
        """
        获取元素的文本
        :param loc: 元素定位
        :return: 元素文本
        """
        element = self.browser_locate(loc)
        var = element.text
        log_d(TAG, "Get element {} text: {}".format(loc, var))
        return var

    def click(self, loc):
        """
        点击元素
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Click element: {}".format(loc))
        element = self.browser_locate(loc)
        element.click()
        return None

    def submit(self, loc):
        """
        提交表单
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Submit form")
        element = self.browser_locate(loc)
        element.submit()
        return None

    def clear(self, loc):
        """
        清除元素内容
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Clear element")
        element = self.browser_locate(loc)
        element.clear()
        return None

    def get_property(self, loc, name):
        """
        获取元素的属性值
        :param loc: 元素定位
        :param name: 属性名
        :return: 属性值
        """
        element = self.browser_locate(loc)
        var = element.get_property(name)
        log_d(TAG, "Get {} property: {}".format(name, var))
        return var

    def get_dom_attribute(self, loc, name):
        """
        获取元素的dom属性值
        :param loc: 元素定位
        :param name: dom属性名
        :return: dom属性值
        """
        element = self.browser_locate(loc)
        var = element.get_dom_attribute(name)
        log_d(TAG, "Get {} dom attribute: {}".format(name, var))
        return var

    def get_attribute(self, loc, name):
        """
        获取元素的属性值
        :param loc: 元素定位
        :param name: 属性名
        :return: 属性值
        """
        element = self.browser_locate(loc)
        var = element.get_attribute(name)
        log_d(TAG, "Get {} attribute: {}".format(name, var))
        return var

    def check_is_selected(self, loc):
        """
        检查元素是否被选中
        :param loc: 元素定位
        :return: True or False
        """
        element = self.browser_locate(loc)
        var = element.is_selected()
        log_d(TAG, "Is element {} selected: {}".format(loc, var))
        return var

    def check_is_enabled(self, loc):
        """
        检查元素是否可用
        :param loc: 元素定位
        :return: True or False
        """
        element = self.browser_locate(loc)
        var = element.is_enabled()
        log_d(TAG, "Is element {} enabled: {}".format(loc, var))
        return var

    def send_keys(self, loc, var):
        """
        向元素输入内容
        :param loc: 元素定位
        :param var: 输入内容
        :return: None
        """
        element = self.browser_locate(loc)
        element.send_keys(var)
        log_d(TAG, "Input {} to element {}".format(var, loc))
        return None

    def check_is_displayed(self, loc):
        """
        检查元素是否可见
        :param loc: 元素定位
        :return: True or False
        """
        element = self.browser_locate(loc)
        var = element.is_displayed()
        log_d(TAG, "Is element {} displayed: {}".format(loc, var))
        return var

    def scrolled_into_view(self, loc):
        """
        滚动到元素可见
        :param loc: 元素定位
        :return: None
        """
        element = self.browser_locate(loc)
        var = element.location_once_scrolled_into_view
        log_d(TAG, "Scroll element {} into view: {}".format(loc, var))
        return var

    def get_size(self, loc):
        """
        获取元素的大小
        :param loc: 元素定位
        :return: 元素大小
        """
        element = self.browser_locate(loc)
        var = element.size
        log_d(TAG, "Get element {} size: {}".format(loc, var))
        return var

    def get_css_value(self, loc, name):
        """
        获取元素的css属性值
        :param loc: 元素定位
        :param name: css属性名
        :return: css属性值
        """
        element = self.browser_locate(loc)
        var = element.value_of_css_property(name)
        log_d(TAG, "Get {} css value: {}".format(name, var))
        return var

    def get_location(self, loc):
        """
        获取元素的位置
        :param loc: 元素定位
        :return: 元素位置
        """
        element = self.browser_locate(loc)
        var = element.location
        log_d(TAG, "Get element {} location: {}".format(loc, var))
        return var

    def get_rect(self, loc):
        """
        获取元素的位置和大小
        :param loc: 元素定位
        :return: 元素的位置和大小
        """
        element = self.browser_locate(loc)
        var = element.rect
        log_d(TAG, "Get element {} rect: {}".format(loc, var))
        return var

    def screenshot_as_base64(self, loc):
        """
        获取元素的截图base64编码
        :param loc: 元素定位
        :return: 元素截图
        """
        element = self.browser_locate(loc)
        var = element.screenshot_as_base64
        log_d(TAG, "Get element {} screenshot: {}".format(loc, var))
        return var

    def screenshot_as_png(self, loc):
        """
        获取元素的截图二进制数据
        :param loc: 元素定位
        :return: 元素截图
        """
        element = self.browser_locate(loc)
        var = element.screenshot_as_png
        log_d(TAG, "Get element {} screenshot: {}".format(loc, var))
        return var

    def screenshot(self, loc, filename):
        """
        截图
        :param loc: 元素定位
        :param filename: 截图文件名
        :return: None
        """
        element = self.browser_locate(loc)
        element.screenshot(filename)
        log_d(TAG, "Screenshot element {} to {}".format(loc, filename))
        return None

    def get_parent(self, loc):
        """
        获取元素的父元素
        :param loc: 元素定位
        :return: 父元素
        """
        element = self.browser_locate(loc)
        var = element.parent
        log_d(TAG, "Get element {} parent: {}".format(loc, var))
        return var

    def get_id(self, loc):
        """
        获取元素的id
        :param loc: 元素定位
        :return: 元素id
        """
        element = self.browser_locate(loc)
        var = element.id
        log_d(TAG, "Get element {} id: {}".format(loc, var))
        return var

    def element_locate(self, loc, child_loc):
        """
        定位元素的子元素
        :param loc: 元素定位
        :param child_loc: 子元素定位
        :return: 子元素
        """
        element = self.browser_locate(loc)
        child_elements = element.find_elements(*child_loc)
        if 1 == len(child_elements):
            log_d(TAG, "Locate element {}'s child element {}".format(loc, child_elements[0]))
            return child_elements[0]
        log_d(TAG, "Locate element {}'s child element {}".format(loc, child_elements))
        return child_elements
