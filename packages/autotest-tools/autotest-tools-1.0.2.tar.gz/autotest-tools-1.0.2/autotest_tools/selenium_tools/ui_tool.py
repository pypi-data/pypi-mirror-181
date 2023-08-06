import base64

from autotest_tools.common_tools.log_tool import log_d
from autotest_tools.common_tools.ocr_tool import get_ocr_result
from autotest_tools.selenium_tools.driver_tool import DriverTool

TAG = "UiTool"


class UiTool(DriverTool):
    def __init__(self, driver):
        super().__init__(driver)

    def ui_get_img_text(self, loc, cut_area=None):
        """
        获取图片中的文字
        :param loc: 图片元素定位
        :param cut_area: 裁切范围
        :return: 图片中的文字
        """
        element = self.browser_locate(loc)
        image_base64 = element.screenshot_as_base64
        image_bytes = base64.b64decode(image_base64)
        res = get_ocr_result(image_bytes, cut_area)
        log_d(TAG, "Get img text, result: {}".format(res))
        return res

    def ui_get_canvas_text(self, loc, w1=0, w2=1, h1=0, h2=1):
        """
        获取canvas中的文字
        :param loc: canvas元素定位
        :param w1: 截取宽起始
        :param w2: 截取宽结尾
        :param h1: 截取宽起始
        :param h2: 截取高结尾
        :return: canvas中的文字
        """
        element = self.browser_locate(loc)
        width = eval(element.get_attribute("width"))
        height = eval(element.get_attribute("height"))
        cut_area = (w1 * width, h1 * height, w2 * width, h2 * height)
        img_bytes = self.get_canvas_bytes(loc)
        res = get_ocr_result(img_bytes, cut_area)
        log_d(TAG, "Get canvas text, result: {}".format(res))
        return res

    def get_canvas_bytes(self, loc):
        """
        下载canvas图片
        :param loc: canvas元素定位
        :return: 图片路径
        """
        element = self.browser_locate(loc)
        js = "var canvas = arguments[0];" \
             "var context = canvas.getContext('2d');" \
             "context.globalCompositeOperation='destination-over';" \
             "context.fillStyle='white';" \
             "context.fillRect(0,0,canvas.width,canvas.height);" \
             "context.globalCompositeOperation='source-over';" \
             "return canvas.toDataURL('image/png');"
        image_data = self.execute_js(js, element)
        image_base64 = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_base64)
        return image_bytes
