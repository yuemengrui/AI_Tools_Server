# *_*coding:utf-8 *_*
# @Author : YueMengRui
import requests
from mylogger import logger
from info.utils.common import delete_temp


def doc_loader(loader, file_path, req):
    try:
        doc = loader.load(file_path)

        data = req.callback.params
        data.update({'data': {'object': 'PDF_Loader', 'data': doc}})
        _ = requests.post(url=req.callback.url, json=data)
    except Exception as e:
        logger.error({'EXCEPTION': e})
    finally:
        delete_temp(file_path)
