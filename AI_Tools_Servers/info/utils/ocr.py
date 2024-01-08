# *_*coding:utf-8 *_*
# @Author : YueMengRui
import requests
from info import logger
from configs import API_OCR_GENERAL
from info.utils.common import cv2_to_base64


def get_ocr_general_res(img):
    data = {
        'image': cv2_to_base64(img)
    }

    try:
        res = requests.post(url=API_OCR_GENERAL,
                            json=data)

        txt_list = res.json()['data']
        txt_list = [x['text'][0] for x in txt_list]
        txt = ''.join(txt_list)
        return txt
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return ''
