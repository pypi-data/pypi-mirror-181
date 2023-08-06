import ddddocr
from PIL import Image


def get_ocr_result(img_path, cut_area=None):
    """
    识别图片中的文字
    :param img_path: 图片路径
    :param cut_area: 裁切范围
    :return: 识别结果
    """
    img = Image.open(img_path)
    region = img.crop(cut_area) if cut_area else img
    ocr = ddddocr.DdddOcr(show_ad=False)
    res = ocr.classification(region)
    return res
