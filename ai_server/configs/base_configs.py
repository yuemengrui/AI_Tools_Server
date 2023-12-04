# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os

FASTAPI_TITLE = 'AI_Tools_Servers'
FASTAPI_HOST = '0.0.0.0'
FASTAPI_PORT = 5000

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)
TEMP = './temp'
os.makedirs(TEMP, exist_ok=True)

OCR_BYTE_URL = ''
OCR_GENERAL_URL = ''
UPLOAD_FILE_URL = ''

LAYOUT_MODEL_PATH = ''
LAYOUT_LABELS = ['directory', 'header', 'footer', 'title', 'text', 'table_caption', 'table', 'figure_caption', 'figure']

# API LIMIT
API_LIMIT = {
    "base": "60/minute",
    "layout": "600/minute"
}
