from autotest_tools.selenium_tools.alert_tool import AlertTool
from autotest_tools.selenium_tools.ec_tool import EcTool
from autotest_tools.selenium_tools.element_tool import ElementTool
from autotest_tools.selenium_tools.keyboard_tool import KeyBoardTool
from autotest_tools.selenium_tools.mouse_tool import MouseTool
from autotest_tools.selenium_tools.ui_tool import UiTool
from autotest_tools.selenium_tools.wait_tool import WaitTool


class BasePage(AlertTool, EcTool, ElementTool, KeyBoardTool, MouseTool, UiTool, WaitTool):
    ...
