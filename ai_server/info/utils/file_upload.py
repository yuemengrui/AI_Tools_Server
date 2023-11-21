# *_*coding:utf-8 *_*
# @Author : YueMengRui
import requests
from configs import UPLOAD_FILE_URL


def upload_file(file_path: str):
    file_name = file_path.split('/')[-1]
    resp = requests.post(url=UPLOAD_FILE_URL,
                         files={"file": (file_name, open(file_path, 'rb'))})
    return resp.json()['file_url']
