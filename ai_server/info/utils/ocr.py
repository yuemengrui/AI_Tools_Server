# *_*coding:utf-8 *_*
# @Author : YueMengRui
import numpy as np
import cv2
import requests
import base64
from info import logger
from configs import OCR_GENERAL_URL


def get_ocr_general_res(img):
    data = {
        'image': base64.b64encode(np.array(cv2.imencode('.png', img)[1]).tobytes()).decode()
    }

    try:
        res = requests.post(url=OCR_GENERAL_URL,
                            json=data)

        txt_list = res.json()['data']['results']
        txt_list = [x['text'][0] for x in txt_list]
        txt = ''.join(txt_list)
        return txt
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return ''
