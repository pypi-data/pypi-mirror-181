from io import BytesIO

import ddddocr
from PIL import Image


def get_ocr_result(img_bytes, cut_area=None):
    """
    识别图片中的文字
    :param img_bytes: 图片字节流
    :param cut_area: 裁切范围
    :return: 识别结果
    """
    img = Image.open(BytesIO(img_bytes))
    region = img.crop(cut_area) if cut_area else img
    ocr = ddddocr.DdddOcr(show_ad=False)
    res = ocr.classification(region)
    return res
