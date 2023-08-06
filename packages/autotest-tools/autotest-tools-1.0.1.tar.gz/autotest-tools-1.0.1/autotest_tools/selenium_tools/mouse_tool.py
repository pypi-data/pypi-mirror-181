from selenium.webdriver import ActionChains

from autotest_tools.common_tools.log_tool import log_d
from autotest_tools.selenium_tools.driver_tool import DriverTool

TAG = "MouseTool"


class MouseTool(DriverTool):
    def __init__(self, driver):
        super().__init__(driver)
        self.mouse = ActionChains(self.driver)

    def mouse_reset(self):
        """
        重置鼠标
        :return: None
        """
        log_d(TAG, "Reset mouse")
        self.mouse.reset_actions()
        return None

    def mouse_click(self, loc):
        """
        鼠标左键单击
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse click")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.click(element)
        self.mouse.perform()
        return None

    def mouse_click_and_hold(self, loc):
        """
        鼠标左键单击并按住
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse click and hold")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.click_and_hold(element)
        self.mouse.perform()
        return None

    def mouse_right_click(self, loc):
        """
        鼠标右键单击
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse right click")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.context_click(element)
        self.mouse.perform()
        return None

    def mouse_double_click(self, loc):
        """
        鼠标左键双击
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse double click")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.double_click(element)
        self.mouse.perform()
        return None

    def mouse_double_click_by_screen_offset(self, x_percent, y_percent):
        """
        鼠标双击指定位置
        :param x_percent: x轴偏移量
        :param y_percent: y轴偏移量
        :return: None
        """
        log_d(TAG, "Mouse double click by screen offset")
        self.mouse_reset()
        browser_size = self.driver.get_window_size()
        x = browser_size["width"] * x_percent
        y = browser_size["height"] * y_percent
        self.mouse_move_by_offset(x, y)
        self.mouse.double_click()
        self.mouse.perform()
        return None

    def mouse_click_by_screen_offset(self, x_percent, y_percent):
        """
        鼠标单击指定位置
        :param x_percent: x轴偏移量
        :param y_percent: y轴偏移量
        :return: None
        """
        log_d(TAG, "Mouse double click by screen offset")
        self.mouse_reset()
        browser_size = self.driver.get_window_size()
        x = browser_size["width"] * x_percent
        y = browser_size["height"] * y_percent
        self.mouse_move_by_offset(x, y)
        self.mouse.click()
        self.mouse.perform()
        return None

    def mouse_drag_and_drop(self, source_loc, target_loc):
        """
        鼠标拖拽到指定元素
        :param source_loc: 元素定位
        :param target_loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse drag and drop")
        source = self.browser_locate(source_loc)
        target = self.browser_locate(target_loc)
        self.mouse_reset()
        self.mouse.drag_and_drop(source, target)
        self.mouse.perform()
        return None

    def mouse_drag_and_drop_by_offset(self, loc, x_offset, y_offset):
        """
        鼠标拖拽到指定元素的偏移量
        :param loc: 元素定位
        :param x_offset: x轴偏移量
        :param y_offset: y轴偏移量
        :return: None
        """
        log_d(TAG, "Mouse drag and drop by offset")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.drag_and_drop_by_offset(element, x_offset, y_offset)
        self.mouse.perform()
        return None

    def mouse_move_by_offset(self, x_offset, y_offset):
        """
        鼠标移动到指定位置
        :param x_offset: x轴偏移量
        :param y_offset: y轴偏移量
        :return: None
        """
        log_d(TAG, "Mouse move by offset")
        self.mouse_reset()
        self.mouse.move_by_offset(x_offset, y_offset)
        self.mouse.perform()
        return None

    def mouse_move_to_element(self, loc):
        """
        鼠标移动到元素
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse move to element")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.move_to_element(element)
        self.mouse.perform()
        return None

    def mouse_move_to_element_with_offset(self, loc, x_offset, y_offset):
        """
        鼠标移动指定元素的偏移量
        :param loc: 元素定位
        :param x_offset: x轴偏移量
        :param y_offset: y轴偏移量
        :return: None
        """
        log_d(TAG, "Mouse move to element with offset")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.move_to_element_with_offset(element, x_offset, y_offset)
        self.mouse.perform()
        return None

    def mouse_pause(self, seconds):
        """
        鼠标暂停
        :param seconds: 秒数
        :return: None
        """
        log_d(TAG, "Mouse pause")
        self.mouse_reset()
        self.mouse.pause(seconds)
        self.mouse.perform()
        return None

    def mouse_release(self):
        """
        鼠标释放
        :return: None
        """
        log_d(TAG, "Mouse release")
        self.mouse_reset()
        self.mouse.release()
        self.mouse.perform()
        return None

    def mouse_move_to_element_center(self, loc):
        """
        鼠标移动到元素中心
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse move to element center")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.move_to_element_with_offset(element, element.size["width"] / 2, element.size["height"] / 2)
        self.mouse.perform()
        return None

    def mouse_move_to_element_top_left(self, loc):
        """
        鼠标移动到元素左上角
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse move to element top left")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.move_to_element_with_offset(element, 0, 0)
        self.mouse.perform()
        return None

    def mouse_move_to_element_top_right(self, loc):
        """
        鼠标移动到元素右上角
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse move to element top right")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.move_to_element_with_offset(element, element.size["width"], 0)
        self.mouse.perform()
        return None

    def mouse_move_to_element_bottom_left(self, loc):
        """
        鼠标移动到元素左下角
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse move to element bottom left")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.move_to_element_with_offset(element, 0, element.size["height"])
        self.mouse.perform()
        return None

    def mouse_move_to_element_bottom_right(self, loc):
        """
        鼠标移动到元素右下角
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse move to element bottom right")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.move_to_element_with_offset(element, element.size["width"], element.size["height"])
        self.mouse.perform()
        return None

    def mouse_scroll_to_element(self, loc):
        """
        鼠标滚动到元素
        :param loc: 元素定位
        :return: None
        """
        log_d(TAG, "Mouse scroll to element")
        element = self.browser_locate(loc)
        self.mouse_reset()
        self.mouse.move_to_element(element)
        self.mouse.perform()
        return None

    def mouse_scroll_by_amount(self, x_offset, y_offset):
        """
        鼠标滚动指定偏移量
        :param x_offset: x轴偏移量
        :param y_offset: y轴偏移量
        :return: None
        """
        log_d(TAG, "Mouse scroll by amount")
        self.mouse_reset()
        self.mouse.move_by_offset(x_offset, y_offset)
        self.mouse.perform()
        return None

    def mouse_scroll_from_origin(self, scroll_orig, x_offset, y_offset):
        """
        鼠标滚动指定偏移量
        :param scroll_orig: 滚动起始点
        :param x_offset: x轴偏移量
        :param y_offset: y轴偏移量
        :return: None
        """
        log_d(TAG, "Mouse scroll from origin")
        self.mouse_reset()
        self.mouse.scroll_from_origin(scroll_orig, x_offset, y_offset)
        self.mouse.perform()
        return None
