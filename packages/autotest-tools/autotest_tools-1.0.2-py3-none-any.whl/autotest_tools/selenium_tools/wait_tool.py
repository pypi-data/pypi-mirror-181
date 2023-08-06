import time

from autotest_tools.common_tools.log_tool import log_d
from autotest_tools.selenium_tools.driver_tool import DriverTool

TAG = "WaitTool"


class WaitTool(DriverTool):
    def __init__(self, driver):
        super().__init__(driver)

    def wait(self, seconds):
        """
        等待
        :param seconds: 秒数
        :return: None
        """
        log_d(TAG, "Wait for {} seconds".format(seconds))
        time.sleep(seconds)
